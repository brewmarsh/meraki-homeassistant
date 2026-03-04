"""Helper function for setting up all switch entities."""

import logging
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..coordinators import MerakiSwitchCoordinator
from .builders.camera import setup_camera_switches
from .builders.firewall import setup_firewall_rule_switches
from .builders.mt40 import setup_mt40_switches
from .builders.ssid import setup_ssid_switches
from .builders.traffic_shaping import setup_traffic_shaping_switches
from .builders.vlan import setup_vlan_switches
from .builders.vpn import setup_vpn_switches

if TYPE_CHECKING:
    from ..core.api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


def async_setup_switches(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    coordinator: MerakiSwitchCoordinator,
    meraki_client: "MerakiAPIClient",
    async_add_entities: AddEntitiesCallback,
    added_entities: set[str] | None = None,
) -> None:
    """Set up all switch entities from the central coordinator."""
    if added_entities is None:
        added_entities = set()

    if not coordinator.data:
        _LOGGER.warning("Coordinator has no data; skipping switch setup.")
        return

    setup_vlan_switches(config_entry, coordinator, added_entities, async_add_entities)
    setup_firewall_rule_switches(
        config_entry, coordinator, added_entities, async_add_entities
    )
    setup_traffic_shaping_switches(
        config_entry, coordinator, added_entities, async_add_entities
    )
    setup_vpn_switches(config_entry, coordinator, added_entities, async_add_entities)
    setup_ssid_switches(config_entry, coordinator, added_entities, async_add_entities)
    setup_camera_switches(config_entry, coordinator, added_entities, async_add_entities)
    setup_mt40_switches(
        config_entry,
        coordinator,
        added_entities,
        meraki_client,
        async_add_entities,
    )
