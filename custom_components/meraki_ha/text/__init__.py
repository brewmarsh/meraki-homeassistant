"""Text platform for Meraki."""

import asyncio

from homeassistant.components.text import TextEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, ENTITY_CHUNK_DELAY, ENTITY_CHUNK_SIZE
from ..helpers.logging_helper import MerakiLoggers

_LOGGER = MerakiLoggers.SWITCH


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
        entity for entity in discovered_entities if isinstance(entity, TextEntity)
    ]

    _LOGGER.debug("Found %d text entities", len(text_entities))
    if text_entities:
        _LOGGER.debug("Adding %d text entities", len(text_entities))
        for i in range(0, len(text_entities), ENTITY_CHUNK_SIZE):
            chunk = text_entities[i : i + ENTITY_CHUNK_SIZE]
            async_add_entities(chunk)
            if len(text_entities) > ENTITY_CHUNK_SIZE:
                await asyncio.sleep(ENTITY_CHUNK_DELAY)

    return True
