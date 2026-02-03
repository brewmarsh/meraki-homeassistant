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
from ...core.parsers.appliance import parse_appliance_data
from ...core.parsers.sensors import parse_sensor_data
from ...types import MerakiDevice, MerakiNetwork
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

        # Set of disabled features to prevent repetitive API calls
        self._disabled_features: set[str] = set()

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

    async def _async_fetch_devices(self) -> dict[str, Any]:
        """
        Fetch devices from the Meraki API.

        Returns
        -------
            A dictionary containing devices and battery readings.

        """
        devices = await self.client.run_with_semaphore(
            self.client.organization.get_organization_devices(),
        )
        if not isinstance(devices, list):
            _LOGGER.warning("get_organization_devices did not return a list")
            devices = []

        return {
            "devices": [MerakiDevice.from_dict(d) for d in devices],
            "battery_readings": None,
        }

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
            # Type narrowing for network.id
            if not network.id:
                continue
            network_id = cast(str, network.id)
            product_types = network.product_types
            if "wireless" in product_types:
                detail_tasks[f"ssids_{network_id}"] = asyncio.create_task(
                    self.client.run_with_semaphore(
                        self.client.wireless.get_network_ssids(network_id),
                    )
                )
            if "appliance" in product_types:
                if f"traffic_{network_id}" not in self._disabled_features:
                    detail_tasks[f"traffic_{network_id}"] = asyncio.create_task(
                        self.client.run_with_semaphore(
                            self.client.network.get_network_traffic(
                                network_id, "appliance"
                            ),
                        )
                    )

                if f"vlans_{network_id}" not in self._disabled_features:
                    detail_tasks[f"vlans_{network_id}"] = asyncio.create_task(
                        self.client.run_with_semaphore(
                            self.client.appliance.get_network_vlans(network_id),
                        )
                    )

                detail_tasks[f"l3_firewall_rules_{network_id}"] = asyncio.create_task(
                    self.client.run_with_semaphore(
                        self.client.appliance.get_l3_firewall_rules(network_id),
                    )
                )
                detail_tasks[f"traffic_shaping_{network_id}"] = asyncio.create_task(
                    self.client.run_with_semaphore(
                        self.client.appliance.get_traffic_shaping(network_id),
                    )
                )
                if self.enable_vpn_management:
                    detail_tasks[f"vpn_status_{network_id}"] = asyncio.create_task(
                        self.client.run_with_semaphore(
                            self.client.appliance.get_vpn_status(network_id),
                        )
                    )
                detail_tasks[f"appliance_ports_{network_id}"] = asyncio.create_task(
                    self.client.run_with_semaphore(
                        self.client.appliance.get_appliance_ports(network_id),
                    )
                )
                detail_tasks[f"content_filtering_{network_id}"] = asyncio.create_task(
                    self.client.run_with_semaphore(
                        self.client.appliance.get_network_appliance_content_filtering(
                            network_id,
                        ),
                    )
                )
            if "wireless" in product_types:
                detail_tasks[f"rf_profiles_{network_id}"] = asyncio.create_task(
                    self.client.run_with_semaphore(
                        self.client.wireless.get_network_wireless_rf_profiles(
                            network_id
                        ),
                    )
                )
        for device in devices:
            if device.product_type == "camera":
                detail_tasks[f"video_settings_{device.serial}"] = asyncio.create_task(
                    self.client.run_with_semaphore(
                        self.client.camera.get_camera_video_settings(device.serial),
                    )
                )
                detail_tasks[f"sense_settings_{device.serial}"] = asyncio.create_task(
                    self.client.run_with_semaphore(
                        self.client.camera.get_camera_sense_settings(device.serial),
                    )
                )
                detail_tasks[f"camera_analytics_{device.serial}"] = asyncio.create_task(
                    self.client.run_with_semaphore(
                        self.client.camera.get_device_camera_analytics_recent(
                            device.serial,
                        ),
                    )
                )
            elif device.product_type == "switch":
                detail_tasks[f"ports_statuses_{device.serial}"] = asyncio.create_task(
                    self.client.run_with_semaphore(
                        self.client.switch.get_device_switch_ports_statuses(
                            device.serial
                        ),
                    )
                )
            elif device.product_type == "appliance" and device.network_id:
                detail_tasks[f"appliance_settings_{device.serial}"] = (
                    asyncio.create_task(
                        self.client.run_with_semaphore(
                            self.client.appliance.get_network_appliance_settings(
                                device.network_id,
                            ),
                        )
                    )
                )
        return detail_tasks

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
        ssids: list[dict[str, Any]] = []
        appliance_traffic: dict[str, Any] = {}
        vlan_by_network: dict[str, Any] = {}
        l3_firewall_rules_by_network: dict[str, Any] = {}
        traffic_shaping_by_network: dict[str, Any] = {}
        vpn_status_by_network: dict[str, Any] = {}
        rf_profiles_by_network: dict[str, Any] = {}
        content_filtering_by_network: dict[str, Any] = {}
        wireless_settings_by_network: dict[str, Any] = {}

        for network in networks:
            if not network.id:
                continue
            network_id = cast(str, network.id)

            network_ssids_key = f"ssids_{network_id}"
            network_ssids = detail_data.get(network_ssids_key)
            if isinstance(network_ssids, list):
                for ssid in network_ssids:
                    if "unconfigured ssid" not in ssid.get("name", "").lower():
                        ssid["networkId"] = network_id
                        ssids.append(ssid)
            elif previous_data and network_ssids_key in previous_data:
                ssids.extend(previous_data[network_ssids_key])

            network_traffic_key = f"traffic_{network_id}"
            network_traffic = detail_data.get(network_traffic_key)
            if isinstance(network_traffic, MerakiTrafficAnalysisError):
                self._disabled_features.add(network_traffic_key)
                _LOGGER.info(
                    "Traffic analysis is not enabled for network %s. To enable it, "
                    "see https://documentation.meraki.com/MX/Design_and_Configure/Configuration_Guides/Firewall_and_Traffic_Shaping/Traffic_Analysis_and_Classification",
                    network_id,
                )
                appliance_traffic[network_id] = {
                    "error": "disabled",
                    "reason": str(network_traffic),
                }
            elif isinstance(network_traffic, dict):
                appliance_traffic[network_id] = network_traffic
            elif previous_data and network_traffic_key in previous_data:
                appliance_traffic[network_id] = previous_data[network_traffic_key]

            network_vlans_key = f"vlans_{network_id}"
            network_vlans = detail_data.get(network_vlans_key)
            if isinstance(network_vlans, MerakiVlanError):
                self._disabled_features.add(network_vlans_key)
                _LOGGER.info(str(network_vlans))
                vlan_by_network[network_id] = []
            elif isinstance(network_vlans, MerakiInformationalError):
                if "vlans are not enabled" in str(network_vlans).lower():
                    # Fallback for generic handling if needed
                    self._disabled_features.add(network_vlans_key)
                    vlan_by_network[network_id] = []
            elif isinstance(network_vlans, MerakiVlansDisabledError):
                vlan_by_network[network_id] = []
            elif isinstance(network_vlans, list):
                vlan_by_network[network_id] = network_vlans
            elif previous_data and network_vlans_key in previous_data:
                vlan_by_network[network_id] = previous_data[network_vlans_key]

            l3_firewall_rules_key = f"l3_firewall_rules_{network_id}"
            l3_firewall_rules = detail_data.get(l3_firewall_rules_key)
            if isinstance(l3_firewall_rules, dict):
                l3_firewall_rules_by_network[network_id] = l3_firewall_rules
            elif previous_data and l3_firewall_rules_key in previous_data:
                l3_firewall_rules_by_network[network_id] = previous_data[
                    l3_firewall_rules_key
                ]

            traffic_shaping_key = f"traffic_shaping_{network_id}"
            traffic_shaping = detail_data.get(traffic_shaping_key)
            if isinstance(traffic_shaping, dict):
                traffic_shaping_by_network[network_id] = traffic_shaping
            elif previous_data and traffic_shaping_key in previous_data:
                traffic_shaping_by_network[network_id] = previous_data[
                    traffic_shaping_key
                ]

            vpn_status_key = f"vpn_status_{network_id}"
            vpn_status = detail_data.get(vpn_status_key)
            if isinstance(vpn_status, dict):
                vpn_status_by_network[network_id] = vpn_status
            elif previous_data and vpn_status_key in previous_data:
                vpn_status_by_network[network_id] = previous_data[vpn_status_key]

            network_rf_profiles_key = f"rf_profiles_{network_id}"
            network_rf_profiles = detail_data.get(network_rf_profiles_key)
            if isinstance(network_rf_profiles, list):
                rf_profiles_by_network[network_id] = network_rf_profiles
            elif previous_data and network_rf_profiles_key in previous_data:
                rf_profiles_by_network[network_id] = previous_data[
                    network_rf_profiles_key
                ]

            content_filtering_key = f"content_filtering_{network_id}"
            content_filtering = detail_data.get(content_filtering_key)
            if isinstance(content_filtering, dict):
                content_filtering_by_network[network_id] = content_filtering
            elif previous_data and content_filtering_key in previous_data:
                content_filtering_by_network[network_id] = previous_data[
                    content_filtering_key
                ]

            wireless_settings_key = f"wireless_settings_{network_id}"
            wireless_settings = detail_data.get(wireless_settings_key)
            if isinstance(wireless_settings, dict):
                wireless_settings_by_network[network_id] = wireless_settings
            elif previous_data and wireless_settings_key in previous_data:
                wireless_settings_by_network[network_id] = previous_data[
                    wireless_settings_key
                ]

        # Pre-process previous devices for faster lookup
        previous_devices_by_serial = {}
        if previous_data and "devices" in previous_data:
            for d in previous_data["devices"]:
                if "serial" in d:
                    previous_devices_by_serial[d["serial"]] = d

        for device in devices:
            product_type = device.product_type
            prev_device = previous_devices_by_serial.get(device.serial)

            if product_type == "camera":
                if settings := detail_data.get(f"video_settings_{device.serial}"):
                    device.video_settings = settings
                    # The video_settings endpoint also provides the RTSP URL
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

            elif product_type == "switch":
                statuses_key = f"ports_statuses_{device.serial}"
                statuses = detail_data.get(statuses_key)
                if isinstance(statuses, list):
                    device.ports_statuses = statuses
                elif prev_device and "ports_statuses" in prev_device:
                    device.ports_statuses = prev_device["ports_statuses"]

            elif product_type == "appliance":
                if ports := detail_data.get(f"appliance_ports_{device.network_id}"):
                    if isinstance(ports, list):
                        device.appliance_ports = ports
                elif prev_device and "appliance_ports" in prev_device:
                    device.appliance_ports = prev_device["appliance_ports"]

                if settings := detail_data.get(
                    f"appliance_settings_{device.serial}",
                ):
                    if isinstance(settings.get("dynamicDns"), dict):
                        device.dynamic_dns = settings["dynamicDns"]
                elif prev_device and "dynamicDns" in prev_device:
                    device.dynamic_dns = prev_device["dynamicDns"]

        return {
            "ssids": ssids,
            "appliance_traffic": appliance_traffic,
            "vlans": vlan_by_network,
            "l3_firewall_rules": l3_firewall_rules_by_network,
            "traffic_shaping": traffic_shaping_by_network,
            "vpn_status": vpn_status_by_network,
            "rf_profiles": rf_profiles_by_network,
            "content_filtering": content_filtering_by_network,
            "wireless_settings": wireless_settings_by_network,
        }

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
            self._async_fetch_devices(),
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
