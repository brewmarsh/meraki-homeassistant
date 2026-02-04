"""Device and sensor constants for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Final

# Re-export for backward compatibility
from .const_sensor import (  # noqa: F401
    SENSOR_CLIENT_COUNT,
    SENSOR_DATA_USAGE,
    SENSOR_SIGNAL_STRENGTH,
    SENSOR_SSID_AVAILABILITY,
    SENSOR_SSID_CHANNEL,
)

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
