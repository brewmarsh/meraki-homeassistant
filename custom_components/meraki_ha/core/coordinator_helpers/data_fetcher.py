"""
Data Fetch Manager for Meraki Data Update Coordinator.

This module contains the logic for fetching and processing data from the Meraki API.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, cast

from ...core.parsers.appliance import parse_appliance_data
from ...core.parsers.sensors import parse_sensor_data
from ...types import MerakiDevice, MerakiNetwork
from .client_fetcher import ClientFetcher
from .detail_fetcher import DetailFetcher
from .detail_processor import DetailProcessor
from .device_fetcher import DeviceFetcher

if TYPE_CHECKING:
    from ..api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class DataFetchManager:
    """Class to manage data fetching for the coordinator."""

    def __init__(
        self,
        client: MerakiAPIClient,
        enable_vpn_management: bool = False,
    ) -> None:
        """
        Initialize the Data Fetch Manager.

        Args:
            client: The Meraki API client.
            enable_vpn_management: Whether to enable VPN management.

        """
        self.client = client
        self.enable_vpn_management = enable_vpn_management

        # Initialize helper classes
        self.client_fetcher = ClientFetcher(self.client)
        self.device_fetcher = DeviceFetcher(self.client)
        self.detail_fetcher = DetailFetcher(self.client)
        self.detail_processor = DetailProcessor(self.client)

        # Set of disabled features to prevent repetitive API calls
        # Note: DetailFetcher/Processor in beta access client._disabled_features directly.
        # We maintain this set on client for compatibility.

    async def _async_fetch_initial_data(self) -> dict[str, Any]:
        """
        Fetch the initial batch of data from the Meraki API.

        Returns
        -------
            A dictionary of initial data.

        """
        if not self.client.has_dashboard:
            await self.client.async_setup()

        tasks = {
            "organization": self.client.run_with_semaphore(
                self.client.organization.get_organization(),
            ),
            "networks": self.client.run_with_semaphore(
                self.client.organization.get_organization_networks(),
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

    def _build_detail_tasks(
        self,
        networks: list[MerakiNetwork],
        devices: list[MerakiDevice],
    ) -> dict[str, asyncio.Task[Any]]:
        """
        Build a dictionary of tasks to fetch detailed data.

        Args:
            networks: A list of networks.
            devices: A list of devices.

        Returns
        -------
            A dictionary of tasks.

        """
        return self.detail_fetcher.build_detail_tasks(networks, devices)

    def _process_detailed_data(
        self,
        detail_data: dict[str, Any],
        networks: list[MerakiNetwork],
        devices: list[MerakiDevice],
        previous_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Process the detailed data and merge it into the main data structure.

        Args:
            detail_data: The raw detailed data from the API.
            networks: A list of networks.
            devices: A list of devices.
            previous_data: The previous data from the coordinator.

        Returns
        -------
            The processed detailed data.

        """
        return self.detail_processor.process_detailed_data(
            detail_data, networks, devices, previous_data
        )

    async def get_all_data(
        self,
        previous_data: dict[str, Any] | None = None,
        timespan: int | None = None,
    ) -> dict[str, Any]:
        """
        Fetch all data from the Meraki API concurrently, with caching.

        Args:
            previous_data: The previous data from the coordinator.
            timespan: The timespan for the data.

        Returns
        -------
            A dictionary of all data.

        """
        if previous_data is None:
            previous_data = {}

        _LOGGER.debug("Fetching fresh Meraki data from API")

        # Ensure async_setup is called to initialize client.dashboard
        if not self.client.has_dashboard:
            await self.client.async_setup()

        initial_results, device_fetcher_result = await asyncio.gather(
            self._async_fetch_initial_data(),
            self.device_fetcher.async_fetch_devices(),
        )

        networks_res = initial_results.get("networks", [])
        if isinstance(networks_res, Exception):
            _LOGGER.warning(
                "Could not fetch networks, network data will be unavailable: %s",
                networks_res,
            )
            networks_list = []
        else:
            networks_list = [MerakiNetwork.from_dict(n) for n in networks_res]

        if isinstance(device_fetcher_result, Exception):
            _LOGGER.warning(
                "Could not fetch devices: %s",
                device_fetcher_result,
            )
            devices_list = []
            battery_readings: list[dict[str, Any]] | None = []
        else:
            devices_list = device_fetcher_result.get("devices", [])
            battery_readings = device_fetcher_result.get("battery_readings")

        appliance_uplink_statuses = initial_results.get("appliance_uplink_statuses")
        parse_appliance_data(devices_list, appliance_uplink_statuses)

        sensor_readings = initial_results.get("sensor_readings")

        if isinstance(sensor_readings, Exception):
            _LOGGER.warning("Could not fetch sensor readings: %s", sensor_readings)
            sensor_readings = []

        parse_sensor_data(
            devices_list,
            cast(list[dict[str, Any]], sensor_readings)
            if isinstance(sensor_readings, list)
            else [],
            battery_readings if battery_readings is not None else [],
        )

        detail_tasks = self._build_detail_tasks(networks_list, devices_list)
        detail_data_results = await asyncio.gather(
            *detail_tasks.values(),
            return_exceptions=True,
        )
        detail_data_dict = dict(
            zip(detail_tasks.keys(), detail_data_results, strict=True)
        )

        # This will populate MerakiDevice and MerakiNetwork objects with parsed data
        processed_detailed_data = self._process_detailed_data(
            detail_data_dict,
            networks_list,
            devices_list,
            previous_data,
        )

        network_clients, device_clients = await asyncio.gather(
            self.client_fetcher.async_fetch_network_clients(networks_list),
            self.client_fetcher.async_fetch_device_clients(devices_list),
            return_exceptions=True,
        )

        organization_res = initial_results.get("organization", {})
        org_name = (
            organization_res.get("name")
            if isinstance(organization_res, dict)
            else "Unknown Organization"
        )

        return {
            "org_name": org_name,
            "networks": networks_list,
            "devices": devices_list,
            "clients": network_clients if isinstance(network_clients, list) else [],
            "clients_by_serial": (
                device_clients if isinstance(device_clients, dict) else {}
            ),
            "ssids": processed_detailed_data.get("ssids", []),
            "appliance_traffic": processed_detailed_data.get("appliance_traffic", {}),
            "vlans": processed_detailed_data.get("vlans", {}),
            "l3_firewall_rules": processed_detailed_data.get("l3_firewall_rules", {}),
            "traffic_shaping": processed_detailed_data.get("traffic_shaping", {}),
            "vpn_status": processed_detailed_data.get("vpn_status", {}),
            "rf_profiles": processed_detailed_data.get("rf_profiles", {}),
            "content_filtering": processed_detailed_data.get("content_filtering", {}),
            "wireless_settings": processed_detailed_data.get("wireless_settings", {}),
        }
