"""Utility functions for naming Meraki devices and entities."""

from typing import Any, Dict, Mapping

from ...const import (
    CONF_DEVICE_NAME_FORMAT,
    DEFAULT_DEVICE_NAME_FORMAT,
    DEVICE_NAME_FORMAT_OMIT,
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
)


import logging

_LOGGER = logging.getLogger(__name__)


def format_device_name(device: Dict[str, Any], config: Mapping[str, Any]) -> str:
    """Format the device name based on the user's preference."""
    name = device.get("name")
    if not name:
        if device.get("productType") == "ssid":
            name = f"SSID {device.get('number')}"
        else:
            name = f"Meraki {device.get('model', 'Device')} {device.get('serial')}"

    name_format = config.get(CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT)

    if name_format == DEVICE_NAME_FORMAT_OMIT:
        return name

    product_type = device.get("productType")
    if not product_type and "productTypes" in device:
        product_type = "network"

    if not product_type:
        product_type = "device"  # default to device

    if product_type == "network":
        product_type_str = "Network"
    elif product_type == "ssid":
        product_type_str = "SSID"
    else:
        product_type_str = product_type.capitalize()

    if name_format == DEVICE_NAME_FORMAT_PREFIX:
        return f"[{product_type_str}] {name}"
    if name_format == DEVICE_NAME_FORMAT_SUFFIX:
        return f"{name} [{product_type_str}]"
    return name
