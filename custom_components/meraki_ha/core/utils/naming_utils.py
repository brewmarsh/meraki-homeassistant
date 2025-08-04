"""Utility functions for naming Meraki devices and entities."""

from typing import Any, Dict

from ...const import (
    CONF_DEVICE_NAME_FORMAT,
    DEFAULT_DEVICE_NAME_FORMAT,
    DEVICE_NAME_FORMAT_OMIT,
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
)


import logging

_LOGGER = logging.getLogger(__name__)

def format_device_name(device: Dict[str, Any], config: Dict[str, Any]) -> str:
    """Format the device name based on the user's preference."""
    name = device.get("name")
    if not name:
        if device.get("productType") == "ssid":
            name = f"SSID {device.get('number')}"
        else:
            name = f"Meraki {device.get('model', 'Device')} {device.get('serial')}"

    name_format = config.get(CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT)
    _LOGGER.debug(f"Formatting device name for device '{name}' with format: {name_format}")
    _LOGGER.debug(f"Device data: {device}")
    _LOGGER.debug(f"Config data: {config}")


    if name_format == DEVICE_NAME_FORMAT_OMIT:
        _LOGGER.debug(f"Formatted device name: {name}")
        return name

    product_type = device.get("productType")

    if product_type in ["switch", "appliance", "camera", "wireless", "sensor"]:
        product_type_str = product_type.capitalize()
    elif product_type in ["ssid", "network"]:
        # SSIDs and networks should not have a prefix/suffix
        _LOGGER.debug(f"Formatted device name for {product_type}: {name}")
        return name
    else:
        product_type_str = "Device"

    if name_format == DEVICE_NAME_FORMAT_PREFIX:
        formatted_name = f"[{product_type_str}] {name}"
        _LOGGER.debug(f"Formatted device name: {formatted_name}")
        return formatted_name
    if name_format == DEVICE_NAME_FORMAT_SUFFIX:
        formatted_name = f"{name} [{product_type_str}]"
        _LOGGER.debug(f"Formatted device name: {formatted_name}")
        return formatted_name
    _LOGGER.debug(f"Formatted device name (default): {name}")
    return name
