"""Data Fetch Manager for Meraki coordinators."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import UpdateFailed

from ...const_api import DEFAULT_CAPS
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
    from ..api.client import MerakiAPIClient
    from ..models.device import MerakiDevice

_LOGGER = logging.getLogger(__name__)

# Shared cache for organization-wide data to prevent redundant API calls
# between multiple domain-specific coordinators.
_ORG_DATA_CACHE: dict[str, Any] = {}
_ORG_DATA_CACHE_EXPIRY: datetime | None = None
CACHE_TTL = timedelta(seconds=25)


class DataFetchManager:
    """Manager for fetching and distributing Meraki data."""

    def __init__(self, client: MerakiAPIClient) -> None:
        """Initialize the data fetch manager."""
        self.client = client
        self._disabled_features: set[str] = set()
        self.client_fetcher = ClientFetcher(client)

        # Initialize strategies
        self.appliance_strategy = ApplianceFetchStrategy(
            client,
            self._disabled_features,
            enable_vpn_management=True,
            enable_firewall_rules=True,
            enable_traffic_shaping=True,
        )
        self.wireless_strategy = WirelessFetchStrategy(client, self._disabled_features)
        self.switch_strategy = SwitchFetchStrategy(client, self._disabled_features)
        self.camera_strategy = CameraFetchStrategy(client, self._disabled_features)
        self.sensor_strategy = SensorFetchStrategy(client, self._disabled_features)

    async def _async_fetch_initial_data(self) -> dict[str, Any]:
        """Fetch the organization-wide data batch with short-lived caching."""
        global _ORG_DATA_CACHE_EXPIRY

        if (
            _ORG_DATA_CACHE
            and _ORG_DATA_CACHE_EXPIRY
            and datetime.now() < _ORG_DATA_CACHE_EXPIRY
        ):
            _LOGGER.debug("Using cached organization-wide data")
            return _ORG_DATA_CACHE.copy()

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
            "switch_ports": self.client.run_with_semaphore(
                self.client.organization.get_organization_switch_ports_statuses()
            ),
        }
        data = await async_gather_with_timeout(tasks, label="Initial batch")

        # Update cache
        _ORG_DATA_CACHE.clear()
        _ORG_DATA_CACHE.update(data)
        _ORG_DATA_CACHE_EXPIRY = datetime.now() + CACHE_TTL

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
        """Extract and instantiate networks from batch results."""
        from ..models.network import MerakiNetwork

        networks_raw = batch_data.get("networks") or []
        data["networks"] = [
            MerakiNetwork.from_dict(n) if isinstance(n, dict) else n
            for n in networks_raw
        ]

    def _distribute_devices(
        self, data: dict[str, Any], batch_data: dict[str, Any]
    ) -> None:
        """Extract and instantiate devices from batch results."""
        from ..models.device import MerakiDevice

        devices_raw = batch_data.get("devices") or []
        data["devices"] = [
            MerakiDevice.from_dict(d) if isinstance(d, dict) else d
            for d in devices_raw
        ]

    def _distribute_batch_data(self, batch_data: dict[str, Any]) -> dict[str, Any]:
        """Distribute initial batch data to respective parsers and models."""
        data: dict[str, Any] = {}

        self._distribute_organization(data, batch_data)
        self._distribute_networks(data, batch_data)
        self._distribute_devices(data, batch_data)
        self._parse_initial_statuses(data, batch_data)

        data["clients"] = []
        return data

    def _parse_initial_statuses(
        self, data: dict[str, Any], batch_data: dict[str, Any]
    ) -> None:
        """Parse device statuses and switch ports into the device models."""
        statuses = batch_data.get("statuses") or []
        switch_ports = batch_data.get("switch_ports") or []
        parse_device_data(data["devices"], statuses, switch_ports)

    def _get_device_capabilities(self, model: str | None) -> list[str]:
        """Return hardcoded capabilities based on device model."""
        if not model:
            return list(DEFAULT_CAPS)

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

    async def get_all_data(
        self, current_data: dict[str, Any] | None = None, timespan: int = 300
    ) -> dict[str, Any]:
        """Perform a full orchestrated data fetch."""
        batch_data = await self._async_fetch_initial_data()
        data = self._distribute_batch_data(batch_data)

        # Strategy tasks (async)
        await self._build_strategy_tasks(data)

        # Client data fetch (async)
        await self._fetch_client_data(data)

        # Orchestrated parsing
        self._process_data(data, current_data)

        # Sensor parsing
        parse_sensor_data(data["devices"], data.get("sensor_readings"), [])
        return data

    async def _fetch_client_data(self, data: dict[str, Any]) -> None:
        """Fetch client data for all networks."""
        networks = data.get("networks", [])
        if not networks:
            return

        tasks = {
            f"clients_{n.id}": self.client_fetcher.async_fetch_network_clients(n.id)
            for n in networks
            if n.id
        }
        try:
            client_results = await async_gather_with_timeout(
                tasks, timeout=30, label="Client batch"
            )
            data["clients"] = self.client_fetcher.derive_device_clients(client_results)
        except Exception:  # pylint: disable=broad-except
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

        # Strategy-based processing for individual devices
        process_device_strategies(data, previous_devices_map, self.strategies)

        # Strategy-based processing for networks
        process_network_strategies(data, current_data, self.strategies)

        # Parse aggregate network data (VLANs, SSIDs, etc.)
        network_details = parse_network_data(
            data["networks"],
            data,
            current_data or {},
        )
        data.update(network_details)

        # Parse appliance-specific data
        appliance_details = parse_appliance_data(data["devices"], data, current_data)
        data.update(appliance_details)

        return data
