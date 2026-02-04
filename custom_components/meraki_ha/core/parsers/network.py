"""Parsers for Meraki network data."""

from __future__ import annotations

import logging
from typing import Any

from ...core.errors import (
    MerakiInformationalError,
    MerakiTrafficAnalysisError,
    MerakiVlanError,
    MerakiVlansDisabledError,
)
from ...core.models.network import (
    MerakiFirewallRule,
    MerakiNetwork,
    MerakiTrafficShaping,
    MerakiVlan,
    MerakiVpn,
)

_LOGGER = logging.getLogger(__name__)


def parse_network_data(
    detail_data: dict[str, Any],
    networks: list[MerakiNetwork],
    previous_data: dict[str, Any],
    disabled_features: set[str],
) -> dict[str, Any]:
    """
    Parse and process network-level data.

    Args:
        detail_data: The raw detailed data from the API.
        networks: A list of Meraki networks.
        previous_data: The previous data from the coordinator.
        disabled_features: A set of disabled features to update.

    Returns
    -------
        A dictionary of processed network data.

    """
    appliance_traffic: dict[str, Any] = {}
    vlan_by_network: dict[str, list[MerakiVlan]] = {}
    l3_firewall_rules_by_network: dict[str, list[MerakiFirewallRule]] = {}
    traffic_shaping_by_network: dict[str, MerakiTrafficShaping] = {}
    vpn_status_by_network: dict[str, MerakiVpn] = {}
    rf_profiles_by_network: dict[str, Any] = {}
    content_filtering_by_network: dict[str, Any] = {}

    for network in networks:
        if not network.id:
            continue
        network_id = str(network.id)

        # Initialize with empty lists to prevent KeyErrors
        vlan_by_network[network_id] = []

        _parse_traffic(
            network_id,
            detail_data,
            previous_data,
            disabled_features,
            appliance_traffic,
        )

        _parse_vlans(
            network_id,
            detail_data,
            previous_data,
            disabled_features,
            vlan_by_network,
        )

        _parse_firewall_rules(
            network_id,
            detail_data,
            previous_data,
            l3_firewall_rules_by_network,
        )

        _parse_traffic_shaping(
            network_id,
            detail_data,
            previous_data,
            traffic_shaping_by_network,
        )

        _parse_vpn_status(
            network_id,
            detail_data,
            previous_data,
            vpn_status_by_network,
        )

        _parse_rf_profiles(
            network_id,
            detail_data,
            previous_data,
            rf_profiles_by_network,
        )

        _parse_content_filtering(
            network_id,
            detail_data,
            previous_data,
            content_filtering_by_network,
        )

    return {
        "appliance_traffic": appliance_traffic,
        "vlans": vlan_by_network,
        "l3_firewall_rules": l3_firewall_rules_by_network,
        "traffic_shaping": traffic_shaping_by_network,
        "vpn_status": vpn_status_by_network,
        "rf_profiles": rf_profiles_by_network,
        "content_filtering": content_filtering_by_network,
    }


def _parse_traffic(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
    disabled_features: set[str],
    appliance_traffic: dict[str, Any],
) -> None:
    """Parse appliance traffic data."""
    key = f"traffic_{network_id}"
    data = detail_data.get(key)
    if isinstance(data, MerakiTrafficAnalysisError):
        disabled_features.add(key)
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


def _parse_vlans(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
    disabled_features: set[str],
    vlan_by_network: dict[str, list[MerakiVlan]],
) -> None:
    """Parse VLAN data."""
    key = f"vlans_{network_id}"
    data = detail_data.get(key)

    if isinstance(data, (MerakiVlanError, MerakiVlansDisabledError)):
        disabled_features.add(key)
        _LOGGER.info(str(data))
        vlan_by_network[network_id] = []
    elif isinstance(data, MerakiInformationalError):
        if "vlans are not enabled" in str(data).lower():
            disabled_features.add(key)
            vlan_by_network[network_id] = []
    elif isinstance(data, list):
        vlan_by_network[network_id] = [MerakiVlan.from_dict(v) for v in data]
    elif previous_data and "vlans" in previous_data:
        prev_vlans = previous_data["vlans"].get(network_id)
        if prev_vlans:
            vlan_by_network[network_id] = prev_vlans


def _parse_firewall_rules(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
    l3_firewall_rules_by_network: dict[str, list[MerakiFirewallRule]],
) -> None:
    """Parse L3 Firewall Rules."""
    key = f"l3_firewall_rules_{network_id}"
    data = detail_data.get(key)
    if isinstance(data, dict):
        rules = data.get("rules", [])
        l3_firewall_rules_by_network[network_id] = [
            MerakiFirewallRule.from_dict(r) for r in rules
        ]
    elif previous_data and "l3_firewall_rules" in previous_data:
        prev_rules = previous_data["l3_firewall_rules"].get(network_id)
        if prev_rules:
            l3_firewall_rules_by_network[network_id] = prev_rules


def _parse_traffic_shaping(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
    traffic_shaping_by_network: dict[str, MerakiTrafficShaping],
) -> None:
    """Parse Traffic Shaping settings."""
    key = f"traffic_shaping_{network_id}"
    data = detail_data.get(key)
    if isinstance(data, dict):
        traffic_shaping_by_network[network_id] = MerakiTrafficShaping.from_dict(data)
    elif previous_data and "traffic_shaping" in previous_data:
        prev_shaping = previous_data["traffic_shaping"].get(network_id)
        if prev_shaping:
            traffic_shaping_by_network[network_id] = prev_shaping


def _parse_vpn_status(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
    vpn_status_by_network: dict[str, MerakiVpn],
) -> None:
    """Parse VPN Status."""
    key = f"vpn_status_{network_id}"
    data = detail_data.get(key)
    if isinstance(data, dict):
        vpn_status_by_network[network_id] = MerakiVpn.from_dict(data)
    elif previous_data and "vpn_status" in previous_data:
        prev_vpn = previous_data["vpn_status"].get(network_id)
        if prev_vpn:
            vpn_status_by_network[network_id] = prev_vpn


def _parse_rf_profiles(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
    rf_profiles_by_network: dict[str, Any],
) -> None:
    """Parse RF Profiles."""
    key = f"rf_profiles_{network_id}"
    data = detail_data.get(key)
    if isinstance(data, list):
        rf_profiles_by_network[network_id] = data
    elif previous_data and key in previous_data:
        rf_profiles_by_network[network_id] = previous_data[key]


def _parse_content_filtering(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
    content_filtering_by_network: dict[str, Any],
) -> None:
    """Parse Content Filtering settings."""
    key = f"content_filtering_{network_id}"
    data = detail_data.get(key)
    if isinstance(data, dict):
        content_filtering_by_network[network_id] = data
    elif previous_data and key in previous_data:
        content_filtering_by_network[network_id] = previous_data[key]
