"""Utility functions for naming Meraki devices and entities."""

import logging
from collections.abc import Mapping
from typing import Any

_LOGGER = logging.getLogger(__name__)


def format_device_name(device: Any, config: Mapping[str, Any]) -> str:
    """Format the device name based on the user's preference."""
    # Handle dict or object
    if isinstance(device, dict):
        name = device.get("name")
        product_type = device.get("productType")
        model = device.get("model", "Device")
        serial = device.get("serial")
        number = device.get("number")
        product_types = device.get("productTypes")
    else:
        name = getattr(device, "name", None)
        product_type = getattr(device, "productType", None)
        model = getattr(device, "model", "Device")
        serial = getattr(device, "serial", None)
        number = getattr(device, "number", None)
        product_types = getattr(device, "productTypes", None)

    if not name:
        if product_type == "ssid":
            name = f"SSID {number}"
        else:
            name = f"Meraki {model} {serial}"

    # Default to prefix if not specified
    name_format = config.get("device_name_format", "prefix")

    if name_format == "omit":
        return name

    if not product_type and product_types:
        product_type = "network"

    if not product_type:
        product_type = "device"  # default to device

    if product_type == "network":
        product_type_str = "Network"
    elif product_type == "organization":
        product_type_str = "Organization"
    elif product_type == "switch":
        product_type_str = "Switch"
    elif product_type == "appliance":
        product_type_str = "Appliance"
    elif product_type == "camera":
        product_type_str = "Camera"
    elif product_type == "ssid":
        product_type_str = "SSID"
    elif product_type == "vlan":
        product_type_str = "VLAN"
    else:
        product_type_str = product_type.capitalize()

    return f"[{product_type_str}] {name}"
