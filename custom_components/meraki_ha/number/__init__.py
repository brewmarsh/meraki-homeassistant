"""Number platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from ..coordinator import MerakiDataUpdateCoordinator
from .setup_helpers import async_setup_numbers


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki number entities from a config entry."""
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    number_entities = async_setup_numbers(hass, config_entry, coordinator)

    _LOGGER.debug("Found %d number entities", len(number_entities))
    if number_entities:
        async_add_entities(number_entities)

    return True
