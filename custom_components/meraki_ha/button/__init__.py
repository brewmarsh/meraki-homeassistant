"""Button platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.button import ButtonEntity

from ..const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki button entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Add discovered entities
    discovered_entities = entry_data.get("entities", [])

    button_entities = [e for e in discovered_entities if isinstance(e, ButtonEntity)]

    if button_entities:
        async_add_entities(button_entities)

    return True
