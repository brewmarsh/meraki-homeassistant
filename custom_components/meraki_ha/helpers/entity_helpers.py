"""Helper functions for entities."""

from typing import Any, Dict, Optional

from ..coordinator import MerakiDataUpdateCoordinator


def format_entity_name(
    device_name: str,
    entity_specific_name: str,
) -> str:
    """Format the entity name by combining the device name and the entity specific name."""
    if entity_specific_name and entity_specific_name.strip():
        return f"{device_name} {entity_specific_name}"
    return device_name


def get_device_from_coordinator(
    coordinator: MerakiDataUpdateCoordinator, serial: str
) -> Optional[Dict[str, Any]]:
    """Retrieve a device from the coordinator's data."""
    for device in coordinator.data.get("devices", []):
        if device.get("serial") == serial:
            return device
    return None
