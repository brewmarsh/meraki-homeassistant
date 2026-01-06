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

<<<<<<< HEAD
<<<<<<< HEAD
CONF_ENABLE_WEB_UI: Final = "enable_web_ui"
"""Configuration key for enabling the web UI."""

CONF_WEB_UI_PORT: Final = "web_ui_port"
"""Configuration key for the web UI port."""

=======
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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

CONF_ENABLE_DEVICE_TRACKER: Final = "enable_device_tracker"
"""Configuration key for enabling device tracker."""

<<<<<<< HEAD
<<<<<<< HEAD

CONF_ENABLE_VLAN_MANAGEMENT: Final = "enable_vlan_management"
"""Configuration key for enabling vlan management."""


CONF_ENABLED_NETWORKS: Final = "enabled_networks"
"""Configuration key for a list of network IDs to enable."""

=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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

<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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

DEFAULT_SCAN_INTERVAL: Final = 300
"""Default scan interval in seconds for the Meraki API data."""

<<<<<<< HEAD
<<<<<<< HEAD
DEFAULT_ENABLE_WEB_UI: Final = False
"""Default value for enabling the web UI."""

DEFAULT_WEB_UI_PORT: Final = 8080
"""Default scan interval in seconds for the Meraki API data."""
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
# Defaults for new options
DEFAULT_ENABLE_DEVICE_STATUS: Final = True
DEFAULT_ENABLE_ORG_SENSORS: Final = True
DEFAULT_ENABLE_CAMERA_ENTITIES: Final = True
DEFAULT_ENABLE_DEVICE_SENSORS: Final = True
DEFAULT_ENABLE_NETWORK_SENSORS: Final = True
DEFAULT_ENABLE_VLAN_SENSORS: Final = True
DEFAULT_ENABLE_PORT_SENSORS: Final = True
DEFAULT_ENABLE_SSID_SENSORS: Final = True

<<<<<<< HEAD
CONF_ENABLE_WEB_UI: Final = "enable_web_ui"
DEFAULT_ENABLE_WEB_UI: Final = False
CONF_WEB_UI_PORT: Final = "web_ui_port"
DEFAULT_WEB_UI_PORT: Final = 9000
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668

=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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

ERASE_TAGS_WARNING: Final = (
    "Tag erasing is enabled! This will ERASE ALL TAGS on your Meraki devices. "
    "Proceed with extreme caution!"
)
"""Warning message for the tag erasing feature."""

<<<<<<< HEAD
<<<<<<< HEAD
=======
DEVICE_NAME_FORMAT_PREFIX: Final = "prefix"
DEVICE_NAME_FORMAT_SUFFIX: Final = "suffix"

>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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
