"""Utility functions for naming Meraki devices and entities."""

from typing import Any, Dict

from ...const import (
    CONF_DEVICE_NAME_FORMAT,
    DEFAULT_DEVICE_NAME_FORMAT,
    DEVICE_NAME_FORMAT_OMIT,
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
)


def format_device_name(device: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Format the device name based on the user's preference."""
    name = device.get("name")
    if not name:
        if device.get("productType") == "ssid":
            name = f"SSID {device.get('number')}"
        else:
            name = f"Meraki {device.get('model', 'Device')} {device.get('serial')}"

    name_format = config.get(CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT)
    product_type = device.get("productType", "Unknown")

    if name_format == DEVICE_NAME_FORMAT_PREFIX:
        return f"[{product_type.capitalize()}] {name}"
    if name_format == DEVICE_NAME_FORMAT_SUFFIX:
        return f"{name} [{product_type.capitalize()}]"
    if name_format == DEVICE_NAME_FORMAT_OMIT:
        return name
    return name
