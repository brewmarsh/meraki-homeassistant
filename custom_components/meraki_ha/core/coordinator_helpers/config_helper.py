"""Configuration helper for the Meraki HA coordinator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry

from ...const_conf import (
    CONF_ENABLE_CAMERA_SENSE,
    CONF_ENABLE_FIREWALL_RULES,
    CONF_ENABLE_TRAFFIC_SHAPING,
    CONF_ENABLE_VPN_MANAGEMENT,
    CONF_IGNORED_NETWORKS,
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    DEFAULT_ENABLE_CAMERA_SENSE,
    DEFAULT_ENABLE_FIREWALL_RULES,
    DEFAULT_ENABLE_TRAFFIC_SHAPING,
    DEFAULT_ENABLE_VPN_MANAGEMENT,
    DEFAULT_IGNORED_NETWORKS,
    DEFAULT_SCAN_INTERVAL,
)


@dataclass
class CoordinatorConfig:
    """Configuration for the Meraki coordinator."""

    api_key: str
    org_id: str
    enable_vpn: bool
    enable_firewall: bool
    enable_traffic: bool
    enable_camera_sense: bool
    scan_interval: int
    update_interval: timedelta
    ignored_networks: list[str]


def get_coordinator_config(entry: ConfigEntry) -> CoordinatorConfig:
    """Extract configuration from the config entry."""
    api_key: str = entry.data[CONF_MERAKI_API_KEY]
    org_id: str = entry.data[CONF_MERAKI_ORG_ID]

    # Feature flags can be in either options (user-controlled)
    # or data (initial setup)
    enable_vpn: bool = entry.options.get(
        CONF_ENABLE_VPN_MANAGEMENT,
        entry.data.get(CONF_ENABLE_VPN_MANAGEMENT, DEFAULT_ENABLE_VPN_MANAGEMENT),
    )
    enable_firewall: bool = entry.options.get(
        CONF_ENABLE_FIREWALL_RULES,
        entry.data.get(CONF_ENABLE_FIREWALL_RULES, DEFAULT_ENABLE_FIREWALL_RULES),
    )
    enable_traffic: bool = entry.options.get(
        CONF_ENABLE_TRAFFIC_SHAPING,
        entry.data.get(CONF_ENABLE_TRAFFIC_SHAPING, DEFAULT_ENABLE_TRAFFIC_SHAPING),
    )
    enable_camera_sense: bool = entry.options.get(
        CONF_ENABLE_CAMERA_SENSE,
        entry.data.get(CONF_ENABLE_CAMERA_SENSE, DEFAULT_ENABLE_CAMERA_SENSE),
    )
    ignored_networks: list[str] = entry.options.get(
        CONF_IGNORED_NETWORKS,
        DEFAULT_IGNORED_NETWORKS,
    )

    try:
        scan_interval = int(
            entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        if scan_interval <= 0:
            scan_interval = DEFAULT_SCAN_INTERVAL
    except (ValueError, TypeError):
        scan_interval = DEFAULT_SCAN_INTERVAL

    update_interval = timedelta(seconds=scan_interval)

    return CoordinatorConfig(
        api_key=api_key,
        org_id=org_id,
        enable_vpn=enable_vpn,
        enable_firewall=enable_firewall,
        enable_traffic=enable_traffic,
        enable_camera_sense=enable_camera_sense,
        scan_interval=scan_interval,
        update_interval=update_interval,
        ignored_networks=ignored_networks,
    )
