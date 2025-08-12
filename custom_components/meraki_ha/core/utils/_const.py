"""Constants for Meraki device types."""
from enum import Enum
from typing import Final, List

# Define device type constants
DEVICE_TYPE_WIRELESS: Final = "wireless"
DEVICE_TYPE_SWITCH: Final = "switch"
DEVICE_TYPE_APPLIANCE: Final = "appliance"
DEVICE_TYPE_CAMERA: Final = "camera"
DEVICE_TYPE_SENSOR: Final = "sensor"
DEVICE_TYPE_CELLULAR: Final = "cellular"
DEVICE_TYPE_NETWORK: Final = "network"
DEVICE_TYPE_SSID: Final = "ssid"
DEVICE_TYPE_UNKNOWN: Final = "unknown"

# Valid device types for type checking
VALID_DEVICE_TYPES: Final[List[str]] = [
    DEVICE_TYPE_WIRELESS,
    DEVICE_TYPE_SWITCH,
    DEVICE_TYPE_APPLIANCE,
    DEVICE_TYPE_CAMERA,
    DEVICE_TYPE_SENSOR,
    DEVICE_TYPE_CELLULAR,
    DEVICE_TYPE_NETWORK,
    DEVICE_TYPE_SSID,
    DEVICE_TYPE_UNKNOWN,
]


class DeviceType(str, Enum):
    """Enum for Meraki device types."""

    WIRELESS = DEVICE_TYPE_WIRELESS
    SWITCH = DEVICE_TYPE_SWITCH
    APPLIANCE = DEVICE_TYPE_APPLIANCE
    CAMERA = DEVICE_TYPE_CAMERA
    SENSOR = DEVICE_TYPE_SENSOR
    CELLULAR = DEVICE_TYPE_CELLULAR
    NETWORK = DEVICE_TYPE_NETWORK
    SSID = DEVICE_TYPE_SSID
    UNKNOWN = DEVICE_TYPE_UNKNOWN
