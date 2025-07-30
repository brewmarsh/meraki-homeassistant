"""Constants for the Meraki Home Assistant integration.

This module defines constants used throughout the Meraki integration,
including domain names, configuration keys, default values, and platform types.
"""

from typing import Final, List

DOMAIN: Final[str] = "meraki_ha"
"""Domain for the component."""

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

CONF_WEBHOOK_URL: Final[str] = "webhook_url"
"""Configuration key for the external webhook URL (str)."""

DEFAULT_WEBHOOK_URL: Final[str] = ""
"""Default webhook URL value (empty string)."""

DATA_SSID_DEVICES_COORDINATOR: Final[str] = (
    "ssid_devices"  # New constant for SSID coordinator key
)
"""Key for storing the SSID devices coordinator within the coordinators dictionary (str)."""

MERAKI_API_CLIENT: Final[str] = "meraki_api_client"
"""Key for storing the MerakiAPIClient instance in hass.data (str)."""

DEFAULT_SCAN_INTERVAL: Final[int] = 300
"""Default scan interval in seconds for the Meraki API data (int)."""

# Platform types
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


PLATFORMS: Final[List[str]] = [
    PLATFORM_SENSOR,
    PLATFORM_DEVICE_TRACKER,
    PLATFORM_SWITCH,
    PLATFORM_TEXT,
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

# Configuration options
CONF_DEVICE_NAME_FORMAT: Final[str] = "device_name_format"
"""Configuration key for the device name format (str)."""

DEVICE_NAME_FORMAT_PREFIX: Final[str] = "prefix"
"""Device name format option: prefix (str)."""
DEVICE_NAME_FORMAT_SUFFIX: Final[str] = "suffix"
"""Device name format option: suffix (str)."""
DEVICE_NAME_FORMAT_OMIT: Final[str] = "omit"
"""Device name format option: omit (str)."""

DEVICE_NAME_FORMAT_OPTIONS: Final[List[str]] = [
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
    DEVICE_NAME_FORMAT_OMIT,
]
"""List of device name format options (List[str])."""

DEFAULT_DEVICE_NAME_FORMAT: Final[str] = DEVICE_NAME_FORMAT_PREFIX
"""Default device name format (str)."""
# CONF_RELAXED_TAG_MATCHING was removed as the feature was removed.

ERASE_TAGS_WARNING: Final[str] = (
    "Tag erasing is enabled! This will ERASE ALL TAGS on your Meraki devices. "
    "Proceed with extreme caution!"
)
"""Warning message for the tag erasing feature (str)."""

WEBHOOK_ID_FORMAT: Final[str] = "meraki_ha_{entry_id}"
