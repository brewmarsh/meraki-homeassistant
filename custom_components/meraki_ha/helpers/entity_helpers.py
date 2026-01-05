"""Helper functions for entities."""

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
