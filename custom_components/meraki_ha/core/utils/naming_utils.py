"""Utility functions for naming Meraki devices and entities."""

from typing import Any, Dict


import logging

_LOGGER = logging.getLogger(__name__)


def format_device_name(device: Dict[str, Any], config: dict) -> str:
    """Format the device name based on the user's preference."""
    name = device.get("name")
    if not name:
        if device.get("productType") == "ssid":
            name = f"SSID {device.get('number')}"
        else:
            name = f"Meraki {device.get('model', 'Device')} {device.get('serial')}"

    # Default to prefix if not specified
    name_format = config.get("device_name_format", "prefix")

    if name_format == "omit":
        return name

    product_type = device.get("productType")
    if not product_type and "productTypes" in device:
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
