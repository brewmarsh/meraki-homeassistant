"""Helper functions for entities."""

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
from __future__ import annotations

from typing import Any

from ..meraki_data_coordinator import MerakiDataCoordinator


def format_entity_name(
    device_name: str,
    entity_specific_name: str,
) -> str:
    """
    Format the entity name.

    Combines the device name and the entity specific name.

    Args:
    ----
        device_name: The name of the device.
        entity_specific_name: The name of the entity.

    Returns
    -------
        The formatted entity name.

    """
    if entity_specific_name and entity_specific_name.strip():
        return f"{device_name} {entity_specific_name}"
    return device_name


def get_device_from_coordinator(
    coordinator: MerakiDataCoordinator,
    serial: str,
) -> dict[str, Any] | None:
    """
    Retrieve a device from the coordinator's data.

    Args:
    ----
        coordinator: The data update coordinator.
        serial: The serial number of the device.

    Returns
    -------
        The device data, or None if not found.

    """
    return next(
        (
            device
            for device in coordinator.data.get("devices", [])
            if device.get("serial") == serial
        ),
        None,
    )
<<<<<<< HEAD
=======
import logging

from ..const import (
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
)

_LOGGER = logging.getLogger(__name__)

def format_entity_name(
    device_name: str,
    device_type: str,
    name_format: str,
    apply_prefix: bool = True,
) -> str:
    """Format the entity name based on the user's selection."""
    _LOGGER.debug(
        "Formatting entity name: device_name=%s, device_type=%s, name_format=%s, apply_prefix=%s",
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
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
