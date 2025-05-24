"""Constants for the Meraki Home Assistant integration.

This module defines constants used throughout the Meraki integration,
including domain names, configuration keys, data storage keys, default values,
platform types, sensor types, attribute names, and other configuration-related
strings.
"""

# Core Integration Constants
DOMAIN: str = "meraki_ha"
"""The domain of this integration, used as a unique identifier in Home Assistant."""

# Configuration Keys used in config_flow.py and for storing settings.
CONF_MERAKI_API_KEY: str = "meraki_api_key"
"""Configuration key for storing the Meraki API key."""

CONF_MERAKI_ORG_ID: str = "meraki_org_id"
"""Configuration key for storing the Meraki Organization ID."""

CONF_RELAXED_TAG_MATCHING: str = "relaxed_tag_matching"
"""Configuration key for the 'relaxed tag matching' option.
If True, SSID switches might be created if any of the device's tags match
the SSID's tags. If False, all of the SSID's tags must be present on the device.
"""

# Keys for storing data within `hass.data`.
DATA_CLIENT: str = "client"
"""DEPRECATED or UNUSED. Key formerly used for storing a Meraki API client instance.
Modern integrations typically use a DataUpdateCoordinator.
"""

DATA_COORDINATOR: str = "coordinator"
"""Key used to store the primary `MerakiDataUpdateCoordinator` instance
in `hass.data[DOMAIN][entry.entry_id]`.
"""

# Default Values
DEFAULT_SCAN_INTERVAL: int = 60
"""Default interval in seconds for polling the Meraki API.
Users can override this in the integration's options.
"""

# Home Assistant Platform Types
# These strings match the platform names used by Home Assistant (e.g., "sensor", "switch").
PLATFORM_SENSOR: str = "sensor"
"""String identifier for the sensor platform."""

PLATFORM_DEVICE_TRACKER: str = "device_tracker"
"""String identifier for the device_tracker platform."""

PLATFORM_SWITCH: str = "switch"
"""String identifier for the switch platform."""
# Note: PLATFORM_DEVICE ("device") was listed but is not a standard entity platform.
# Device registration is handled via device_registry, not a "device" platform.
# Removing it from PLATFORMS list if it's not an actual platform being set up.

PLATFORMS: List[str] = [PLATFORM_SENSOR, PLATFORM_DEVICE_TRACKER, PLATFORM_SWITCH]
"""List of Home Assistant platforms supported and set up by this integration."""

# Sensor Types (example, if defining specific sensor type constants)
# These might be used for `device_class` or internal categorization.
SENSOR_CLIENT_COUNT: str = "client_count"
"""Identifier for sensors representing client counts."""

SENSOR_SIGNAL_STRENGTH: str = "signal_strength"
"""Identifier for sensors representing signal strength (RSSI, SNR)."""

SENSOR_DATA_USAGE: str = "data_usage"
"""Identifier for sensors representing data usage (upload/download)."""

SENSOR_SSID_AVAILABILITY: str = "ssid_availability"
"""Identifier for sensors indicating SSID enabled/disabled status."""

SENSOR_SSID_CHANNEL: str = "ssid_channel"
"""Identifier for sensors showing the wireless channel of an SSID."""

# Device/Entity Attributes
# These are keys used when populating `extra_state_attributes` or accessing
# specific pieces of data within device/entity objects.
ATTR_CONNECTED_CLIENTS: str = "connected_clients"
"""Attribute key for storing the number of clients connected to a device or SSID."""

ATTR_SSIDS: str = "ssids"
"""Attribute key for storing information about SSIDs, often a list of SSID dicts
associated with a device in the coordinator's data.
"""

# Warnings and Informational Messages
ERASE_TAGS_WARNING: str = (
    "Tag erasing is enabled! This will ERASE ALL TAGS on your Meraki devices. "
    "Proceed with extreme caution!"
)
"""Warning message displayed to the user if the 'erase tags' option is enabled,
highlighting the potential data loss.
"""
