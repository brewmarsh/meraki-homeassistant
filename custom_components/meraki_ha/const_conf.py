"""Configuration constants for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Final

CONF_INTEGRATION_TITLE: Final = "Meraki"
"""Title for the integration."""

CONF_MERAKI_API_KEY: Final = "meraki_api_key"
"""Configuration key for the Meraki API key."""

CONF_MERAKI_ORG_ID: Final = "meraki_org_id"
"""Configuration key for the Meraki organization ID."""

CONF_SCAN_INTERVAL: Final = "scan_interval"
"""Configuration key for the scan interval in seconds."""

CONF_IGNORED_NETWORKS: Final = "ignored_networks"
"""Configuration key for a list of network names to ignore."""

CONF_ENABLED_NETWORKS: Final = "enabled_networks"
"""Configuration key for a list of network names to enable."""

CONF_HIDE_UNCONFIGURED_SSIDS: Final = "hide_unconfigured_ssids"
"""Configuration key for hiding unconfigured SSIDs."""

CONF_RTSP_STREAM_ENABLED: Final = "rtsp_stream_enabled"
"""Configuration key for enabling RTSP stream on a camera."""

CONF_ENABLE_DEVICE_TRACKER: Final = "enable_device_tracker"
"""Configuration key for enabling device tracker."""

CONF_ENABLE_VLAN_MANAGEMENT: Final = "enable_vlan_management"
"""Configuration key for enabling vlan management."""

CONF_ENABLE_VPN_MANAGEMENT: Final = "enable_vpn_management"
"""Configuration key for enabling VPN management."""

CONF_ENABLE_FIREWALL_RULES: Final = "enable_firewall_rules"
"""Configuration key for enabling firewall rules."""

CONF_ENABLE_TRAFFIC_SHAPING: Final = "enable_traffic_shaping"
"""Configuration key for enabling traffic shaping."""

# New Configuration Options
CONF_ENABLE_DEVICE_STATUS: Final = "enable_device_status"
CONF_ENABLE_ORG_SENSORS: Final = "enable_org_sensors"
CONF_ENABLE_CAMERA_ENTITIES: Final = "enable_camera_entities"
CONF_ENABLE_DEVICE_SENSORS: Final = "enable_device_sensors"
CONF_ENABLE_NETWORK_SENSORS: Final = "enable_network_sensors"
CONF_ENABLE_VLAN_SENSORS: Final = "enable_vlan_sensors"
CONF_ENABLE_PORT_SENSORS: Final = "enable_port_sensors"
CONF_ENABLE_SSID_SENSORS: Final = "enable_ssid_sensors"
CONF_ENABLE_CAMERA_SENSE: Final = "enable_camera_sense"

DEFAULT_ENABLED_NETWORKS: Final[list[str]] = []
"""Default value for the enabled networks list."""

DEFAULT_IGNORED_NETWORKS: Final[list[str]] = []
"""Default value for the ignored networks list."""

DEFAULT_ENABLE_VLAN_MANAGEMENT: Final = False
"""Default value for enabling vlan management."""

DEFAULT_ENABLE_VPN_MANAGEMENT: Final = False
"""Default value for enabling VPN management."""

DEFAULT_ENABLE_FIREWALL_RULES: Final = False
"""Default value for enabling firewall rules."""

DEFAULT_ENABLE_TRAFFIC_SHAPING: Final = False
"""Default value for enabling traffic shaping."""

DEFAULT_HIDE_UNCONFIGURED_SSIDS: Final = False
"""Default value for hiding unconfigured SSIDs."""

DEFAULT_SCAN_INTERVAL: Final = 300
"""Default scan interval in seconds for the Meraki API data."""

# Defaults for new options
DEFAULT_ENABLE_DEVICE_STATUS: Final = True
DEFAULT_ENABLE_ORG_SENSORS: Final = True
DEFAULT_ENABLE_CAMERA_ENTITIES: Final = True
DEFAULT_ENABLE_DEVICE_SENSORS: Final = True
DEFAULT_ENABLE_NETWORK_SENSORS: Final = True
DEFAULT_ENABLE_VLAN_SENSORS: Final = True
DEFAULT_ENABLE_PORT_SENSORS: Final = True
DEFAULT_ENABLE_SSID_SENSORS: Final = True
DEFAULT_ENABLE_CAMERA_SENSE: Final = True
