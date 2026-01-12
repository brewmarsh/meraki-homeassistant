"""Switch platform for Meraki."""

import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import (
    DATA_CLIENT,
    DOMAIN,
    ENTITY_CHUNK_DELAY,
    ENTITY_CHUNK_SIZE,
    PLATFORM_SWITCH,
)
from ..helpers.logging_helper import MerakiLoggers
from .setup_helpers import async_setup_switches

_LOGGER = MerakiLoggers.SWITCH


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki switch entities from a config entry."""
    if config_entry.entry_id not in hass.data[DOMAIN]:
        # This entry is not ready yet, we'll wait for the coordinator to be ready
        return False
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    api_client = entry_data.get(DATA_CLIENT)
    if not api_client:
        _LOGGER.warning("Meraki client not available; skipping switch setup.")
        return False

    switch_entities = async_setup_switches(hass, config_entry, coordinator, api_client)

    _LOGGER.debug("Found %d switch entities", len(switch_entities))
    if switch_entities:
        _LOGGER.debug("Adding %d switch entities", len(switch_entities))
        for i in range(0, len(switch_entities), ENTITY_CHUNK_SIZE):
            chunk = switch_entities[i : i + ENTITY_CHUNK_SIZE]
            async_add_entities(chunk)
            if len(switch_entities) > ENTITY_CHUNK_SIZE:
                await asyncio.sleep(ENTITY_CHUNK_DELAY)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_SWITCH])
