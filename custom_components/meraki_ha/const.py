"""Constants for the meraki_ha integration."""

DOMAIN = "meraki_ha"
"""Domain for the component."""

CONF_MERAKI_API_KEY = "meraki_api_key"
"""Configuration key for the Meraki API key."""

CONF_MERAKI_ORG_ID = "meraki_org_id"
"""Configuration key for the Meraki organization ID."""

DATA_CLIENT = "client"
"""Key for storing the Meraki API client in Home Assistant's data."""

DATA_COORDINATOR = "coordinator"
"""Key for storing the Meraki data coordinator in Home Assistant's data."""

DEFAULT_SCAN_INTERVAL = 60
"""Default scan interval for the Meraki API data."""

# Platform types
PLATFORM_SENSOR = "sensor"
PLATFORM_DEVICE_TRACKER = "device_tracker"
PLATFORM_DEVICE = "device"

PLATFORMS = [PLATFORM_SENSOR, PLATFORM_DEVICE_TRACKER, PLATFORM_DEVICE]
"""List of platforms supported by the integration."""

# Sensor types
SENSOR_CLIENT_COUNT = "client_count"
SENSOR_SIGNAL_STRENGTH = "signal_strength"
SENSOR_DATA_USAGE = "data_usage"
SENSOR_SSID_AVAILABILITY = "ssid_availability"
SENSOR_SSID_CHANNEL = "ssid_channel"

# Device Attributes
ATTR_CONNECTED_CLIENTS = "connected_clients"
ATTR_SSIDS = "ssids"

# Configuration options
#   const.py
ERASE_TAGS_WARNING = (
    "Tag erasing is enabled! This will ERASE ALL TAGS on your Meraki devices. "
    "Proceed with extreme caution!"
)
CONF_RELAXED_TAG_MATCHING = "relaxed_tag_matching"
"""Configuration key for relaxed tag matching."""
