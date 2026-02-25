"""Parsers for Meraki network data."""

from __future__ import annotations

import logging
from typing import Any

from ...core.models.network import (
    MerakiFirewallRule,
    MerakiNetwork,
    MerakiTrafficShaping,
    MerakiVlan,
    MerakiVpn,
)
from ..errors import (
    MerakiInformationalError,
    MerakiTrafficAnalysisError,
    MerakiVlanError,
    MerakiVlansDisabledError,
)

_LOGGER = logging.getLogger(__name__)


def parse_network_data(
    detail_data: dict[str, Any],
    networks: list[MerakiNetwork],
    previous_data: dict[str, Any],
    disabled_features: set[str],
) -> dict[str, Any]:
    """Parse and process network-level data."""
    network_ids = [str(n.id) for n in networks if n.id]

    return {
        "appliance_traffic": {
            nid: data
            for nid in network_ids
            if (
                data := _extract_appliance_traffic(
                    nid, detail_data, previous_data, disabled_features
                )
            )
            is not None
        },
        "vlans": {
            nid: data
            for nid in network_ids
            if (
                data := _extract_vlans(
                    nid, detail_data, previous_data, disabled_features
                )
            )
            is not None
        },
        "l3_firewall_rules": {
            nid: data
            for nid in network_ids
            if (data := _extract_firewall_rules(nid, detail_data, previous_data))
            is not None
        },
        "traffic_shaping": {
            nid: data
            for nid in network_ids
            if (data := _extract_traffic_shaping(nid, detail_data, previous_data))
            is not None
        },
        "vpn_status": {
            nid: data
            for nid in network_ids
            if (data := _extract_vpn_status(nid, detail_data, previous_data)) is not None
        },
        "rf_profiles": {
            nid: data
            for nid in network_ids
            if (data := _extract_rf_profiles(nid, detail_data, previous_data))
            is not None
        },
        "content_filtering": {
            nid: data
            for nid in network_ids
            if (data := _extract_content_filtering(nid, detail_data, previous_data))
            is not None
        },
    }


def _extract_appliance_traffic(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
    disabled_features: set[str],
) -> dict[str, Any] | None:
    """Extract appliance traffic data."""
    key = f"traffic_{network_id}"
    data = detail_data.get(key)

    if isinstance(data, (MerakiTrafficAnalysisError, MerakiInformationalError)):
        disabled_features.add(key)
        return {"error": "disabled", "reason": str(data)}

    if isinstance(data, dict):
        return data

    if previous_data and key in previous_data:
        return previous_data[key]

    return None


def _extract_vlans(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
    disabled_features: set[str],
) -> list[MerakiVlan] | None:
    """Extract VLAN data with fallback support."""
    key = f"vlans_{network_id}"
    data = detail_data.get(key)

    if isinstance(data, (MerakiVlanError, MerakiVlansDisabledError)):
        disabled_features.add(key)
        return []

    if isinstance(data, MerakiInformationalError):
        if "vlans are not enabled" in str(data).lower():
            disabled_features.add(key)
            return []

    if isinstance(data, list):
        return [MerakiVlan.from_dict(v) for v in data]

    if isinstance(data, dict):
        # Fallback: search dictionary values for the list
        for value in data.values():
            if isinstance(value, list):
                return [MerakiVlan.from_dict(v) for v in value if isinstance(v, dict)]

    if previous_data and "vlans" in previous_data:
        return previous_data["vlans"].get(network_id)

    return None


def _extract_firewall_rules(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
) -> list[MerakiFirewallRule] | None:
    """Extract L3 Firewall Rules."""
    key = f"l3_firewall_rules_{network_id}"
    data = detail_data.get(key)

    if isinstance(data, dict):
        rules = data.get("rules", [])
        return [MerakiFirewallRule.from_dict(r) for r in rules]

    if previous_data and "l3_firewall_rules" in previous_data:
        return previous_data["l3_firewall_rules"].get(network_id)

    return None


def _extract_traffic_shaping(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
) -> MerakiTrafficShaping | None:
    """Extract Traffic Shaping settings."""
    key = f"traffic_shaping_{network_id}"
    data = detail_data.get(key)

    if isinstance(data, dict):
        return MerakiTrafficShaping.from_dict(data)

    if previous_data and "traffic_shaping" in previous_data:
        return previous_data["traffic_shaping"].get(network_id)

    return None


def _extract_vpn_status(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
) -> MerakiVpn | None:
    """Extract VPN Status."""
    key = f"vpn_status_{network_id}"
    data = detail_data.get(key)

    if isinstance(data, dict):
        return MerakiVpn.from_dict(data)

    if previous_data and "vpn_status" in previous_data:
        return previous_data["vpn_status"].get(network_id)

    return None


def _extract_rf_profiles(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
) -> list[dict[str, Any]] | None:
    """Extract RF Profiles."""
    key = f"rf_profiles_{network_id}"
    data = detail_data.get(key)

    if isinstance(data, list):
        return data

    if previous_data and key in previous_data:
        return previous_data[key]

    return None


def _extract_content_filtering(
    network_id: str,
    detail_data: dict[str, Any],
    previous_data: dict[str, Any],
) -> dict[str, Any] | None:
    """Extract Content Filtering settings."""
    key = f"content_filtering_{network_id}"
    data = detail_data.get(key)

    if isinstance(data, dict):
        return data

    if previous_data and key in previous_data:
        return previous_data[key]

    return None
