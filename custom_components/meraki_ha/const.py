"""
Constants for the Meraki Home Assistant integration.

This module defines constants used throughout the Meraki integration,
including domain names, configuration keys, default values, and platform types.
"""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "meraki_ha"
"""Domain for the component."""

MANUFACTURER: Final = "Cisco Meraki"
"""Manufacturer for all Meraki devices."""

CONF_INTEGRATION_TITLE: Final = "Meraki"
"""Title for the integration."""

CONF_MERAKI_API_KEY: Final = "meraki_api_key"
"""Configuration key for the Meraki API key."""

CONF_MERAKI_ORG_ID: Final = "meraki_org_id"
"""Configuration key for the Meraki organization ID."""

CONF_SCAN_INTERVAL: Final = "scan_interval"
"""Configuration key for the scan interval in seconds."""

CONF_SCAN_INTERVAL_DEVICE_STATUS: Final = "scan_interval_device_status"
"""Configuration key for the device status scan interval in seconds."""

CONF_SCAN_INTERVAL_CLIENTS: Final = "scan_interval_clients"
"""Configuration key for the clients scan interval in seconds."""

DATA_CLIENT: Final = "client"
"""Key for storing the Meraki API client in Home Assistant's data."""

DATA_COORDINATOR: Final = "coordinator"
"""Key for storing the Meraki data coordinator in Home Assistant's data."""

DATA_COORDINATORS: Final = "coordinators"
"""Key for storing the dictionary of all coordinators."""

CONF_IGNORED_NETWORKS: Final = "ignored_networks"
"""Configuration key for a list of network names to ignore."""

CONF_HIDE_UNCONFIGURED_SSIDS: Final = "hide_unconfigured_ssids"
"""Configuration key for hiding unconfigured SSIDs."""

CONF_RTSP_STREAM_ENABLED: Final = "rtsp_stream_enabled"
"""Configuration key for enabling RTSP stream on a camera."""

CONF_CAMERA_STREAM_SOURCE: Final = "camera_stream_source"
"""Configuration key for camera stream source (rtsp or cloud)."""

CONF_CAMERA_SNAPSHOT_INTERVAL: Final = "camera_snapshot_interval"
"""Configuration key for camera snapshot refresh interval in seconds."""

CAMERA_STREAM_SOURCE_RTSP: Final = "rtsp"
"""Use RTSP for camera streaming."""

CAMERA_STREAM_SOURCE_CLOUD: Final = "cloud"
"""Use cloud video link for camera streaming."""

DEFAULT_CAMERA_STREAM_SOURCE: Final = "rtsp"
"""Default camera stream source."""

DEFAULT_CAMERA_SNAPSHOT_INTERVAL: Final = 0
"""Default camera snapshot interval (0 = disabled)."""

CONF_CAMERA_ENTITY_MAPPINGS: Final = "camera_entity_mappings"
"""Configuration key for camera entity mappings (Meraki serial -> HA entity_id)."""

CONF_MQTT_RELAY_DESTINATIONS: Final = "mqtt_relay_destinations"
"""Configuration key for MQTT relay destinations."""

# Dashboard display settings
CONF_DASHBOARD_VIEW_MODE: Final = "dashboard_view_mode"
"""Configuration key for dashboard view mode (network or type)."""

CONF_DASHBOARD_DEVICE_TYPE_FILTER: Final = "dashboard_device_type_filter"
"""Configuration key for default device type filter on dashboard."""

CONF_DASHBOARD_STATUS_FILTER: Final = "dashboard_status_filter"
"""Configuration key for default device status filter on dashboard."""

CONF_CAMERA_LINK_INTEGRATION: Final = "camera_link_integration"
"""Configuration key for which integration to filter cameras for linking."""

# Dashboard defaults
DASHBOARD_VIEW_MODE_NETWORK: Final = "network"
"""View devices grouped by network."""

DASHBOARD_VIEW_MODE_TYPE: Final = "type"
"""View devices grouped by device type."""

DEFAULT_DASHBOARD_VIEW_MODE: Final = "network"
"""Default dashboard view mode."""

DEFAULT_DASHBOARD_DEVICE_TYPE_FILTER: Final = "all"
"""Default device type filter (all = no filter)."""

DEFAULT_DASHBOARD_STATUS_FILTER: Final = "all"
"""Default device status filter (all = no filter)."""

DEFAULT_CAMERA_LINK_INTEGRATION: Final = ""
"""Default camera link integration (empty = show all cameras)."""

CONF_TEMPERATURE_UNIT: Final = "temperature_unit"
"""Configuration key for temperature unit preference."""

TEMPERATURE_UNIT_CELSIUS: Final = "celsius"
"""Use Celsius for temperature readings."""

TEMPERATURE_UNIT_FAHRENHEIT: Final = "fahrenheit"
"""Use Fahrenheit for temperature readings."""

DEFAULT_TEMPERATURE_UNIT: Final = TEMPERATURE_UNIT_CELSIUS
"""Default temperature unit (Celsius)."""

CONF_ENABLE_DEVICE_TRACKER: Final = "enable_device_tracker"
"""Configuration key for enabling device tracker."""

CONF_ENABLE_VLAN_MANAGEMENT: Final = "enable_vlan_management"
"""Configuration key for enabling vlan management."""

CONF_ENABLED_NETWORKS: Final = "enabled_networks"
"""Configuration key for a list of network IDs to enable."""

# New Configuration Options
CONF_ENABLE_DEVICE_STATUS: Final = "enable_device_status"
CONF_ENABLE_ORG_SENSORS: Final = "enable_org_sensors"
CONF_ENABLE_CAMERA_ENTITIES: Final = "enable_camera_entities"
CONF_ENABLE_DEVICE_SENSORS: Final = "enable_device_sensors"
CONF_ENABLE_NETWORK_SENSORS: Final = "enable_network_sensors"
CONF_ENABLE_VLAN_SENSORS: Final = "enable_vlan_sensors"
CONF_ENABLE_PORT_SENSORS: Final = "enable_port_sensors"
CONF_ENABLE_SSID_SENSORS: Final = "enable_ssid_sensors"

DEFAULT_ENABLED_NETWORKS: Final[list[str]] = []
"""Default value for the ignored networks list."""

DEFAULT_ENABLE_VLAN_MANAGEMENT: Final = False
"""Default value for enabling vlan management."""

DEFAULT_IGNORED_NETWORKS: Final = ""
"""Default value for the ignored networks list."""

DEFAULT_HIDE_UNCONFIGURED_SSIDS: Final = False
"""Default value for hiding unconfigured SSIDs."""

DATA_SSID_DEVICES_COORDINATOR: Final = "ssid_devices"
"""Key for the SSID devices coordinator."""

MERAKI_API_CLIENT: Final = "meraki_api_client"
"""Key for storing the MerakiAPIClient instance in hass.data."""

DEFAULT_SCAN_INTERVAL: Final = 90
"""Default scan interval in seconds for the Meraki API data."""

DEFAULT_SCAN_INTERVAL_DEVICE_STATUS: Final = 60
"""Default scan interval in seconds for device status."""

DEFAULT_SCAN_INTERVAL_CLIENTS: Final = 120
"""Default scan interval in seconds for clients."""


# Defaults for new options
DEFAULT_ENABLE_DEVICE_STATUS: Final = True
DEFAULT_ENABLE_ORG_SENSORS: Final = True
DEFAULT_ENABLE_CAMERA_ENTITIES: Final = True
DEFAULT_ENABLE_DEVICE_SENSORS: Final = True
DEFAULT_ENABLE_NETWORK_SENSORS: Final = True
DEFAULT_ENABLE_VLAN_SENSORS: Final = True
DEFAULT_ENABLE_PORT_SENSORS: Final = True
DEFAULT_ENABLE_SSID_SENSORS: Final = True

CONF_ENABLE_WEB_UI: Final = "enable_web_ui"
DEFAULT_ENABLE_WEB_UI: Final = False
CONF_WEB_UI_PORT: Final = "web_ui_port"
DEFAULT_WEB_UI_PORT: Final = 9000

# Platform types
PLATFORM_BINARY_SENSOR: Final = "binary_sensor"
"""Represents the binary_sensor platform."""
PLATFORM_BUTTON: Final = "button"
"""Represents the button platform."""
PLATFORM_SENSOR: Final = "sensor"
"""Represents the sensor platform."""
PLATFORM_DEVICE_TRACKER: Final = "device_tracker"
"""Represents the device_tracker platform."""
PLATFORM_DEVICE: Final = "device"
"""Represents a generic device platform."""
PLATFORM_SWITCH: Final = "switch"
"""Represents the switch platform."""
PLATFORM_TEXT: Final = "text"
"""Represents the text platform."""
PLATFORM_CAMERA: Final = "camera"
"""Represents the camera platform."""
PLATFORM_NUMBER: Final = "number"
"""Represents the number platform."""

PLATFORMS: Final = [
    PLATFORM_SENSOR,
    PLATFORM_BINARY_SENSOR,
    PLATFORM_BUTTON,
    PLATFORM_SWITCH,
    PLATFORM_TEXT,
    PLATFORM_CAMERA,
    PLATFORM_NUMBER,
]
"""List of platforms supported by the integration."""

# Sensor types (examples, expand as needed)
SENSOR_CLIENT_COUNT: Final = "client_count"
"""Sensor type for client count."""
SENSOR_SIGNAL_STRENGTH: Final = "signal_strength"
"""Sensor type for signal strength."""
SENSOR_DATA_USAGE: Final = "data_usage"
"""Sensor type for data usage."""
SENSOR_SSID_AVAILABILITY: Final = "ssid_availability"
"""Sensor type for SSID availability."""
SENSOR_SSID_CHANNEL: Final = "ssid_channel"
"""Sensor type for SSID channel."""

# Device Attributes (examples, expand as needed)
ATTR_CONNECTED_CLIENTS: Final = "connected_clients"
"""Device attribute for connected clients."""
ATTR_SSIDS: Final = "ssids"
"""Device attribute for SSIDs."""

TAG_HA_DISABLED: Final = "ha-disabled"
"""Tag used to indirectly disable an SSID on an access point."""

# Device name format options
DEVICE_NAME_FORMAT_PREFIX: Final = "prefix"
"""Format device name with type prefix."""
DEVICE_NAME_FORMAT_SUFFIX: Final = "suffix"
"""Format device name with type suffix."""
DEVICE_NAME_FORMAT_NONE: Final = "none"
"""Do not format device name."""

ERASE_TAGS_WARNING: Final = (
    "Tag erasing is enabled! This will ERASE ALL TAGS on your Meraki devices. "
    "Proceed with extreme caution!"
)
"""Warning message for the tag erasing feature."""

WEBHOOK_ID_FORMAT: Final = "meraki_ha_{entry_id}"

MERAKI_CONTENT_FILTERING_CATEGORIES: Final[list[dict[str, str]]] = [
    {
        "id": "meraki:contentFiltering/category/1",
        "name": "Adult and Pornography",
        "description": "Sites featuring sexual content, nudity, or pornography.",
    },
    {
        "id": "meraki:contentFiltering/category/2",
        "name": "Illegal",
        "description": "Sites promoting illegal activities.",
    },
    {
        "id": "meraki:contentFiltering/category/3",
        "name": "Gambling",
        "description": "Online gambling sites.",
    },
    {
        "id": "meraki:contentFiltering/category/4",
        "name": "Hate and Racism",
        "description": "Sites promoting hatred or discrimination.",
    },
    {
        "id": "meraki:contentFiltering/category/5",
        "name": "Weapons",
        "description": "Sites related to the sale or promotion of weapons.",
    },
    {
        "id": "meraki:contentFiltering/category/6",
        "name": "Violence",
        "description": "Sites with graphic or gratuitous violence.",
    },
    {
        "id": "meraki:contentFiltering/category/7",
        "name": "Peer-to-peer",
        "description": "Peer-to-peer file sharing sites and applications.",
    },
    {
        "id": "meraki:contentFiltering/category/8",
        "name": "Malware sites",
        "description": "Sites known to host or distribute malware.",
    },
    {
        "id": "meraki:contentFiltering/category/9",
        "name": "Phishing and other frauds",
        "description": "Sites engaged in phishing, scams, or other frauds.",
    },
    {
        "id": "meraki:contentFiltering/category/10",
        "name": "Key loggers and monitoring",
        "description": "Sites for keyloggers, spyware, and monitoring tools.",
    },
    {
        "id": "meraki:contentFiltering/category/11",
        "name": "Botnets",
        "description": "Sites associated with botnet command and control servers.",
    },
    {
        "id": "meraki:contentFiltering/category/12",
        "name": "Spam URLs",
        "description": "URLs frequently found in unsolicited email (spam).",
    },
    {
        "id": "meraki:contentFiltering/category/13",
        "name": "Auctions",
        "description": "Online auction sites.",
    },
    {
        "id": "meraki:contentFiltering/category/14",
        "name": "Games",
        "description": "Online gaming sites.",
    },
    {
        "id": "meraki:contentFiltering/category/15",
        "name": "Social Networking",
        "description": "Social networking sites and applications.",
    },
    {
        "id": "meraki:contentFiltering/category/16",
        "name": "Web-based email",
        "description": "Web-based email services.",
    },
    {
        "id": "meraki:contentFiltering/category/17",
        "name": "Internet communications",
        "description": "Chat, instant messaging, and other communication platforms.",
    },
    {
        "id": "meraki:contentFiltering/category/18",
        "name": "Shareware and freeware",
        "description": "Sites for downloading shareware and freeware.",
    },
    {
        "id": "meraki:contentFiltering/category/19",
        "name": "Web advertisements",
        "description": "Sites primarily serving advertisements.",
    },
    {
        "id": "meraki:contentFiltering/category/20",
        "name": "Nudity",
        "description": "Sites with non-pornographic nudity.",
    },
]
