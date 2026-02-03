"""Processes detailed data for the Meraki coordinator."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from ...core.errors import (
    MerakiInformationalError,
    MerakiTrafficAnalysisError,
    MerakiVlanError,
    MerakiVlansDisabledError,
)

if TYPE_CHECKING:
    from ...types import MerakiDevice, MerakiNetwork
    from ..api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class DetailProcessor:
    """Class to process detailed data."""

    def __init__(self, client: MerakiAPIClient) -> None:
        """
        Initialize the detail processor.

        Args:
            client: The Meraki API client.
        """
        self._client = client

    def process_detailed_data(
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
                self._client._disabled_features.add(network_traffic_key)
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
                self._client._disabled_features.add(network_vlans_key)
                _LOGGER.info(str(network_vlans))
                vlan_by_network[network_id] = []
            elif isinstance(network_vlans, MerakiInformationalError):
                if "vlans are not enabled" in str(network_vlans).lower():
                    # Fallback for generic handling if needed
                    self._client._disabled_features.add(network_vlans_key)
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
