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


    def distribute_batch_data(self, data: dict[str, Any]) -> None:
        """Organize initial data for efficient access."""
        self._networks_by_id = {}
        if networks := data.get("networks"):
            for n in networks:
                if isinstance(n, dict):
                    self._networks_by_id[n["id"]] = n

        self._devices_by_network: dict[str, list[dict[str, Any]]] = {}
        if devices := data.get("devices"):
            for d in devices:
                if isinstance(d, dict):
                    net_id = d.get("networkId")
                    if net_id:
                        if net_id not in self._devices_by_network:
                            self._devices_by_network[net_id] = []
                        self._devices_by_network[net_id].append(d)

    def build_detail_tasks(self, data: dict[str, Any], tasks: dict[str, Any]) -> None:
        """Build detailed tasks for networks and devices."""
        # Networks
        for network_id, network in getattr(self, "_networks_by_id", {}).items():
            product_types = network.get("productTypes", [])

            # Appliance
            if "appliance" in product_types:
                self.appliance_strategy.build_network_tasks(network_id, tasks)

            # Wireless
            if "wireless" in product_types:
                self.wireless_strategy.build_network_tasks(network_id, product_types, tasks)

        # Devices
        if devices := data.get("devices"):
             for d in devices:
                if not isinstance(d, dict):
                    continue

                # Basic device object for strategy use
                device = MerakiDevice.from_dict(d)

                # Determine capabilities
                model = device.model or ""
                capabilities = []
                for cap, prefixes in DEVICE_CAPABILITIES.items():
                     if any(model.startswith(prefix) for prefix in prefixes):
                         capabilities.append(cap)
                # Add default caps
                capabilities.extend(DEFAULT_CAPS)

                # Call strategies
                self.switch_strategy.build_device_tasks(device, tasks, capabilities)
                self.wireless_strategy.build_device_tasks(device, tasks, capabilities)
                self.appliance_strategy.build_device_tasks(device, tasks, capabilities)
                self.camera_strategy.build_device_tasks(device, tasks, capabilities)
                self.sensor_strategy.build_device_tasks(device, tasks, capabilities)

    async def get_all_data(
        self, current_data: dict[str, Any] | None, timespan: int = 300
    ) -> dict[str, Any]:
        """Fetch all data from the API."""
        # 1. Fetch initial batch
        data = await self._async_fetch_initial_data()

        # 2. Organize data
        self.distribute_batch_data(data)

        # 3. Build detail tasks
        tasks: dict[str, Any] = {}
        self.build_detail_tasks(data, tasks)

        # 4. Fetch details
        details = await self._async_gather_with_timeout(tasks, label="Detail batch")

        # 5. Merge details into data
        data.update(details)

        return data
