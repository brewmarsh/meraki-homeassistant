"""Helper functions for entities."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..const import (
    DEVICE_NAME_FORMAT_NONE,
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
)
from .logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.MAIN


def format_entity_name(
    device_name: str,
    device_type: str,
    name_format: str = DEVICE_NAME_FORMAT_NONE,
    apply_prefix: bool = True,
) -> str:
    """Format the entity name based on the user's selection."""
    _LOGGER.debug(
        "Formatting entity name: name=%s, type=%s, format=%s, prefix=%s",
        device_name,
        device_type,
        name_format,
        apply_prefix,
    )
    if apply_prefix and device_type != "sensor":
        if name_format == DEVICE_NAME_FORMAT_PREFIX:
            return f"[{device_type.capitalize()}] {device_name}"
        if name_format == DEVICE_NAME_FORMAT_SUFFIX:
            return f"{device_name} [{device_type.capitalize()}]"
    return device_name


def get_device_from_coordinator(
    coordinator: MerakiDataCoordinator,
    serial: str,
) -> dict[str, Any] | None:
    """Get a device from the coordinator by serial number."""
    if not coordinator.data:
        return None
    devices = coordinator.data.get("devices")
    if devices:
        for device in devices:
            if device.get("serial") == serial:
                return device
    return None
