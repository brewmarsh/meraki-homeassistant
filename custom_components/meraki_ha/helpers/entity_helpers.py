"""Helper functions for entities."""

from __future__ import annotations

from typing import Any

<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
=======
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)


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
<<<<<<< HEAD
    coordinator: MerakiDataUpdateCoordinator,
=======
    coordinator: MerakiDataCoordinator,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
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
