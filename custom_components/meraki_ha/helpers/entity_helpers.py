"""Helper functions for entities."""

from ..const import (
    DEVICE_NAME_FORMAT_PREFIX,
    DEVICE_NAME_FORMAT_SUFFIX,
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
    if apply_format:
        if name_format == DEVICE_NAME_FORMAT_PREFIX:
            return f"[{device_type.capitalize()}] {device_name}"
        if name_format == DEVICE_NAME_FORMAT_SUFFIX:
            return f"{device_name} [{device_type.capitalize()}]"
    return device_name
