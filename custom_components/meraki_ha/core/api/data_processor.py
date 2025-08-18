"""Data processing for the Meraki API client."""

from typing import Any, Dict, List
from ...core.errors import MerakiNetworkError


def process_get_all_data(
    networks: List[Dict[str, Any]],
    devices: List[Dict[str, Any]],
    clients_results: List[Any],
    detail_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Process the data from the get_all_data function."""
    clients: List[Dict[str, Any]] = []
    if isinstance(clients_results, list):
        for i, network in enumerate(networks):
            if isinstance(network, dict) and "id" in network:
                if not isinstance(clients_results[i], Exception):
                    for client in clients_results[i]:
                        client["networkId"] = network["id"]
                    clients.extend(clients_results[i])

    ssids: List[Dict[str, Any]] = []
    appliance_traffic = {}
    vlan_by_network = {}
    rf_profiles_by_network = {}

    for network in networks:
        if isinstance(network, dict) and "id" in network:
            network_ssids = detail_data.get(f"ssids_{network['id']}")
            if network_ssids and not isinstance(network_ssids, Exception):
                for ssid in network_ssids:
                    if (
                        isinstance(ssid, dict)
                        and "name" in ssid
                        and "unconfigured ssid" not in ssid["name"].lower()
                    ):
                        ssid["networkId"] = network["id"]
                        ssids.append(ssid)
            network_traffic = detail_data.get(f"traffic_{network['id']}")
            if isinstance(network_traffic, MerakiNetworkError):
                appliance_traffic[network["id"]] = {
                    "error": "disabled",
                    "reason": str(network_traffic),
                }
            elif network_traffic and not isinstance(network_traffic, Exception):
                appliance_traffic[network["id"]] = network_traffic

            network_vlans = detail_data.get(f"vlans_{network['id']}")
            if isinstance(network_vlans, MerakiNetworkError):
                vlan_by_network[network["id"]] = {
                    "error": "disabled",
                    "reason": str(network_vlans),
                }
            elif network_vlans and not isinstance(network_vlans, Exception):
                vlan_by_network[network["id"]] = network_vlans
            network_rf_profiles = detail_data.get(f"rf_profiles_{network['id']}")
            if network_rf_profiles and not isinstance(network_rf_profiles, Exception):
                rf_profiles_by_network[network["id"]] = network_rf_profiles

    for device in devices:
        if isinstance(device, dict) and "serial" in device:
            if device.get("productType") == "wireless":
                wireless_settings = detail_data.get(
                    f"wireless_settings_{device['serial']}"
                )
                if wireless_settings and not isinstance(wireless_settings, Exception):
                    device["radio_settings"] = wireless_settings
            elif device.get("productType") == "camera":
                video_settings = detail_data.get(f"video_settings_{device['serial']}")
                if video_settings and not isinstance(video_settings, Exception):
                    device["video_settings"] = video_settings
            elif device.get("productType") == "switch":
                ports_statuses = detail_data.get(
                    f"ports_statuses_{device['serial']}"
                )
                if ports_statuses and not isinstance(ports_statuses, Exception):
                    device["ports_statuses"] = ports_statuses
            elif device.get("productType") == "appliance":
                appliance_settings = detail_data.get(
                    f"appliance_settings_{device['serial']}"
                )
                if appliance_settings and not isinstance(
                    appliance_settings, Exception
                ):
                    if "dynamicDns" in appliance_settings:
                        device["dynamicDns"] = appliance_settings["dynamicDns"]

    return {
        "networks": networks,
        "devices": devices,
        "clients": clients,
        "ssids": ssids,
        "appliance_traffic": appliance_traffic,
        "vlans": vlan_by_network,
        "rf_profiles": rf_profiles_by_network,
    }
