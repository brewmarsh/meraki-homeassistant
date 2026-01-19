"""Utility functions for naming Meraki devices and entities."""

import logging
from collections.abc import Mapping
from typing import Any

_LOGGER = logging.getLogger(__name__)


def format_device_name(device: dict[str, Any], config: Mapping[str, Any]) -> str:
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
<<<<<<< HEAD


def format_entity_name(
    device: dict[str, Any], config: Mapping[str, Any], entity_name: str | None
) -> str:
    """Format an entity name by combining the device name and entity-specific name."""
    device_name = format_device_name(device, config)
    if entity_name:
        return f"{device_name} {entity_name}"
    return device_name
=======
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
