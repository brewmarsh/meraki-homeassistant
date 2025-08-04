"""Helper functions for entities."""

from ..const import (
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
    DEVICE_NAME_FORMAT_OMIT,
)


import logging

_LOGGER = logging.getLogger(__name__)

def format_entity_name(
    device_name: str,
    device_type: str,
    name_format: str,
    apply_format: bool = False,
) -> str:
    """Format the entity name based on the user's selection."""
    _LOGGER.debug(
        "Formatting entity name: device_name=%s, device_type=%s, name_format=%s, apply_format=%s",
        device_name,
        device_type,
        name_format,
        apply_format,
    )
    if apply_format:
        if name_format == DEVICE_NAME_FORMAT_PREFIX:
            return f"[{device_type.capitalize()}] {device_name}"
        if name_format == DEVICE_NAME_FORMAT_SUFFIX:
            return f"{device_name} [{device_type.capitalize()}]"
    return device_name
