"""Utility functions for naming Meraki devices and entities."""

import dataclasses
import logging
from collections.abc import Mapping
from typing import Any, cast

_LOGGER = logging.getLogger(__name__)


def format_device_name(device: dict[str, Any] | Any, config: Mapping[str, Any]) -> str:
    """Format the device name based on the user's preference."""
    if dataclasses.is_dataclass(type(device)):
        device = dataclasses.asdict(cast(Any, device))

    name = device.get("name")

    product_type = device.get("productType")
    model = device.get("model", "")

    if not product_type:
        if model.startswith("MV"):
            product_type = "camera"
        elif model.startswith("MR") or model.startswith("CW"):
            product_type = "wireless"
        elif model.startswith("MX") or model.startswith("Z"):
            product_type = "appliance"
        elif model.startswith("MS"):
            product_type = "switch"
        elif model.startswith("MT"):
            product_type = "sensor"
        elif model.startswith("MG"):
            product_type = "cellularGateway"

    prefix = ""
    if config.get("device_name_format") == "prefix":
        if product_type == "wireless":
            prefix = "[Wireless] "
        elif product_type == "camera":
            prefix = "[Camera] "
        elif product_type == "appliance":
            prefix = "[Appliance] "
        elif product_type == "switch":
            prefix = "[Switch] "
        elif product_type == "sensor":
            prefix = "[Sensor] "
        elif product_type == "cellularGateway":
            prefix = "[Gateway] "

    if not name:
        if product_type == "ssid":
            name = f"SSID {device.get('number')}"
            # SSID doesn't get prefix
            prefix = ""
        else:
            name = f"Meraki {device.get('model', 'Device')} {device.get('serial')}"

    return f"{prefix}{name}"


def format_entity_name(
    device: dict[str, Any] | Any, config: Mapping[str, Any], entity_name: str | None
) -> str:
    """Format an entity name by combining the device name and entity-specific name."""
    device_name = format_device_name(device, config)
    if entity_name and entity_name.strip():
        return f"{device_name} {entity_name.strip()}"
    return device_name
