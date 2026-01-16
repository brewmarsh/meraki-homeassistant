"""Parsers for Meraki network data."""
from __future__ import annotations
import logging
from typing import Any
from ..errors import MerakiInformationalError
from ...types import MerakiNetwork

_LOGGER = logging.getLogger(__name__)


def parse_network_data(
    detail_data: dict[str, Any],
    networks: list[MerakiNetwork],
    previous_data: dict[str, Any],
    coordinator: Any,
) -> dict[str, Any]:
    """
    Parse and process network-level data.

    Args:
        detail_data: The raw detailed data from the API.
        networks: A list of Meraki networks.
        previous_data: The previous data from the coordinator.
        coordinator: The data update coordinator.

    Returns:
        A dictionary of processed network data.
    """
    appliance_traffic: dict[str, Any] = {}
    vlan_by_network: dict[str, Any] = {}
    l3_firewall_rules_by_network: dict[str, Any] = {}
    traffic_shaping_by_network: dict[str, Any] = {}
    vpn_status_by_network: dict[str, Any] = {}
    rf_profiles_by_network: dict[str, Any] = {}
    content_filtering_by_network: dict[str, Any] = {}

    for network in networks:
        if not isinstance(network, dict) or "id" not in network:
            continue

        network_id = network["id"]

        # Appliance Traffic
        network_traffic_key = f"traffic_{network_id}"
        network_traffic = detail_data.get(network_traffic_key)
        if isinstance(network_traffic, MerakiInformationalError):
            if "traffic analysis" in str(network_traffic).lower():
                if coordinator:
                    coordinator.add_network_status_message(
                        network_id,
                        "Traffic Analysis is not enabled for this network.",
                    )
                    coordinator.mark_traffic_check_done(network_id)
            appliance_traffic[network_id] = {
                "error": "disabled",
                "reason": str(network_traffic),
            }
        elif isinstance(network_traffic, dict):
            appliance_traffic[network_id] = network_traffic
        elif previous_data and network_traffic_key in previous_data:
            appliance_traffic[network_id] = previous_data[network_traffic_key]

        # VLANs
        network_vlans_key = f"vlans_{network_id}"
        network_vlans = detail_data.get(network_vlans_key)
        if isinstance(network_vlans, MerakiInformationalError):
            if "vlans are not enabled" in str(network_vlans).lower():
                if coordinator:
                    coordinator.add_network_status_message(
                        network_id,
                        "VLANs are not enabled for this network.",
                    )
                    coordinator.mark_vlan_check_done(network_id)
            vlan_by_network[network_id] = []
        elif isinstance(network_vlans, list):
            vlan_by_network[network_id] = network_vlans
        elif previous_data and network_vlans_key in previous_data:
            vlan_by_network[network_id] = previous_data[network_vlans_key]

        # L3 Firewall Rules
        l3_firewall_rules_key = f"l3_firewall_rules_{network_id}"
        l3_firewall_rules = detail_data.get(l3_firewall_rules_key)
        if isinstance(l3_firewall_rules, dict):
            l3_firewall_rules_by_network[network_id] = l3_firewall_rules
        elif previous_data and l3_firewall_rules_key in previous_data:
            l3_firewall_rules_by_network[network_id] = previous_data[
                l3_firewall_rules_key
            ]

        # Traffic Shaping
        traffic_shaping_key = f"traffic_shaping_{network_id}"
        traffic_shaping = detail_data.get(traffic_shaping_key)
        if isinstance(traffic_shaping, dict):
            traffic_shaping_by_network[network_id] = traffic_shaping
        elif previous_data and traffic_shaping_key in previous_data:
            traffic_shaping_by_network[network_id] = previous_data[
                traffic_shaping_key
            ]

        # VPN Status
        vpn_status_key = f"vpn_status_{network_id}"
        vpn_status = detail_data.get(vpn_status_key)
        if isinstance(vpn_status, dict):
            vpn_status_by_network[network_id] = vpn_status
        elif previous_data and vpn_status_key in previous_data:
            vpn_status_by_network[network_id] = previous_data[vpn_status_key]

        # RF Profiles
        network_rf_profiles_key = f"rf_profiles_{network['id']}"
        network_rf_profiles = detail_data.get(network_rf_profiles_key)
        if isinstance(network_rf_profiles, list):
            rf_profiles_by_network[network['id']] = network_rf_profiles
        elif previous_data and network_rf_profiles_key in previous_data:
            rf_profiles_by_network[network['id']] = previous_data[
                network_rf_profiles_key
            ]

        # Content Filtering
        content_filtering_key = f"content_filtering_{network_id}"
        content_filtering = detail_data.get(content_filtering_key)
        if isinstance(content_filtering, dict):
            content_filtering_by_network[network_id] = content_filtering
        elif previous_data and content_filtering_key in previous_data:
            content_filtering_by_network[network_id] = previous_data[
                content_filtering_key
            ]

    return {
        "appliance_traffic": appliance_traffic,
        "vlans": vlan_by_network,
        "l3_firewall_rules": l3_firewall_rules_by_network,
        "traffic_shaping": traffic_shaping_by_network,
        "vpn_status": vpn_status_by_network,
        "rf_profiles": rf_profiles_by_network,
        "content_filtering": content_filtering_by_network,
    }
