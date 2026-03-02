"""MT40 switch builder."""

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ...coordinators import MerakiSwitchCoordinator
from ..mt40_power_outlet import MerakiMt40PowerOutlet

if TYPE_CHECKING:
    from ...core.api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


def setup_mt40_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiSwitchCoordinator,
    added_entities: set[str],
    meraki_client: "MerakiAPIClient",
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MT40 power outlet switches."""
    entities = _build_mt40_entities(
        coordinator, coordinator.data, config_entry, added_entities, meraki_client
    )
    if entities:
        async_add_entities(entities)


def _build_mt40_entities(
    coordinator: MerakiSwitchCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
    meraki_client: "MerakiAPIClient",
) -> list[SwitchEntity]:
    """Build MT40 power outlet entities."""
    entities: list[SwitchEntity] = []
    devices = data.get("devices", [])
    for device_info in devices:
        entity = _create_mt40_outlet_switch(
            coordinator, device_info, config_entry, added_entities, meraki_client
        )
        if entity:
            entities.append(entity)
    return entities


def _create_mt40_outlet_switch(
    coordinator: MerakiSwitchCoordinator,
    device_info: Any,
    config_entry: ConfigEntry,
    added_entities: set[str],
    meraki_client: "MerakiAPIClient",
) -> SwitchEntity | None:
    """Create an MT40 power outlet switch if applicable and not already added."""
    if not (device_info.model or "").startswith("MT40"):
        return None

    serial = device_info.serial
    network_id = device_info.network_id
    unique_id = f"{serial}_{network_id}_outlet"
    if unique_id in added_entities:
        return None

    added_entities.add(unique_id)
    return MerakiMt40PowerOutlet(
        coordinator, device_info, config_entry, meraki_client
    )
