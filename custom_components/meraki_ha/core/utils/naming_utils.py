"""Utility functions for naming Meraki devices and entities."""

import logging
import re
from collections.abc import Mapping
from typing import Any

_LOGGER = logging.getLogger(__name__)

# Pattern to match one or more existing prefixes like "[Switch] " or "[MV] [MV] "
# Uses + to match multiple consecutive prefixes
_PREFIX_PATTERN = re.compile(r"^(\[[\w\s]+\]\s+)+")


def format_device_name(device: dict[str, Any], config: Mapping[str, Any]) -> str:
    """Format the device name based on the user's preference.

    This function adds a [ProductType] prefix to device names. It detects and
    removes any existing prefix to prevent duplicates like "[Switch] [Switch] Name".
    """
    name = device.get("name")
    if not name:
        if device.get("productType") == "ssid":
            name = f"SSID {device.get('number')}"
        else:
            name = f"Meraki {device.get('model', 'Device')} {device.get('serial')}"

    # Default to prefix if not specified
    name_format = config.get("device_name_format", "prefix")

    if name_format == "omit":
        # Still strip any existing prefix if present
        return _PREFIX_PATTERN.sub("", name)

    # Strip any existing prefix to prevent duplicates
    clean_name = _PREFIX_PATTERN.sub("", name)

    product_type = device.get("productType")
    if not product_type and "productTypes" in device:
        product_type = "network"

    if not product_type:
        product_type = "device"  # default to device

    # Use Meraki model prefixes for device types
    # MV = Camera, MT = Sensor, MR = Wireless, MS = Switch, MX = Appliance, etc.
    product_type_map = {
        "camera": "MV",
        "sensor": "MT",
        "wireless": "MR",
        "switch": "MS",
        "appliance": "MX",
        "cellularGateway": "MG",
        "network": "Network",
        "organization": "Org",
        "ssid": "SSID",
        "vlan": "VLAN",
    }

    product_type_str = product_type_map.get(product_type, product_type.upper()[:2])

    return f"[{product_type_str}] {clean_name}"
