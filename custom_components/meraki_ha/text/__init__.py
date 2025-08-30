"""Text platform for Meraki."""

import logging

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
        entity for entity in discovered_entities if isinstance(entity, TextEntity)
    ]

    _LOGGER.debug("Found %d text entities", len(text_entities))
    if text_entities:
        async_add_entities(text_entities)

    return True
