"""Switch platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DATA_CLIENT, DOMAIN, PLATFORM_SWITCH
from .setup_helpers import async_setup_switches

_LOGGER = logging.getLogger(__name__)


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

    if switch_entities:
        _LOGGER.debug("Adding %d switch entities", len(switch_entities))
        async_add_entities(switch_entities)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_SWITCH])
