"""Text platform for Meraki."""

import logging
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.text import TextEntity

from ..const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki text entities from a config entry."""
    entry_data = hass.data.get(DOMAIN, {}).get(config_entry.entry_id, {})
    if not entry_data:
        _LOGGER.warning("Meraki entry data not found for %s", config_entry.entry_id)
        return False

    discovered_entities = entry_data.get("entities", [])

    # Filter for text entities
    text_entities = [
        entity
        for entity in discovered_entities
        if isinstance(entity, TextEntity)
    ]

    _LOGGER.debug("Found %d text entities", len(text_entities))
    if text_entities:
        _LOGGER.debug("Adding %d text entities", len(text_entities))
        chunk_size = 50
        for i in range(0, len(text_entities), chunk_size):
            chunk = text_entities[i:i + chunk_size]
            async_add_entities(chunk)
            if len(text_entities) > chunk_size:
                await asyncio.sleep(1)

    return True
