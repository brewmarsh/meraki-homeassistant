"""Data Fetch Manager with Smart Error Handling."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, cast

from ...core.const import DEFAULT_CAPS, DEVICE_CAPABILITIES

# Import the custom errors so we can pass them to strategies
from ...core.errors import (
    MerakiTrafficAnalysisError,
    MerakiVlansDisabledError,
)
from ...core.fetch_strategies.appliance import ApplianceFetchStrategy
from ...core.fetch_strategies.camera import CameraFetchStrategy
from ...core.fetch_strategies.sensor import SensorFetchStrategy
from ...core.fetch_strategies.switch import SwitchFetchStrategy
from ...core.fetch_strategies.wireless import WirelessFetchStrategy
from ...core.models.device import MerakiDevice
from ...core.models.network import MerakiNetwork
from ...core.parsers.appliance import parse_appliance_data
from ...core.parsers.devices import parse_device_data
from ...core.parsers.network import parse_network_data
from ...core.parsers.sensors import parse_sensor_data
from .client_fetcher import ClientFetcher

if TYPE_CHECKING:
    from ..api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)

BATCH_SIZE = 5

SILENT_ERRORS = [
    "Traffic Analysis with Hostname Visibility must be enabled",
    "VLANs are not enabled for this network",
]


class DataFetchManager:
    """Class to manage data fetching for the coordinator."""

    def __init__(
        self,
        client: MerakiAPIClient,
        enable_vpn_management: bool = False,
        enable_firewall_rules: bool = False,
        enable_traffic_shaping: bool = False,
        enable_camera_sense: bool = True,
    ) -> None:
        """Initialize the Data Fetch Manager."""
        self.client = client
        self.enable_vpn_management = enable_vpn_management
        self.enable_firewall_rules = enable_firewall_rules
        self.enable_traffic_shaping = enable_traffic_shaping
        self.enable_camera_sense = enable_camera_sense

        self.client_fetcher = ClientFetcher(self.client)
        self._disabled_features = client._disabled_features

        # Initialize strategies
        self.appliance_strategy = ApplianceFetchStrategy(
            client,
            self._disabled_features,
            enable_vpn_management,
            enable_firewall_rules,
            enable_traffic_shaping,
        )
        self.wireless_strategy = WirelessFetchStrategy(client, self._disabled_features)
        self.switch_strategy = SwitchFetchStrategy(client, self._disabled_features)
        self.camera_strategy = CameraFetchStrategy(
            client, self._disabled_features, enable_camera_sense
        )
        self.sensor_strategy = SensorFetchStrategy(client, self._disabled_features)

    async def _execute_batches(self, tasks: dict[str, Any], label: str) -> list[Any]:
        """Execute tasks in batches with cooldown."""
        task_items = list(tasks.items())
        all_results = []
        for i in range(0, len(task_items), BATCH_SIZE):
            if i > 0:
                _LOGGER.debug("Cooling down for 1s between %s batches...", label)
                await asyncio.sleep(1)

            chunk = dict(task_items[i : i + BATCH_SIZE])
            _LOGGER.debug(
                "Executing %s batch: items %d to %d",
                label,
                i + 1,
                min(i + BATCH_SIZE, len(task_items)),
            )
            chunk_results = await asyncio.gather(
                *chunk.values(), return_exceptions=True
            )
            all_results.extend(chunk_results)
        return all_results

    def _process_single_result(self, key: str, result: Any, label: str) -> Any:
        """Process a single task result with smart error handling."""
        if isinstance(result, Exception):
            error_msg = str(result)
            is_silent = False
            for silent_msg in SILENT_ERRORS:
                if silent_msg in error_msg:
                    _LOGGER.debug(
                        "Skipping %s: Configuration requirement not met in "
                        "Meraki Dashboard.",
                        key,
                    )
                    is_silent = True
                    break

            if is_silent:
                if "Traffic Analysis" in error_msg:
                    return MerakiTrafficAnalysisError(error_msg)
                elif "VLANs" in error_msg:
                    return MerakiVlansDisabledError(error_msg)
                else:
                    return []

            return self._handle_fetch_exception(result, key, label)

        if isinstance(result, (dict, list)) or result is None:
            return result

        _LOGGER.debug(
            "Filtering out unexpected type %s for %s during %s",
            type(result),
            key,
            label,
        )
        return None

    def _process_batch_results(
        self, tasks: dict[str, Any], results: list[Any], label: str
    ) -> dict[str, Any]:
        """Process raw batch results into sanitized dictionary."""
        sanitized_results: dict[str, Any] = {}
        for key, result in zip(tasks.keys(), results, strict=True):
            sanitized_results[key] = self._process_single_result(key, result, label)
        return sanitized_results

    async def _async_gather_with_timeout(
        self, tasks: dict[str, Any], timeout: int = 25, label: str = "Tasks"
    ) -> dict[str, Any]:
        """Gather tasks with timeout, batching, and smart error transformation."""
        if not tasks:
            return {}

        _LOGGER.debug(
            "Starting %s: %s items in batches of %s", label, len(tasks), BATCH_SIZE
        )

        try:
            results = await asyncio.wait_for(
                self._execute_batches(tasks, label), timeout=timeout
            )
            return self._process_batch_results(tasks, results, label)

        except asyncio.TimeoutError:
            _LOGGER.error("Timeout during %s. Potential semaphore deadlock.", label)
            _LOGGER.debug("Pending keys for %s: %s", label, list(tasks.keys()))
            # Clean up unawaited coroutines to prevent RuntimeWarnings in tests
            for task in tasks.values():
                if asyncio.iscoroutine(task):
                    task.close()
            raise

    def _handle_fetch_exception(
        self, exception: Exception, key: str, label: str
    ) -> Exception | None:
        """Handle and transform fetch exceptions for smart updates."""
        # 1. Handle already transformed informational errors
        if isinstance(
            exception, (MerakiTrafficAnalysisError, MerakiVlansDisabledError)
        ):
            _LOGGER.debug(
                "Feature disabled for %s during %s: %s", key, label, exception
            )
            return exception

        # 2. Fallback: Log as ERROR and sanitize to None
        _LOGGER.error("Error fetching %s during %s: %s", key, label, exception)
        return None

    async def _async_fetch_initial_data(self) -> dict[str, Any]:
        """Fetch the organization-wide data batch."""
        if not self.client.has_dashboard:
            await self.client.async_setup()

        tasks = {
            "organization": self.client.run_with_semaphore(
                self.client.organization.get_organization(),
            ),
            "networks": self.client.run_with_semaphore(
                self.client.organization.get_organization_networks(),
            ),
            "devices": self.client.run_with_semaphore(
                self.client.organization.get_organization_devices(),
            ),
            "appliance_uplink_statuses": self.client.run_with_semaphore(
                self.client.appliance.get_organization_appliance_uplink_statuses(),
            ),
            "device_statuses": self.client.run_with_semaphore(
                self.client.organization.get_organization_devices_statuses(),
            ),
            "sensor_readings": self.client.run_with_semaphore(
                self.client.sensor.get_organization_sensor_readings_latest(),
            ),
            "switch_ports_statuses": self.client.run_with_semaphore(
                self.client.organization.get_organization_switch_ports_statuses(),
            ),
        }
        return await self._async_gather_with_timeout(tasks, label="Initial batch")

    def _distribute_batch_data(self, batch_data: dict[str, Any]) -> dict[str, Any]:
        """Distribute initial batch data to respective parsers."""
        data: dict[str, Any] = {}

        # Organization
        data["organization"] = batch_data.get("organization")
        if data["organization"] and isinstance(data["organization"], dict):
             data["org_name"] = data["organization"].get("name")

        # Networks
        # Ensure we handle None if networks key is present but None
        networks_raw = batch_data.get("networks") or []
        data["networks"] = [
            MerakiNetwork.from_dict(n) if isinstance(n, dict) else n
            for n in networks_raw
        ]

        # Devices
        # Ensure we handle None
        devices_raw = batch_data.get("devices") or []
        data["devices"] = [
            MerakiDevice.from_dict(d) if isinstance(d, dict) else d
            for d in devices_raw
        ]

        # Statuses
        data["appliance_uplink_statuses"] = batch_data.get("appliance_uplink_statuses")
        data["device_statuses"] = batch_data.get("device_statuses")
        data["sensor_readings"] = batch_data.get("sensor_readings")

        data["switch_ports_statuses"] = batch_data.get("switch_ports_statuses")
        if data["switch_ports_statuses"]:
            for status in data["switch_ports_statuses"]:
                if isinstance(status, dict) and (serial := status.get("serial")):
                    data[f"ports_statuses_{serial}"] = status.get("ports", [])

        # Initialize clients lists
        data["clients"] = []
        data["clients_by_serial"] = {}

        # Parse device statuses immediately as they are available
        parse_device_data(data["devices"], data["device_statuses"] or [])

        return data

    def _get_device_capabilities(self, model: str | None) -> list[str]:
        """Get capabilities for a device model."""
        if not model:
            return list(DEFAULT_CAPS)

        # Exact match
        if caps := DEVICE_CAPABILITIES.get(model):
            return caps

        # Prefix match (e.g. MS120-48 -> MS120)
        # Iterate keys in descending order of length to match longest prefix first
        sorted_keys = sorted(DEVICE_CAPABILITIES.keys(), key=len, reverse=True)
        for key in sorted_keys:
            if model.startswith(key):
                return DEVICE_CAPABILITIES[key]

        return list(DEFAULT_CAPS)

    def _build_detail_tasks(self, data: dict[str, Any]) -> dict[str, Any]:
        """Build tasks for detailed data fetching per network/device."""
        tasks: dict[str, Any] = {}

        # 1. Network Tasks
        for network in data.get("networks", []):
            if not isinstance(network, MerakiNetwork) or not network.id:
                continue

            network_id = str(network.id)
            product_types = network.product_types or []

            if "appliance" in product_types:
                self.appliance_strategy.build_network_tasks(network_id, tasks)

            if "wireless" in product_types:
                self.wireless_strategy.build_network_tasks(network_id, product_types, tasks)

        # 2. Device Tasks
        for device in data.get("devices", []):
            if not isinstance(device, MerakiDevice) or not device.serial:
                continue

            capabilities = self._get_device_capabilities(device.model)

            ptype = device.product_type
            if not ptype:
                continue

            if ptype == "appliance" or ptype == "cellularGateway":
                self.appliance_strategy.build_device_tasks(device, tasks, capabilities, data)
            elif ptype == "wireless":
                self.wireless_strategy.build_device_tasks(device, tasks, capabilities, data)
            elif ptype == "switch":
                self.switch_strategy.build_device_tasks(device, tasks, capabilities, data)
            elif ptype == "camera":
                self.camera_strategy.build_device_tasks(device, tasks, capabilities, data)
            elif ptype == "sensor":
                self.sensor_strategy.build_device_tasks(device, tasks, capabilities, data)

        return tasks

    async def get_all_data(
        self,
        current_data: dict[str, Any] | None = None,
        timespan: int = 300
    ) -> dict[str, Any]:
        """Fetch all data from the Meraki API."""
        # 1. Fetch initial organization data
        initial_data = await self._async_fetch_initial_data()

        # 2. Parse basic structures
        data = self._distribute_batch_data(initial_data)

        # 3. Fetch detailed data per network/device
        detail_tasks = self._build_detail_tasks(data)
        if detail_tasks:
            detail_results = await self._async_gather_with_timeout(
                 detail_tasks, timeout=45, label="Detail batch"
            )
            # 4. Merge detailed results into data
            data.update(detail_results)

        # 5. Process Device Details
        previous_devices_map = {}
        if current_data and "devices" in current_data:
             for d in current_data["devices"]:
                 if isinstance(d, MerakiDevice) and d.serial:
                     previous_devices_map[d.serial] = d

        for device in data.get("devices", []):
            if not isinstance(device, MerakiDevice) or not device.serial:
                continue

            prev_device = previous_devices_map.get(device.serial)
            ptype = device.product_type

            if ptype == "appliance" or ptype == "cellularGateway":
                self.appliance_strategy.process_device_details(device, data, prev_device)
            elif ptype == "wireless":
                self.wireless_strategy.process_device_details(device, data, prev_device)
            elif ptype == "switch":
                self.switch_strategy.process_device_details(device, data, prev_device)
            elif ptype == "camera":
                self.camera_strategy.process_device_details(device, data, prev_device)
            elif ptype == "sensor":
                self.sensor_strategy.process_device_details(device, data, prev_device)

        # 6. Parse Network Details
        network_details = parse_network_data(
            data, # acts as detail_data because results are merged
            data["networks"],
            current_data or {},
            self._disabled_features
        )
        data.update(network_details)

        # 7. Fetch Clients
        networks = data.get("networks", [])
        if networks:
            try:
                clients = await asyncio.wait_for(
                    self.client_fetcher.async_fetch_network_clients(networks),
                    timeout=25
                )
                data["clients"] = clients
            except asyncio.TimeoutError:
                _LOGGER.error("Timeout during %s. Potential semaphore deadlock.", "Client data")
                raise

            # Derive device clients
            devices = data.get("devices", [])
            if devices:
                clients_by_serial = self.client_fetcher.derive_device_clients(clients, devices)
                data["clients_by_serial"] = clients_by_serial

        return data
