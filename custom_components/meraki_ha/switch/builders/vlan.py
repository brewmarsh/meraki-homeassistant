"""VLAN switch builder."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ...const_conf import CONF_ENABLE_VLAN_MANAGEMENT
from ...coordinator import MerakiDataUpdateCoordinator
from ..vlan_dhcp import MerakiVLANDHCPSwitch

_LOGGER = logging.getLogger(__name__)


def setup_vlan_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiDataUpdateCoordinator,
    added_entities: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up VLAN switches."""
    if not config_entry.options.get(CONF_ENABLE_VLAN_MANAGEMENT):
        return
    entities = _build_vlan_entities(
        coordinator, coordinator.data, config_entry, added_entities
    )
    if entities:
        async_add_entities(entities)


def _build_vlan_entities(
    coordinator: MerakiDataUpdateCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build VLAN entities."""
    entities: list[SwitchEntity] = []
    vlans_by_network = data.get("vlans", {})
    for network_id, vlans in vlans_by_network.items():
        if isinstance(vlans, list):
            entities.extend(
                _create_vlan_entities(
                    coordinator, config_entry, network_id, vlans, added_entities
                )
            )
    return entities


def _create_vlan_entities(
    coordinator: MerakiDataUpdateCoordinator,
    config_entry: ConfigEntry,
    network_id: str,
    vlans: list[Any],
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Create VLAN entities for a network."""
    entities: list[SwitchEntity] = []
    for vlan in vlans:
        vlan_id = getattr(vlan, "id", None)
        if not vlan_id:
            continue

        unique_id = f"meraki_vlan_{network_id}_{vlan_id}_dhcp"
        if unique_id not in added_entities:
            entities.append(
                MerakiVLANDHCPSwitch(
                    coordinator,
                    config_entry,
                    network_id,
                    vlan,
                )
            )
            added_entities.add(unique_id)
    return entities
