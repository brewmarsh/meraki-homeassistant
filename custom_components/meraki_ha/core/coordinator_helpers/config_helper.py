"""Configuration helper for the Meraki Coordinator."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry

from ...const_conf import (
    CONF_ENABLE_CAMERA_SENSE,
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VPN_MANAGEMENT,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_ENABLE_CAMERA_SENSE,
    DEFAULT_ENABLE_FIREWALL_RULES,
    DEFAULT_ENABLE_TRAFFIC_SHAPING,
    DEFAULT_ENABLE_VPN_MANAGEMENT,
    DEFAULT_SCAN_INTERVAL,
)


@dataclass
class CoordinatorConfig:
    """Configuration for the Meraki Coordinator."""

    api_key: str
    org_id: str
    scan_interval: int
    enable_vpn: bool
    enable_firewall: bool
    enable_traffic: bool
    enable_camera_sense: bool


def get_coordinator_config(entry: ConfigEntry) -> CoordinatorConfig:
    """Extract configuration from the config entry."""
    # Feature flags can be in either options (user-controlled)
    # or data (initial setup)
    enable_vpn = entry.options.get(
        CONF_ENABLE_VPN_MANAGEMENT,
        entry.data.get(CONF_ENABLE_VPN_MANAGEMENT, DEFAULT_ENABLE_VPN_MANAGEMENT),
    )
    enable_firewall = entry.options.get(
        CONF_ENABLE_FIREWALL_RULES,
        entry.data.get(CONF_ENABLE_FIREWALL_RULES, DEFAULT_ENABLE_FIREWALL_RULES),
    )
    enable_traffic = entry.options.get(
        CONF_ENABLE_TRAFFIC_SHAPING,
        entry.data.get(CONF_ENABLE_TRAFFIC_SHAPING, DEFAULT_ENABLE_TRAFFIC_SHAPING),
    )
    enable_camera_sense = entry.options.get(
        CONF_ENABLE_CAMERA_SENSE,
        entry.data.get(CONF_ENABLE_CAMERA_SENSE, DEFAULT_ENABLE_CAMERA_SENSE),
    )

    try:
        scan_interval = int(
            entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        if scan_interval <= 0:
            scan_interval = DEFAULT_SCAN_INTERVAL
    except (ValueError, TypeError):
        scan_interval = DEFAULT_SCAN_INTERVAL

    return CoordinatorConfig(
        api_key=entry.data[CONF_MERAKI_API_KEY],
        org_id=entry.data[CONF_MERAKI_ORG_ID],
        scan_interval=scan_interval,
        enable_vpn=enable_vpn,
        enable_firewall=enable_firewall,
        enable_traffic=enable_traffic,
        enable_camera_sense=enable_camera_sense,
    )
