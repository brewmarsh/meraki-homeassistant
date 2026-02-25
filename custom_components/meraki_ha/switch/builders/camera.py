"""Camera switch builder."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ...coordinator import MerakiDataUpdateCoordinator
from ..camera_controls import AnalyticsSwitch

_LOGGER = logging.getLogger(__name__)


def setup_camera_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up camera-specific switches."""
    entities = _build_camera_entities(coordinator, coordinator.data, added_entities)
    if entities:
        async_add_entities(entities)


def _build_camera_entities(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build camera-specific entities."""
    entities: list[SwitchEntity] = []
    devices = data.get("devices", [])
    for device_info in devices:
        entity = _create_camera_analytics_switch(
            coordinator, device_info, added_entities
        )
        if entity:
            entities.append(entity)
    return entities


def _create_camera_analytics_switch(
    coordinator: MerakiDataUpdateCoordinator,
    device_info: Any,
    added_entities: set[str],
) -> SwitchEntity | None:
    """Create a camera analytics switch if applicable and not already added."""
    if not (device_info.product_type or "").startswith("camera"):
        return None

    serial = device_info.serial
    unique_id = f"{serial}_analytics_switch"
    if unique_id in added_entities:
        return None

    added_entities.add(unique_id)
    return AnalyticsSwitch(coordinator, coordinator.api, device_info)
