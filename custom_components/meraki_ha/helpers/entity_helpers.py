"""Helper functions for entities."""

from __future__ import annotations

from typing import Any

<<<<<<< HEAD
<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
=======
<<<<<<< HEAD
from ..coordinator import MerakiDataUpdateCoordinator
=======
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
from ..meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)


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
<<<<<<< HEAD
    coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
    coordinator: MerakiDataUpdateCoordinator,
=======
    coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    coordinator: MerakiDataCoordinator,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
