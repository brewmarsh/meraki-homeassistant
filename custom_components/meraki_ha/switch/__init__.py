"""Switch platform for Meraki."""

<<<<<<< HEAD
=======
import asyncio
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

<<<<<<< HEAD
from ..const import DOMAIN, PLATFORM_SWITCH
=======
from ..const import DATA_CLIENT, DOMAIN, PLATFORM_SWITCH
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
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
<<<<<<< HEAD
    meraki_client = entry_data.get("meraki_client")
    if not meraki_client:
        _LOGGER.warning("Meraki client not available; skipping switch setup.")
        return False

    switch_entities = async_setup_switches(
        hass, config_entry, coordinator, meraki_client
    )

    _LOGGER.debug("Found %d switch entities", len(switch_entities))
    if switch_entities:
        async_add_entities(switch_entities)
=======
    api_client = entry_data.get(DATA_CLIENT)
    if not api_client:
        _LOGGER.warning("Meraki client not available; skipping switch setup.")
        return False

    switch_entities = async_setup_switches(hass, config_entry, coordinator, api_client)

    _LOGGER.debug("Found %d switch entities", len(switch_entities))
    if switch_entities:
        _LOGGER.debug("Adding %d switch entities", len(switch_entities))
        chunk_size = 50
        for i in range(0, len(switch_entities), chunk_size):
            chunk = switch_entities[i : i + chunk_size]
            async_add_entities(chunk)
            if len(switch_entities) > chunk_size:
                await asyncio.sleep(1)
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_SWITCH])
