"""Button platform for the Meraki Home Assistant integration."""

import logging
import asyncio

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

    discovered_entities = entry_data.get("entities", [])
    button_entities = [e for e in discovered_entities if isinstance(e, ButtonEntity)]

    if button_entities:
        _LOGGER.debug("Adding %d button entities", len(button_entities))
        chunk_size = 50
        for i in range(0, len(button_entities), chunk_size):
            chunk = button_entities[i:i + chunk_size]
            async_add_entities(chunk)
            if len(button_entities) > chunk_size:
                await asyncio.sleep(1)

    return True
