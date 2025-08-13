"""Helper functions for entities."""


def format_entity_name(
    device_name: str,
    entity_specific_name: str,
) -> str:
    """Format the entity name by combining the device name and the entity specific name."""
    if entity_specific_name and entity_specific_name.strip():
        return f"{device_name} {entity_specific_name}"
    return device_name
