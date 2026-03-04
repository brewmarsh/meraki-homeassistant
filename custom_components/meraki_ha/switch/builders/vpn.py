"""VPN switch builder."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ...const_conf import CONF_ENABLE_VPN_MANAGEMENT
from ...coordinators import MerakiSwitchCoordinator
from ...core.models.network import MerakiVpn
from ..vpn import MerakiVPNSwitch

_LOGGER = logging.getLogger(__name__)


def setup_vpn_switches(
    config_entry: ConfigEntry,
    coordinator: MerakiSwitchCoordinator,
    added_entities: set[str],
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up VPN switches."""
    if not config_entry.options.get(CONF_ENABLE_VPN_MANAGEMENT):
        return
    entities = _build_vpn_entities(
        coordinator, coordinator.data, config_entry, added_entities
    )
    if entities:
        async_add_entities(entities)


def _build_vpn_entities(
    coordinator: MerakiSwitchCoordinator,
    data: dict[str, Any],
    config_entry: ConfigEntry,
    added_entities: set[str],
) -> list[SwitchEntity]:
    """Build VPN entities."""
    entities: list[SwitchEntity] = []
    vpn_status_by_network = data.get("vpn_status", {})
    for network_id, vpn_status in vpn_status_by_network.items():
        if isinstance(vpn_status, MerakiVpn):
            entity = _create_vpn_entity(
                coordinator, config_entry, network_id, added_entities
            )
            if entity:
                entities.append(entity)
    return entities


def _create_vpn_entity(
    coordinator: MerakiSwitchCoordinator,
    config_entry: ConfigEntry,
    network_id: str,
    added_entities: set[str],
) -> SwitchEntity | None:
    """Create a single VPN switch entity if not already added."""
    unique_id = f"vpn_{network_id}"
    if unique_id in added_entities:
        return None

    # We need to fetch the network object for the entity
    network = coordinator.get_network(network_id)
    if not network:
        return None

    added_entities.add(unique_id)
    return MerakiVPNSwitch(
        coordinator,
        config_entry,
        network,
    )
