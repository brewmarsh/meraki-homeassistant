"""Core utilities package."""

from .device_types import (
    DEVICE_TYPE_APPLIANCE,
    DEVICE_TYPE_CAMERA,
    DEVICE_TYPE_CELLULAR,
    DEVICE_TYPE_NETWORK,
    DEVICE_TYPE_SENSOR,
    DEVICE_TYPE_SWITCH,
    DEVICE_TYPE_UNKNOWN,
    DEVICE_TYPE_WIRELESS,
    map_meraki_model_to_device_type,
)

__all__ = [
    "DEVICE_TYPE_WIRELESS",
    "DEVICE_TYPE_SWITCH",
    "DEVICE_TYPE_APPLIANCE",
    "DEVICE_TYPE_CAMERA",
    "DEVICE_TYPE_SENSOR",
    "DEVICE_TYPE_CELLULAR",
    "DEVICE_TYPE_NETWORK",
    "DEVICE_TYPE_UNKNOWN",
    "map_meraki_model_to_device_type",
]
