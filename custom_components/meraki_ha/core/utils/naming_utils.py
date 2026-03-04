"""Utility functions for naming Meraki devices and entities."""

import dataclasses
import logging
from collections.abc import Mapping
from typing import Any, cast

_LOGGER = logging.getLogger(__name__)


def standardize_device_name(name: str | None) -> str:
    """Standardize device name with Meraki prefix."""
    if not name:
        return "Meraki Device"
    name_str = str(name)
    if (
        name_str.lower().startswith("meraki")
        or name_str.startswith("[")
        or name_str.startswith("Site: ")
    ):
        return name_str
    return f"Meraki {name_str}"


def format_device_name(device: dict[str, Any] | Any, config: Mapping[str, Any]) -> str:
    """Format the device name based on the user's preference."""
    if dataclasses.is_dataclass(type(device)):
        device = dataclasses.asdict(cast(Any, device))

    name = device.get("name")
    model = str(device.get("model") or "")
    product_type = str(device.get("productType") or device.get("product_type") or "")

    if not name:
        if product_type == "ssid":
            name = f"[SSID {device.get('number')}]"
        else:
            name = f"{model} {device.get('serial')}"

    # Enforce [Sensor] prefix for MT devices
    if product_type == "sensor" or model.startswith("MT"):
        if not str(name).startswith("[Sensor]"):
            name = f"[Sensor] {name}"

    return standardize_device_name(name)


def format_entity_name(
    device: dict[str, Any] | Any, config: Mapping[str, Any], entity_name: str | None
) -> str:
    """Format an entity name by combining the device name and entity-specific name."""
    device_name = format_device_name(device, config)
    if entity_name and entity_name.strip():
        return f"{device_name} {entity_name.strip()}"
    return device_name
