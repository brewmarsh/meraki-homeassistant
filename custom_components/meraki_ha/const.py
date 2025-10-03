"""Constants for the Meraki Home Assistant integration.

This module defines constants used throughout the Meraki integration,
including domain names, configuration keys, default values, and platform types.
"""

from typing import Final, List

DOMAIN: Final[str] = "meraki_ha"
"""Domain for the component."""

MANUFACTURER: Final[str] = "Cisco Meraki"
"""Manufacturer for all Meraki devices."""

CONF_INTEGRATION_TITLE: Final[str] = "Meraki"
"""Title for the integration."""

CONF_MERAKI_API_KEY: Final[str] = "meraki_api_key"
"""Configuration key for the Meraki API key (str)."""

CONF_MERAKI_ORG_ID: Final[str] = "meraki_org_id"
"""Configuration key for the Meraki organization ID (str)."""

CONF_SCAN_INTERVAL: Final[str] = "scan_interval"
"""Configuration key for the scan interval in seconds (str)."""

DATA_CLIENT: Final[str] = "client"
"""Key for storing the Meraki API client in Home Assistant's data (str)."""

DATA_COORDINATOR: Final[str] = "coordinator"
"""Key for storing the Meraki data coordinator in Home Assistant's data (str)."""

DATA_COORDINATORS: Final[str] = (
    "coordinators"  # New constant for the coordinators dictionary
)
"""Key for storing the dictionary of all coordinators (str)."""

CONF_RTSP_STREAM_ENABLED: Final[str] = "rtsp_stream_enabled"
"""Configuration key for enabling RTSP stream on a camera (str)."""

CONF_ENABLE_DEVICE_TRACKER: Final[str] = "enable_device_tracker"
"""Configuration key for enabling device tracker (str)."""


CONF_IGNORED_NETWORKS: Final[str] = "ignored_networks"
"""Configuration key for a list of network names to ignore (str)."""

CONF_ENABLE_VLAN_MANAGEMENT: Final[str] = "enable_vlan_management"
"""Configuration key for enabling vlan management (str)."""


DEFAULT_IGNORED_NETWORKS: Final[str] = ""
"""Default value for the ignored networks list (str)."""

DEFAULT_ENABLE_VLAN_MANAGEMENT: Final[bool] = False
"""Default value for enabling vlan management (bool)."""

DATA_SSID_DEVICES_COORDINATOR: Final[str] = (
    "ssid_devices"  # New constant for SSID coordinator key
)
"""Key for storing the SSID devices coordinator within the coordinators dictionary (str)."""

MERAKI_API_CLIENT: Final[str] = "meraki_api_client"
"""Key for storing the MerakiAPIClient instance in hass.data (str)."""

DEFAULT_SCAN_INTERVAL: Final[int] = 300
"""Default scan interval in seconds for the Meraki API data (int)."""

# Platform types
PLATFORM_BINARY_SENSOR: Final[str] = "binary_sensor"
"""Represents the binary_sensor platform (str)."""
PLATFORM_BUTTON: Final[str] = "button"
"""Represents the button platform (str)."""
PLATFORM_SENSOR: Final[str] = "sensor"
"""Represents the sensor platform (str)."""
PLATFORM_DEVICE_TRACKER: Final[str] = "device_tracker"
"""Represents the device_tracker platform (str)."""
PLATFORM_DEVICE: Final[str] = (
    "device"  # Assuming this is a custom platform or future use
)
"""Represents a generic device platform (str)."""
PLATFORM_SWITCH: Final[str] = "switch"
"""Represents the switch platform (str)."""
PLATFORM_TEXT: Final[str] = "text"
"""Represents the text platform (str)."""
PLATFORM_CAMERA: Final[str] = "camera"
"""Represents the camera platform (str)."""

PLATFORMS: Final[List[str]] = [
    PLATFORM_SENSOR,
    PLATFORM_BINARY_SENSOR,
    PLATFORM_BUTTON,
    PLATFORM_SWITCH,
    PLATFORM_TEXT,
    PLATFORM_CAMERA,
]
"""List of platforms supported by the integration (List[str])."""

# Sensor types (examples, expand as needed)
SENSOR_CLIENT_COUNT: Final[str] = "client_count"
"""Sensor type for client count (str)."""
SENSOR_SIGNAL_STRENGTH: Final[str] = "signal_strength"
"""Sensor type for signal strength (str)."""
SENSOR_DATA_USAGE: Final[str] = "data_usage"
"""Sensor type for data usage (str)."""
SENSOR_SSID_AVAILABILITY: Final[str] = "ssid_availability"
"""Sensor type for SSID availability (str)."""
SENSOR_SSID_CHANNEL: Final[str] = "ssid_channel"
"""Sensor type for SSID channel (str)."""

# Device Attributes (examples, expand as needed)
ATTR_CONNECTED_CLIENTS: Final[str] = "connected_clients"
"""Device attribute for connected clients (str)."""
ATTR_SSIDS: Final[str] = "ssids"
"""Device attribute for SSIDs (str)."""

TAG_HA_DISABLED: Final[str] = "ha-disabled"
"""Tag used to indirectly disable an SSID on an access point."""

ERASE_TAGS_WARNING: Final[str] = (
    "Tag erasing is enabled! This will ERASE ALL TAGS on your Meraki devices. "
    "Proceed with extreme caution!"
)
"""Warning message for the tag erasing feature (str)."""

WEBHOOK_ID_FORMAT: Final[str] = "meraki_ha_{entry_id}"

MERAKI_CONTENT_FILTERING_CATEGORIES: Final[List[dict]] = [
    {
        "id": "meraki:contentFiltering/category/1",
        "name": "Adult and Pornography",
        "description": "Sites featuring sexual content, nudity, or pornography.",
    },
    {
        "id": "meraki:contentFiltering/category/2",
        "name": "Illegal",
        "description": "Sites promoting illegal activities, such as drug-making or hacking.",
    },
    {
        "id": "meraki:contentFiltering/category/3",
        "name": "Gambling",
        "description": "Online gambling sites, including casinos, sports betting, and lotteries.",
    },
    {
        "id": "meraki:contentFiltering/category/4",
        "name": "Hate and Racism",
        "description": "Sites promoting hatred, discrimination, or violence against individuals or groups.",
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
        "description": "Sites known to host or distribute malware, viruses, or other malicious software.",
    },
    {
        "id": "meraki:contentFiltering/category/9",
        "name": "Phishing and other frauds",
        "description": "Sites engaged in phishing, scams, or other fraudulent activities.",
    },
    {
        "id": "meraki:contentFiltering/category/10",
        "name": "Key loggers and monitoring",
        "description": "Sites for keyloggers, spyware, and other monitoring tools.",
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
