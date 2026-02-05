"""
Data Fetch Manager for Meraki Data Update Coordinator.

This module manages high-concurrency data retrieval using the Strategy pattern
and batching to prevent semaphore deadlocks.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, cast

from ...core.const import DEFAULT_CAPS, DEVICE_CAPABILITIES
from ...core.fetch_strategies.appliance import ApplianceFetchStrategy
from ...core.fetch_strategies.camera import CameraFetchStrategy
from ...core.fetch_strategies.sensor import SensorFetchStrategy
from ...core.fetch_strategies.switch import SwitchFetchStrategy
from ...core.fetch_strategies.wireless import WirelessFetchStrategy
from ...core.models.device import MerakiDevice
from ...core.models.network import MerakiNetwork
from ...core.parsers.appliance import parse_appliance_data
from ...core.parsers.network import parse_network_data
from ...core.parsers.sensors import parse_sensor_data
from .client_fetcher import ClientFetcher

if TYPE_CHECKING:
    from ..api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)

BATCH_SIZE = 5


class DataFetchManager:
    """Class to manage data fetching for the coordinator."""

    def __init__(
        self,
        client: MerakiAPIClient,
        enable_vpn_management: bool = False,
        enable_firewall_rules: bool = False,
        enable_traffic_shaping: bool = False,
    ) -> None:
        """Initialize the Data Fetch Manager."""
        self.client = client
        self.enable_vpn_management = enable_vpn_management
        self.enable_firewall_rules = enable_firewall_rules
        self.enable_traffic_shaping = enable_traffic_shaping

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
        self.camera_strategy = CameraFetchStrategy(client, self._disabled_features)
        self.sensor_strategy = SensorFetchStrategy(client, self._disabled_features)

    async def _async_gather_with_timeout(
        self, tasks: dict[str, Any], timeout: int = 25, label: str = "Tasks"
    ) -> dict[str, Any]:
        """Gather tasks with a hard timeout and batching to prevent API overloading."""
        if not tasks:
            return {}

        _LOGGER.debug(
            "Starting %s: %s items in batches of %s", label, len(tasks), BATCH_SIZE
        )

        async def _execute_batches() -> list[Any]:
            """Inner coroutine to handle chunked execution."""
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

        try:
            # Use the batched execution logic (from Beta branch)
            results = await asyncio.wait_for(_execute_batches(), timeout=timeout)
            
            # Sanitization Logic (from Feat branch)
            # Filter out exceptions to prevent downstream crashes
            sanitized_results = {}
            for key, result in zip(tasks.keys(), results, strict=True):
                if isinstance(result, Exception):
                    _LOGGER.error("Error fetching %s during %s: %s", key, label, result)
                    sanitized_results[key] = None
                elif isinstance(result, (dict, list)) or result is None:
                    sanitized_results[key] = result
                else:
                    _LOGGER.debug(
                        "Filtering out unexpected type %s for %s during %s",
                        type(result),
                        key,
                        label,
                    )
                    sanitized_results[key] = None
            return sanitized_results
            
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout during %s. Potential semaphore deadlock.", label)
            # Log specific keys to identify which strategy is hanging
            _LOGGER.debug("Pending keys for %s: %s", label, list(tasks.keys()))
            raise

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
            "sensor_readings": self.client.run_with_semaphore(
                self.client.sensor.get_organization_sensor_readings_latest(),
            ),
            # Bulk load switch ports to reduce individual API calls
            "switch_ports_statuses": self.client.run_with_semaphore(
                self.client.organization.get_organization_switch_ports_statuses(),
            ),
        }
        return await self._async_gather_with_timeout(tasks, label="Initial batch")

    async def _fetch_batch_camera_analytics(
        self, devices: list[MerakiDevice]
    ) -> dict[str, Any]:
        """Fetch camera analytics for all cameras in a single batch of tasks."""
        camera_serials = [d.serial for d in devices if d.product_type == "camera"]
        if not camera_serials:
            return {}

        _LOGGER.debug("Bulk loading analytics for %d cameras", len(camera_serials))
        tasks = {
            f"camera_analytics_{serial}": self.client.run_with_semaphore(
                self.client.camera.get_device_camera_analytics_recent(serial)
            )
            for serial in camera_serials
            if serial
        }

        return await self._async_gather_with_timeout(tasks, label="Camera analytics")

    def _distribute_batch_data(
        self,
        initial_results: dict[str, Any],
        camera_analytics: dict[str, Any],
        detail_data: dict[str, Any],
    ) -> None:
        """Distribute batch-loaded data into detail_data dictionary."""
        # 1. Distribute Switch Ports Statuses
        switch_statuses = initial_results.get("switch_ports_statuses", [])
        if isinstance(switch_statuses, list):
            for switch in switch_statuses:
                serial = switch.get("serial")
                ports = switch.get("ports")
                if serial and ports:
                    detail_data[f"ports_statuses_{serial}"] = ports

        # 2. Distribute Camera Analytics
        detail_data.update(camera_analytics)

    def _build_detail_tasks(
        self,
        networks: list[MerakiNetwork],
        devices: list[MerakiDevice],
        detail_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Orchestrate task building across all strategies."""
        detail_tasks: dict[str, Any] = {}

        for network in networks:
            if not network.id:
                continue
            net_id = cast(str, network.id)
            p_types = network.product_types

            if "wireless" in p_types:
                self.wireless_strategy.build_network_tasks(
                    net_id, p_types, detail_tasks
                )
            if "appliance" in p_types:
                self.appliance_strategy.build_network_tasks(net_id, detail_tasks)

        self._build_device_detail_tasks(devices, detail_tasks, detail_data)

        return detail_tasks

    def _build_device_detail_tasks(
        self,
        devices: list[MerakiDevice],
        tasks: dict[str, Any],
        detail_data: dict[str, Any] | None = None,
    ) -> None:
        """Add per-device detail tasks based on capabilities."""
        if detail_data is None:
            detail_data = {}
            
        for device in devices:
            # ### Lookup Logic
            # Get capabilities for the device model to determine which tasks to add.
            capabilities = DEVICE_CAPABILITIES.get(device.model or "", DEFAULT_CAPS)

            # ### Task Creation Logic
            # Combined Logic: Pass BOTH detail_data (for bulk data) AND capabilities (for guarding)
            if device.product_type == "camera":
                self.camera_strategy.build_device_tasks(
                    device, tasks, capabilities
                )
            elif device.product_type == "switch":
                self.switch_strategy.build_device_tasks(
                    device, tasks, capabilities
                )
            elif device.product_type == "appliance":
                self.appliance_strategy.build_device_tasks(device, tasks, capabilities)
            elif device.product_type == "sensor":
                self.sensor_strategy.build_device_tasks(device, tasks, capabilities)

    def _process_detailed_data(
        self,
        detail_data: dict[str, Any],
        networks: list[MerakiNetwork],
        devices: list[MerakiDevice],
        previous_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Parse results back into the coordinator data structure."""
        processed_data = parse_network_data(
            detail_data, networks, previous_data, self._disabled_features
        )
        processed_data["ssids"] = []
        processed_data["wireless_settings"] = {}

        for network in networks:
            if not network.id:
                continue
            network_id = cast(str, network.id)

            self.wireless_strategy.process_network_data(
                network_id, detail_data, previous_data, processed_data
            )
            self.appliance_strategy.process_network_traffic(
                network_id,
                detail_data,
                previous_data,
                processed_data["appliance_traffic"],
            )
            self.appliance_strategy.process_network_vlans(
                network_id, detail_data, previous_data, processed_data["vlans"]
            )

        previous_devices_by_serial = {
            d.serial: d for d in previous_data.get("devices", []) if hasattr(d, "serial")
        }

        for device in devices:
            prev = (
                previous_devices_by_serial.get(device.serial) if device.serial else None
            )

            if device.product_type == "camera":
                self.camera_strategy.process_device_details(device, detail_data, prev)
            elif device.product_type == "switch":
                self.switch_strategy.process_device_details(device, detail_data, prev)
            elif device.product_type == "appliance":
                self.appliance_strategy.process_device_details(
                    device, detail_data, prev
                )
            elif device.product_type == "sensor":
                self.sensor_strategy.process_device_details(device, detail_data, prev)

        return processed_data

    async def get_all_data(
        self,
        previous_data: dict[str, Any] | None = None,
        timespan: int | None = None,
    ) -> dict[str, Any]:
        """Fetch all data for the coordinator update cycle."""
        previous_data = previous_data or {}
        _LOGGER.debug("Fetching fresh Meraki data from API")

        # 1. Organization-level baseline
        initial_results = await self._async_fetch_initial_data()

        # 2. Convert to Models
        # Ensure results are iterable by using 'or []' in case they were sanitized to None
        networks_list = [
            MerakiNetwork.from_dict(n)
            for n in (initial_results.get("networks") or [])
            if isinstance(n, dict)
        ]
        devices_list = [
            MerakiDevice.from_dict(d)
            for d in (initial_results.get("devices") or [])
            if isinstance(d, dict)
        ]

        # 3. Apply baseline parsers (Uplinks & Sensors)
        parse_appliance_data(
            devices_list, initial_results.get("appliance_uplink_statuses")
        )
        parse_sensor_data(devices_list, initial_results.get("sensor_readings", []), [])

        # 4. Fetch Batch Details (Camera Analytics)
        camera_analytics = await self._fetch_batch_camera_analytics(devices_list)

        # 5. Initialize detail_data and distribute batch results
        detail_data_dict: dict[str, Any] = {}
        self._distribute_batch_data(initial_results, camera_analytics, detail_data_dict)

        # 6. Fetch Remaining Details (Strategy + Timeout Protection)
        detail_tasks = self._build_detail_tasks(
            networks_list, devices_list, detail_data_dict
        )
        fetched_detail_data = await self._async_gather_with_timeout(
            detail_tasks, label="Detailed device data"
        )
        detail_data_dict.update(fetched_detail_data)

        # 7. Fetch Clients (Consolidated: Network-level then derive Device-level)
        client_tasks = {
            "network_clients": self.client_fetcher.async_fetch_network_clients(
                networks_list
            )
        }
        client_results = await self._async_gather_with_timeout(
            client_tasks, label="Client data"
        )
        network_clients = client_results.get("network_clients", [])
        if not isinstance(network_clients, list):
            network_clients = []

        device_clients = self.client_fetcher.derive_device_clients(
            network_clients, devices_list
        )

        # Inject clients for strategies that require them (e.g. Wireless)
        detail_data_dict["clients"] = (
            network_clients if isinstance(network_clients, list) else []
        )

        # 8. Final Processing
        processed_detailed_data = self._process_detailed_data(
            detail_data_dict, networks_list, devices_list, previous_data
        )

        org_data = initial_results.get("organization", {})
        org_name = (
            org_data.get("name", "Unknown Org")
            if isinstance(org_data, dict)
            else "Unknown Org"
        )

        return {
            "org_name": org_name,
            "networks": networks_list,
            "devices": devices_list,
            "clients": network_clients if isinstance(network_clients, list) else [],
            "clients_by_serial": (
                device_clients if isinstance(device_clients, dict) else {}
            ),
            **processed_detailed_data,
        }