"""
Data Fetch Manager for Meraki Data Update Coordinator.

This module contains the logic for fetching and processing data from the Meraki API.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, cast

# Merged Imports
from ...core.fetch_strategies.appliance import ApplianceFetchStrategy
from ...core.fetch_strategies.camera import CameraFetchStrategy
from ...core.fetch_strategies.switch import SwitchFetchStrategy
from ...core.fetch_strategies.wireless import WirelessFetchStrategy
from ...core.models.device import MerakiAppliancePort, MerakiDevice
from ...core.models.network import MerakiNetwork
from ...core.parsers.appliance import parse_appliance_data
from ...core.parsers.network import parse_network_data
from ...core.parsers.sensors import parse_sensor_data
from .client_fetcher import ClientFetcher

if TYPE_CHECKING:
    from ..api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


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

        # Initialize helper classes
        self.client_fetcher = ClientFetcher(self.client)

        # Set of disabled features to prevent repetitive API calls
        self._disabled_features = client._disabled_features

        # Initialize strategies (Adopted from beta)
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

    async def _async_fetch_initial_data(self) -> dict[str, Any]:
        """Fetch the initial batch of data from the Meraki API."""
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
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        data = dict(zip(tasks.keys(), results, strict=True))

        return data

    def _build_network_detail_tasks(
        self,
        network: MerakiNetwork,
        tasks: dict[str, asyncio.Task[Any]],
    ) -> None:
        """Add detail tasks for a single network."""
        if not network.id:
            return
        network_id = cast(str, network.id)
        product_types = network.product_types

        if "wireless" in product_types:
            self.wireless_strategy.build_network_tasks(network_id, product_types, tasks)

        if "appliance" in product_types:
            # We use the strategy from Beta to keep DataFetchManager thin
            self.appliance_strategy.build_network_tasks(network_id, tasks)

    def _build_device_detail_tasks(
        self,
        device: MerakiDevice,
        tasks: dict[str, asyncio.Task[Any]],
    ) -> None:
        """Add detail tasks for a single device."""
        if device.product_type == "camera":
            self.camera_strategy.build_device_tasks(device, tasks)
        elif device.product_type == "switch":
            self.switch_strategy.build_device_tasks(device, tasks)
        elif device.product_type == "appliance":
            self.appliance_strategy.build_device_tasks(device, tasks)

    def _build_detail_tasks(
        self,
        networks: list[MerakiNetwork],
        devices: list[MerakiDevice],
    ) -> dict[str, asyncio.Task[Any]]:
        """Build a dictionary of tasks to fetch detailed data."""
        detail_tasks: dict[str, asyncio.Task[Any]] = {}
        for network in networks:
            self._build_network_detail_tasks(network, detail_tasks)
        for device in devices:
            self._build_device_detail_tasks(device, detail_tasks)
        return detail_tasks

    def _process_detailed_data(
        self,
        detail_data: dict[str, Any],
        networks: list[MerakiNetwork],
        devices: list[MerakiDevice],
        previous_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Process the detailed data using configured strategies."""
        processed_data = parse_network_data(
            detail_data,
            networks,
            previous_data,
            self._disabled_features,
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
                network_id, detail_data, previous_data, processed_data["appliance_traffic"]
            )
            self.appliance_strategy.process_network_vlans(
                network_id, detail_data, previous_data, processed_data["vlans"]
            )

        previous_devices_by_serial = {}
        if previous_data and "devices" in previous_data:
            for d in previous_data["devices"]:
                if "serial" in d:
                    previous_devices_by_serial[d["serial"]] = d

        for device in devices:
            self._process_device_details(
                device, detail_data, previous_devices_by_serial
            )

        return processed_data

    def _process_device_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        previous_devices_by_serial: dict[str, Any],
    ) -> None:
        """Process details for a single device using strategies."""
        prev_device = None
        if device.serial:
            prev_device = previous_devices_by_serial.get(device.serial)

        if device.product_type == "camera":
            self.camera_strategy.process_device_details(device, detail_data, prev_device)
        elif device.product_type == "switch":
            self.switch_strategy.process_device_details(device, detail_data, prev_device)
        elif device.product_type == "appliance":
            self.appliance_strategy.process_device_details(device, detail_data, prev_device)

    async def get_all_data(
        self,
        previous_data: dict[str, Any] | None = None,
        timespan: int | None = None,
    ) -> dict[str, Any]:
        """Fetch all data from the Meraki API concurrently."""
        if previous_data is None:
            previous_data = {}

        _LOGGER.debug("Fetching fresh Meraki data from API")

        if not self.client.has_dashboard:
            await self.client.async_setup()

        initial_results = await self._async_fetch_initial_data()

        networks_res = initial_results.get("networks", [])
        if isinstance(networks_res, Exception):
            _LOGGER.error("Could not fetch networks: %s", networks_res)
        networks_list = [MerakiNetwork.from_dict(n) for n in networks_res] if not isinstance(networks_res, Exception) else []

        devices_res = initial_results.get("devices", [])
        if isinstance(devices_res, Exception):
            _LOGGER.error("Could not fetch devices: %s", devices_res)
        devices_list = [MerakiDevice.from_dict(d) for d in (devices_res if isinstance(devices_res, list) else [])]

        appliance_uplink_statuses = initial_results.get("appliance_uplink_statuses")
        parse_appliance_data(devices_list, appliance_uplink_statuses)

        sensor_readings = initial_results.get("sensor_readings", [])
        parse_sensor_data(
            devices_list,
            sensor_readings if isinstance(sensor_readings, list) else [],
            [],
        )

        detail_tasks = self._build_detail_tasks(networks_list, devices_list)
        detail_data_results = await asyncio.gather(*detail_tasks.values(), return_exceptions=True)
        detail_data_dict = dict(zip(detail_tasks.keys(), detail_data_results, strict=True))

        processed_detailed_data = self._process_detailed_data(
            detail_data_dict, networks_list, devices_list, previous_data
        )

        network_clients, device_clients = await asyncio.gather(
            self.client_fetcher.async_fetch_network_clients(networks_list),
            self.client_fetcher.async_fetch_device_clients(devices_list),
            return_exceptions=True,
        )

        organization_res = initial_results.get("organization", {})
        org_name = organization_res.get("name", "Unknown Organization") if isinstance(organization_res, dict) else "Unknown Organization"

        return {
            "org_name": org_name,
            "networks": networks_list,
            "devices": devices_list,
            "clients": network_clients if isinstance(network_clients, list) else [],
            "clients_by_serial": device_clients if isinstance(device_clients, dict) else {},
            **processed_detailed_data,
        }