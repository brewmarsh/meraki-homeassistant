"""Device and sensor constants for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Final

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
