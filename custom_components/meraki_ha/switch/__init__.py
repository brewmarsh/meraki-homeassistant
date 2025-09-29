"""Switch platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import device_registry as dr

from ..const import DOMAIN
from .setup_helpers import async_setup_switches


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki switch entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    camera_service = entry_data["camera_service"]

    device_registry = dr.async_get(hass)
    for network in coordinator.data.get("networks", []):
        device_registry.async_get_or_create(
            config_entry_id=config_entry.entry_id,
            identifiers={(DOMAIN, f"network_{network['id']}")},
            name=network["name"],
            manufacturer="Cisco Meraki",
            model="Network",
        )

    switch_entities = async_setup_switches(hass, config_entry, coordinator, camera_service)

    _LOGGER.debug("Found %d switch entities", len(switch_entities))
    if switch_entities:
        async_add_entities(switch_entities)

    return True
