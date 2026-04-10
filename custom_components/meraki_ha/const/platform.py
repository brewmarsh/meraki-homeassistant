"""Platform constants for the Meraki Home Assistant integration."""

from __future__ import annotations

from typing import Final

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
PLATFORM_SELECT: Final = "select"
"""Represents the select platform."""

PLATFORMS: Final = [
    PLATFORM_SENSOR,
    PLATFORM_BINARY_SENSOR,
    PLATFORM_BUTTON,
    PLATFORM_SWITCH,
    PLATFORM_TEXT,
    PLATFORM_CAMERA,
    PLATFORM_NUMBER,
    PLATFORM_SELECT,
]
"""List of platforms supported by the integration."""
