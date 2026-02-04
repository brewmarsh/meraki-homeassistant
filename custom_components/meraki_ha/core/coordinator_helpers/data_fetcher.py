"""
Data Fetch Manager for Meraki Data Update Coordinator.

This module contains the logic for fetching and processing data from the Meraki API.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, cast

from ...core.errors import (
    MerakiInformationalError,
    MerakiTrafficAnalysisError,
    MerakiVlanError,
    MerakiVlansDisabledError,
)
from ...core.models.device import MerakiAppliancePort, MerakiDevice
from ...core.models.network import MerakiNetwork
from ...core.parsers.appliance import parse_appliance_data
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
        """
        Initialize the Data Fetch Manager.

        Args:
            client: The Meraki API client.
            enable_vpn_management: Whether to enable VPN management.
            enable_firewall_rules: Whether to enable firewall rule management.
            enable_traffic_shaping: Whether to enable traffic shaping management.

        """
        self.client = client
        self.enable_vpn_management = enable_vpn_management
        self.enable_firewall_rules = enable_firewall_rules
        self.enable_traffic_shaping = enable_traffic_shaping

        # Initialize helper classes
        self.client_fetcher = ClientFetcher(self.client)

        # Set of disabled features to prevent repetitive API calls
        self._disabled_features = client._disabled_features

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
            tasks.update(
                self.client.wireless.get_network_detail_tasks(network_id, product_types)
            )

        if "appliance" in product_types:
            self._build_appliance_network_tasks(network_id, tasks)

    def _build_appliance_network_tasks(
        self,
        network_id: str,
        tasks: dict[str, asyncio.Task[Any]],
    ) -> None:
        """Add appliance specific network tasks."""
        if f"traffic_{network_id}" not in self._disabled_features:
            tasks[f"traffic_{network_id}"] = asyncio.create_task(
                self.client.run_with_semaphore(
                    self.client.network.get_network_traffic(network_id, "appliance"),
                )
            )

        if f"vlans_{network_id}" not in self._disabled_features:
            tasks[f"vlans_{network_id}"] = asyncio.create_task(
                self.client.run_with_semaphore(
                    self.client.get_vlan_data(network_id),
                )
            )

        if self.enable_firewall_rules:
            tasks[f"l3_firewall_rules_{network_id}"] = asyncio.create_task(
                self.client.run_with_semaphore(
                    self.client.appliance.get_l3_firewall_rules(network_id),
                )
            )
        if self.enable_traffic_shaping:
            tasks[f"traffic_shaping_{network_id}"] = asyncio.create_task(
                self.client.run_with_semaphore(
                    self.client.appliance.get_traffic_shaping(network_id),
                )
            )
        if self.enable_vpn_management:
            tasks[f"vpn_status_{network_id}"] = asyncio.create_task(
                self.client.run_with_semaphore(
                    self.client.appliance.get_vpn_status(network_id),
                )
            )
        tasks[f"appliance_ports_{network_id}"] = asyncio.create_task(
            self.client.run_with_semaphore(
                self.client.appliance.get_appliance_ports(network_id),
            )
        )
        tasks[f"content_filtering_{network_id}"] = asyncio.create_task(
            self.client.run_with_semaphore(
                self.client.appliance.get_network_appliance_content_filtering(
                    network_id,
                ),
            )
        )

    def _build_device_detail_tasks(
        self,
        device: MerakiDevice,
        tasks: dict[str, asyncio.Task[Any]],
    ) -> None:
        """Add detail tasks for a single device."""
        if device.product_type == "camera":
            tasks[f"video_settings_{device.serial}"] = asyncio.create_task(
                self.client.run_with_semaphore(
                    self.client.camera.get_camera_video_settings(device.serial),
                )
            )
            tasks[f"sense_settings_{device.serial}"] = asyncio.create_task(
                self.client.run_with_semaphore(
                    self.client.camera.get_camera_sense_settings(device.serial),
                )
            )
            tasks[f"camera_analytics_{device.serial}"] = asyncio.create_task(
                self.client.run_with_semaphore(
                    self.client.camera.get_device_camera_analytics_recent(
                        device.serial,
                    ),
                )
            )
        elif device.product_type == "switch":
            tasks[f"ports_statuses_{device.serial}"] = asyncio.create_task(
                self.client.run_with_semaphore(
                    self.client.switch.get_device_switch_ports_statuses(device.serial),
                )
            )
        elif device.product_type == "appliance" and device.network_id:
            tasks[f"appliance_settings_{device.serial}"] = asyncio.create_task(
                self.client.run_with_semaphore(
                    self.client.appliance.get_network_appliance_settings(
                        device.network_id,
                    ),
                )
            )

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
        detail_tasks: dict[str, asyncio.Task[Any]] = {}
        for network in networks:
            self._build_network_detail_tasks(network, detail_tasks)
        for device in devices:
            self._build_device_detail_tasks(device, detail_tasks)
        return detail_tasks

    def _process_network_wireless_data(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        processed_data: dict[str, Any],
    ) -> None:
        """Process wireless data (SSIDs and RF Profiles) for a network."""
        wireless_data = self.client.wireless.process_network_detail_data(
            detail_data, network_id, previous_data
        )

        ssids = wireless_data.get("ssids", [])
        if ssids:
            cast(list[dict[str, Any]], processed_data["ssids"]).extend(ssids)

        rf_profiles = wireless_data.get("rf_profiles")
        if isinstance(rf_profiles, dict):
            processed_data["rf_profiles"].update(rf_profiles)

    def _process_network_traffic(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        appliance_traffic: dict[str, Any],
    ) -> None:
        """Process traffic data for a network."""
        key = f"traffic_{network_id}"
        data = detail_data.get(key)
        if isinstance(data, MerakiTrafficAnalysisError):
            self._disabled_features.add(key)
            _LOGGER.info(
                "Traffic analysis is not enabled for network %s.",
                network_id,
            )
            appliance_traffic[network_id] = {
                "error": "disabled",
                "reason": str(data),
            }
        elif isinstance(data, dict):
            appliance_traffic[network_id] = data
        elif previous_data and key in previous_data:
            appliance_traffic[network_id] = previous_data[key]

    def _process_network_vlans(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        vlan_by_network: dict[str, Any],
    ) -> None:
        """Process VLAN data for a network."""
        key = f"vlans_{network_id}"
        data = detail_data.get(key)
        if isinstance(data, (MerakiVlanError, MerakiVlansDisabledError)):
            if isinstance(data, MerakiVlanError):
                self._disabled_features.add(key)
                _LOGGER.info(str(data))
            vlan_by_network[network_id] = []
        elif isinstance(data, MerakiInformationalError):
            if "vlans are not enabled" in str(data).lower():
                self._disabled_features.add(key)
                vlan_by_network[network_id] = []
        elif isinstance(data, list):
            vlan_by_network[network_id] = data
        elif previous_data and key in previous_data:
            vlan_by_network[network_id] = previous_data[key]

    def _process_simple_network_data(
        self,
        network_id: str,
        detail_data: dict[str, Any],
        previous_data: dict[str, Any],
        key_prefix: str,
        storage: dict[str, Any],
        data_type: type = dict,
    ) -> None:
        """Process simple network data."""
        key = f"{key_prefix}_{network_id}"
        data = detail_data.get(key)
        if isinstance(data, data_type):
            storage[network_id] = data
        elif previous_data and key in previous_data:
            storage[network_id] = previous_data[key]

    def _process_device_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        previous_devices_by_serial: dict[str, Any],
    ) -> None:
        """Process details for a single device."""
        prev_device = None
        if device.serial:
            prev_device = previous_devices_by_serial.get(device.serial)

        if device.product_type == "camera":
            self._process_camera_details(device, detail_data, prev_device)
        elif device.product_type == "switch":
            self._process_switch_details(device, detail_data, prev_device)
        elif device.product_type == "appliance":
            self._process_appliance_details(device, detail_data, prev_device)

    def _process_camera_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: dict[str, Any] | None,
    ) -> None:
        """Process camera details."""
        if settings := detail_data.get(f"video_settings_{device.serial}"):
            device.video_settings = settings
            if isinstance(settings, dict):
                device.rtsp_url = settings.get("rtsp_url")
            else:
                device.rtsp_url = None
        elif prev_device and "video_settings" in prev_device:
            device.video_settings = prev_device["video_settings"]
            device.rtsp_url = prev_device.get("rtsp_url")

        if settings := detail_data.get(f"sense_settings_{device.serial}"):
            device.sense_settings = settings
        elif prev_device and "sense_settings" in prev_device:
            device.sense_settings = prev_device["sense_settings"]

    def _process_switch_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: dict[str, Any] | None,
    ) -> None:
        """Process switch details."""
        statuses_key = f"ports_statuses_{device.serial}"
        statuses = detail_data.get(statuses_key)
        if isinstance(statuses, list):
            device.ports_statuses = statuses
        elif prev_device and "ports_statuses" in prev_device:
            device.ports_statuses = prev_device["ports_statuses"]

    def _process_appliance_details(
        self,
        device: MerakiDevice,
        detail_data: dict[str, Any],
        prev_device: dict[str, Any] | None,
    ) -> None:
        """Process appliance details."""
        if ports := detail_data.get(f"appliance_ports_{device.network_id}"):
            if isinstance(ports, list):
                device.appliance_ports = [
                    MerakiAppliancePort.from_dict(p)
                    for p in ports
                    if isinstance(p, dict)
                ]
        elif prev_device and "appliance_ports" in prev_device:
            device.appliance_ports = prev_device["appliance_ports"]

        if settings := detail_data.get(f"appliance_settings_{device.serial}"):
            if isinstance(settings.get("dynamicDns"), dict):
                device.dynamic_dns = settings["dynamicDns"]
        elif prev_device and "dynamicDns" in prev_device:
            device.dynamic_dns = prev_device["dynamicDns"]

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
        processed_data: dict[str, Any] = {
            "ssids": [],
            "appliance_traffic": {},
            "vlans": {},
            "l3_firewall_rules": {},
            "traffic_shaping": {},
            "vpn_status": {},
            "rf_profiles": {},
            "content_filtering": {},
            "wireless_settings": {},
        }

        for network in networks:
            if not network.id:
                continue
            network_id = cast(str, network.id)

            self._process_network_wireless_data(
                network_id, detail_data, previous_data, processed_data
            )
            self._process_network_traffic(
                network_id,
                detail_data,
                previous_data,
                processed_data["appliance_traffic"],
            )
            self._process_network_vlans(
                network_id, detail_data, previous_data, processed_data["vlans"]
            )
            for key in [
                "l3_firewall_rules",
                "traffic_shaping",
                "vpn_status",
                "content_filtering",
                "wireless_settings",
            ]:
                self._process_simple_network_data(
                    network_id,
                    detail_data,
                    previous_data,
                    key,
                    processed_data[key],
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

        if not self.client.has_dashboard:
            await self.client.async_setup()

        initial_results = await self._async_fetch_initial_data()

        networks_res = initial_results.get("networks", [])
        if isinstance(networks_res, Exception):
            _LOGGER.warning(
                "Could not fetch networks, network data will be unavailable: %s",
                networks_res,
            )
            networks_list = []
        else:
            networks_list = [MerakiNetwork.from_dict(n) for n in networks_res]

        devices_res = initial_results.get("devices", [])
        if isinstance(devices_res, Exception):
            _LOGGER.warning(
                "Could not fetch devices: %s",
                devices_res,
            )
            devices_list = []
        else:
            devices_list = [
                MerakiDevice.from_dict(d) if isinstance(d, dict) else d
                for d in (devices_res if isinstance(devices_res, list) else [])
            ]

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
            [],  # Battery readings are already in sensor_readings
        )

        detail_tasks = self._build_detail_tasks(networks_list, devices_list)
        detail_data_results = await asyncio.gather(
            *detail_tasks.values(),
            return_exceptions=True,
        )
        detail_data_dict = dict(
            zip(detail_tasks.keys(), detail_data_results, strict=True)
        )

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
            **processed_detailed_data,
        }
