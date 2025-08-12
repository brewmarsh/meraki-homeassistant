"""Utility functions for providing icons for Meraki device types."""

from .device_types import (
    DEVICE_TYPE_APPLIANCE,
    DEVICE_TYPE_CAMERA,
    DEVICE_TYPE_CELLULAR,
    DEVICE_TYPE_SENSOR,
    DEVICE_TYPE_SWITCH,
    DEVICE_TYPE_WIRELESS,
)

DEVICE_TYPE_ICONS = {
    DEVICE_TYPE_APPLIANCE: "mdi:router-wireless",
    DEVICE_TYPE_CAMERA: "mdi:cctv",
    DEVICE_TYPE_CELLULAR: "mdi:signal-cellular-3",
    DEVICE_TYPE_SENSOR: "mdi:sensors",
    DEVICE_TYPE_SWITCH: "mdi:ethernet-switch",
    DEVICE_TYPE_WIRELESS: "mdi:wifi",
}


def get_device_type_icon(device_type: str) -> str:
    """Return the icon for a given device type."""
    return DEVICE_TYPE_ICONS.get(device_type, "mdi:help-circle")
