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
    entity_specific_name: str,
) -> str:
    """Format the entity name based on the user's selection."""
    _LOGGER.debug(f"Formatting entity name with device_name='{device_name}', device_type='{device_type}', name_format='{name_format}', entity_specific_name='{entity_specific_name}'")
    if name_format == DEVICE_NAME_FORMAT_PREFIX:
        formatted_name = f"[{device_type.capitalize()}] {device_name}"
    elif name_format == DEVICE_NAME_FORMAT_SUFFIX:
        formatted_name = f"{device_name} [{device_type.capitalize()}]"
    else:  # omit
        formatted_name = device_name

    if entity_specific_name and entity_specific_name.strip():
        return f"{formatted_name} {entity_specific_name}"
    return formatted_name
