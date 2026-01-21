"""Text platform for Meraki."""

<<<<<<< HEAD
import asyncio
import logging

from homeassistant.components.text import TextEntity
=======
import logging

>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

<<<<<<< HEAD
from ..const import DOMAIN
=======
from ..const import DOMAIN, PLATFORM_TEXT
from .meraki_ssid_name import MerakiSSIDNameText
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki text entities from a config entry."""
<<<<<<< HEAD
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
        chunk_size = 50
        for i in range(0, len(text_entities), chunk_size):
            chunk = text_entities[i : i + chunk_size]
            async_add_entities(chunk)
            if len(text_entities) > chunk_size:
                await asyncio.sleep(1)

    return True
=======
    if config_entry.entry_id not in hass.data[DOMAIN]:
        return False
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    meraki_client = coordinator.api

    if coordinator.data:
        text_entities = [
            MerakiSSIDNameText(coordinator, meraki_client, config_entry, ssid)
            for ssid in coordinator.data.get("ssids", [])
        ]

        if text_entities:
            async_add_entities(text_entities)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_TEXT])
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
