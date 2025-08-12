"""Data structures for Meraki device types."""

from typing import Final
import re

from ._const import (
    DeviceType,
    DEVICE_TYPE_WIRELESS,
    DEVICE_TYPE_SWITCH,
    DEVICE_TYPE_APPLIANCE,
    DEVICE_TYPE_CAMERA,
    DEVICE_TYPE_SENSOR,
    DEVICE_TYPE_CELLULAR,
    DEVICE_TYPE_NETWORK,
    DEVICE_TYPE_UNKNOWN,
)

# Compiled regex pattern for model validation
MODEL_PATTERN: Final = re.compile(
    r"^(MR|MS|MX|MV|MT|MG|GR|GS|GX)\d{1,3}(-[A-Z0-9-]+)?$"
)

# Map device prefixes to types
DEVICE_PREFIX_MAPPINGS: Final[dict[tuple[str, ...], str]] = {
    # Wireless Access Points (both traditional MR and cloud-managed GR series)
    ("MR", "GR"): DeviceType.WIRELESS,
    # Switches (both traditional MS and cloud-managed GS series)
    ("MS", "GS"): DeviceType.SWITCH,
    # Security Appliances (both traditional MX and cloud-managed GX series)
    ("MX", "GX"): DeviceType.APPLIANCE,
    # Cameras
    ("MV",): DeviceType.CAMERA,
    # Environmental Sensors
    ("MT",): DeviceType.SENSOR,
    # Cellular Gateways
    ("MG",): DeviceType.CELLULAR,
}

# Device type descriptions for UI and logging
DEVICE_TYPE_DESCRIPTIONS: Final[dict[str, str]] = {
    DEVICE_TYPE_WIRELESS: "Wireless Access Point",
    DEVICE_TYPE_SWITCH: "Network Switch",
    DEVICE_TYPE_APPLIANCE: "Security Appliance",
    DEVICE_TYPE_CAMERA: "Smart Camera",
    DEVICE_TYPE_SENSOR: "Environmental Sensor",
    DEVICE_TYPE_CELLULAR: "Cellular Gateway",
    DEVICE_TYPE_NETWORK: "Virtual Network Device",
    DEVICE_TYPE_UNKNOWN: "Unknown Device",
}
