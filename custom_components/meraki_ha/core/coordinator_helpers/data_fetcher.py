"""Data Fetch Manager for Meraki coordinators."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.const.device import DEFAULT_CAPS

from ...core.parsers.appliance import parse_appliance_data
from ...core.parsers.devices import parse_device_data
from ...core.parsers.network import parse_network_data
from ...core.parsers.sensors import parse_sensor_data
from ..fetch_strategies.appliance import ApplianceFetchStrategy
from ..fetch_strategies.camera import CameraFetchStrategy
from ..fetch_strategies.sensor import SensorFetchStrategy
from ..fetch_strategies.switch import SwitchFetchStrategy
from ..fetch_strategies.wireless import WirelessFetchStrategy
from .batch_utils import async_gather_with_timeout
from .client_fetcher import ClientFetcher
from .strategy_executor import (
    collect_device_tasks,
    collect_network_tasks,
    process_device_strategies,
    process_network_strategies,
)

if TYPE_CHECKING:
    from ..api import MerakiApiClientProtocol
    from ..models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class DataFetchManager:
    """Manager for fetching and distributing Meraki data."""

    def __init__(
        self,
        client: MerakiApiClientProtocol,
        enable_vpn_management: bool = False,
        enable_firewall_rules: bool = False,
        enable_traffic_shaping: bool = False,
        enable_camera_sense: bool = False,
    ) -> None:
        """Initialize the data fetch manager."""
        self.client = client
        self.enable_vpn_management = enable_vpn_management
        self.enable_firewall_rules = enable_firewall_rules
        self.enable_traffic_shaping = enable_traffic_shaping
        self.enable_camera_sense = enable_camera_sense
        self._disabled_features: set[str] = set()
        self.client_fetcher = ClientFetcher(client)

        # Instance-based cache for organization-wide data
        self._org_data_cache: dict[str, Any] = {}
        self._org_data_cache_expiry: float = 0
        self._cache_ttl = 30  # seconds

        # Initialize strategies
        self.appliance_strategy = ApplianceFetchStrategy(
            client,
            self._disabled_features,
            enable_vpn_management=self.enable_vpn_management,
            enable_firewall_rules=self.enable_firewall_rules,
            enable_traffic_shaping=self.enable_traffic_shaping,
        )
        self.wireless_strategy = WirelessFetchStrategy(client, self._disabled_features)
        self.switch_strategy = SwitchFetchStrategy(client, self._disabled_features)
        self.camera_strategy = CameraFetchStrategy(
            client,
            self._disabled_features,
            enable_camera_sense=self.enable_camera_sense,
        )
        self.sensor_strategy = SensorFetchStrategy(client, self._disabled_features)

    async def _async_fetch_batch_data(self, fast_only: bool = False) -> dict[str, Any]:
        """Fetch the organization-wide data batch with short-lived caching."""
        current_time = time.time()
        if (
            self._org_data_cache
            and current_time < self._org_data_cache_expiry
            and (fast_only or "switch_ports" in self._org_data_cache)
        ):
            _LOGGER.debug("Using cached organization-wide data")
            return self._org_data_cache

        if not self.client.has_dashboard:
            await self.client.async_setup()

        tasks = {
            "organization": self.client.run_with_semaphore(
                self.client.organization.get_organization()
            ),
            "networks": self.client.run_with_semaphore(
                self.client.organization.get_organization_networks()
            ),
            "devices": self.client.run_with_semaphore(
                self.client.organization.get_organization_devices()
            ),
            "statuses": self.client.run_with_semaphore(
                self.client.organization.get_organization_devices_statuses()
            ),
        }

        if not fast_only:
            tasks["switch_ports"] = self.client.run_with_semaphore(
                self.client.organization.get_organization_switch_ports_statuses()
            )
            tasks["appliance_uplink_statuses"] = self.client.run_with_semaphore(
                self.client.appliance.get_organization_appliance_uplink_statuses()
            )
            tasks["sensor_readings"] = self.client.run_with_semaphore(
                self.client.sensor.get_organization_sensor_readings_latest()
            )

        data = await async_gather_with_timeout(tasks, label="Batch fetch")

        # Update cache
        self._org_data_cache.clear()
        self._org_data_cache.update(data)
        self._org_data_cache_expiry = current_time + self._cache_ttl

        return data

    def _distribute_organization(
        self, data: dict[str, Any], batch_data: dict[str, Any]
    ) -> None:
        """Extract organization data from batch results."""
        data["organization"] = batch_data.get("organization")
        if data["organization"] and isinstance(data["organization"], dict):
            data["org_name"] = data["organization"].get("name")

    def _distribute_networks(
        self, data: dict[str, Any], batch_data: dict[str, Any]
    ) -> None:
        """Extract and instantiate networks with guaranteed organization_id propagation."""
        from ..models.network import MerakiNetwork

        networks_raw = batch_data.get("networks") or []

        # Extract org_id from the batch data to ensure it's propagated to models
        # This is critical for discovery handlers that filter by organization_id.
        org_id = None
        if org_dict := batch_data.get("organization"):
            if isinstance(org_dict, dict):
                org_id = org_dict.get("id")

        processed_networks = []
        for n in networks_raw:
            if isinstance(n, dict):
                # Backfill organizationId if the API omitted it but we have it in context
                if org_id and not n.get("organizationId"):
                    n["organizationId"] = org_id
                processed_networks.append(MerakiNetwork.from_dict(n))
            else:
                processed_networks.append(n)

        data["networks"] = processed_networks

    def _distribute_devices(
        self, data: dict[str, Any], batch_data: dict[str, Any]
    ) -> None:
        """Extract and instantiate devices from batch results."""
        from ..models.device import MerakiDevice

        devices_raw = batch_data.get("devices") or []
        data["devices"] = [
            MerakiDevice.from_dict(d) if isinstance(d, dict) else d for d in devices_raw
        ]

    def _distribute_batch_data(self, batch_data: dict[str, Any]) -> dict[str, Any]:
        """Distribute initial batch data to respective parsers and models."""
        data: dict[str, Any] = {}

        self._distribute_organization(data, batch_data)
        self._distribute_networks(data, batch_data)
        self._distribute_devices(data, batch_data)
        self._parse_initial_statuses(data, batch_data)

        data["appliance_uplink_statuses"] = batch_data.get("appliance_uplink_statuses")
        data["sensor_readings"] = batch_data.get("sensor_readings")

        data["clients"] = []
        return data

    def _parse_initial_statuses(
        self, data: dict[str, Any], batch_data: dict[str, Any]
    ) -> None:
        """Parse device statuses and switch ports into the device models."""
        statuses = batch_data.get("statuses") or []
        parse_device_data(data["devices"], statuses)

        switch_ports = batch_data.get("switch_ports") or []
        for entry in switch_ports:
            if isinstance(entry, dict) and (serial := entry.get("serial")):
                data[f"switch_ports_{serial}"] = entry.get("ports", [])

    def _get_device_capabilities(self, model: str | None) -> list[str]:
        """Return hardcoded capabilities based on device model."""
        from custom_components.meraki_ha.const.device import DEVICE_CAPABILITIES

        if not model:
            return list(DEFAULT_CAPS)

        for prefix, caps in DEVICE_CAPABILITIES.items():
            if model.startswith(prefix):
                return list(caps)

        return list(DEFAULT_CAPS)

    @property
    def strategies(self) -> dict[str, Any]:
        """Return the strategy map for device types."""
        return {
            "appliance": self.appliance_strategy,
            "cellularGateway": self.appliance_strategy,
            "wireless": self.wireless_strategy,
            "switch": self.switch_strategy,
            "camera": self.camera_strategy,
            "sensor": self.sensor_strategy,
        }

    async def _build_strategy_tasks(self, data: dict[str, Any]) -> None:
        """Build and execute detailed data fetching tasks."""
        tasks: dict[str, Any] = {}
        collect_network_tasks(data, tasks, self.strategies)
        collect_device_tasks(
            data, tasks, self.strategies, self._get_device_capabilities
        )

        if tasks:
            results = await async_gather_with_timeout(
                tasks, timeout=45, label="Detail batch"
            )
            data.update(results)

    async def get_device_data(
        self, current_data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Perform a lightweight orchestrated data fetch (Fast Poll)."""
        batch_data = await self._async_fetch_batch_data(fast_only=True)
        data = self._distribute_batch_data(batch_data)
        self._process_data(data, current_data)
        return data

    async def get_sensor_data(
        self, current_data: dict[str, Any] | None = None, timespan: int = 300
    ) -> dict[str, Any]:
        """Perform a full heavy orchestrated data fetch (Slow Poll)."""
        batch_data = await self._async_fetch_batch_data(fast_only=False)
        data = self._distribute_batch_data(batch_data)

        await self._build_strategy_tasks(data)
        await self._fetch_client_data(data)
        self._process_data(data, current_data)

        try:
            sensor_details = parse_sensor_data(
                data["devices"], data.get("sensor_readings"), []
            )
            data.update(sensor_details)
        except Exception as err:
            _LOGGER.error("Failed to parse sensor data: %s", err, exc_info=True)

        return data

    async def get_all_data(
        self, current_data: dict[str, Any] | None = None, timespan: int = 300
    ) -> dict[str, Any]:
        """Legacy method for backward compatibility. Performs full fetch."""
        return await self.get_sensor_data(current_data, timespan)

    async def _fetch_client_data(self, data: dict[str, Any]) -> None:
        """Fetch client data for all networks."""
        networks = data.get("networks", [])
        if not networks:
            return

        tasks = {
            f"clients_{n.id}": self.client_fetcher.async_fetch_network_clients([n])
            for n in networks
            if n.id
        }
        try:
            client_results = await async_gather_with_timeout(
                tasks, timeout=30, label="Client batch"
            )
            all_clients: list[dict[str, Any]] = []
            for result in client_results.values():
                if isinstance(result, list):
                    all_clients.extend(result)
            data["clients_by_serial"] = self.client_fetcher.derive_device_clients(
                all_clients, data["devices"]
            )
            data["clients"] = all_clients
        except Exception:
            _LOGGER.error("Timeout during client data fetch")
            data["clients"] = {}

    def _process_data(
        self, data: dict[str, Any], current_data: dict[str, Any] | None
    ) -> dict[str, Any]:
        """Orchestrate the parsing and strategy processing."""
        previous_devices_map: dict[str, MerakiDevice] = {}
        if current_data and "devices" in current_data:
            for d in current_data["devices"]:
                if d.serial:
                    previous_devices_map[d.serial] = d

        if "clients_by_serial" in data:
            data["clients"] = data["clients_by_serial"]
        process_device_strategies(data, previous_devices_map, self.strategies)
        process_network_strategies(data, current_data, self.strategies)

        network_details = parse_network_data(
            data,
            data["networks"],
            current_data or {},
            self._disabled_features,
        )
        data.update(network_details)

        appliance_details = parse_appliance_data(data["devices"], data, current_data)
        data.update(appliance_details)
