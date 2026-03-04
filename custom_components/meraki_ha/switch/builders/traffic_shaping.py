"""Traffic shaping switch builder."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ...const_conf import CONF_ENABLE_TRAFFIC_SHAPING
from ...coordinators import MerakiSwitchCoordinator
from ...core.models.network import MerakiTrafficShaping
from ..traffic_shaping import MerakiTrafficShapingSwitch

_LOGGER = logging.getLogger(__name__)


def setup_traffic_shaping_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiSwitchCoordinator,
    added_entities: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up traffic shaping switches."""
    if not config_entry.options.get(CONF_ENABLE_TRAFFIC_SHAPING):
        return
    entities = _build_traffic_shaping_entities(
        coordinator, coordinator.data, config_entry, added_entities
    )
    if entities:
        async_add_entities(entities)


def _build_traffic_shaping_entities(
    coordinator: MerakiSwitchCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build traffic shaping entities."""
    entities: list[SwitchEntity] = []
    traffic_shaping_by_network = data.get("traffic_shaping", {})
    for network_id, traffic_shaping in traffic_shaping_by_network.items():
        entity = _create_traffic_shaping_entity(
            coordinator, config_entry, network_id, traffic_shaping, added_entities
        )
        if entity:
            entities.append(entity)
    return entities


def _create_traffic_shaping_entity(
    coordinator: MerakiSwitchCoordinator,
    config_entry: ConfigEntry,
    network_id: str,
    traffic_shaping: Any,
    added_entities: set[str],
) -> SwitchEntity | None:
    """Create a single traffic shaping switch entity if not already added."""
    if not isinstance(traffic_shaping, MerakiTrafficShaping):
        return None

    unique_id = f"{network_id}_traffic_shaping_switch"
    if unique_id in added_entities:
        return None

    added_entities.add(unique_id)
    return MerakiTrafficShapingSwitch(
        coordinator,
        config_entry,
        network_id,
        traffic_shaping,
    )
