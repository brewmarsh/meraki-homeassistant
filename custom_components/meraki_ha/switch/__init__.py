"""Switch platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, DATA_COORDINATOR
from .setup_helpers import async_setup_switches


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki switch entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data[DATA_COORDINATOR]

    switch_entities = async_setup_switches(hass, config_entry, coordinator)

    _LOGGER.debug("Found %d switch entities", len(switch_entities))
    if switch_entities:
        async_add_entities(switch_entities)

    return True
