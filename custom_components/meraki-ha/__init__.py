"""Meraki HA integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .sensor import async_setup_entry as async_setup_sensor_entry

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up meraki_ha from a config entry."""
    _LOGGER.debug("Meraki HA: async_setup_entry in __init__.py called")
    _LOGGER.debug(f"Config Entry: {entry.as_dict()}")

    async def async_add_entities(entities: list):
        """Add entities to Home Assistant."""
        _LOGGER.debug(f"Meraki HA: async_add_entities called with entities: {entities}") #Added log
        hass.async_create_task(
            hass.data["entity_platform"].async_add_entities(DOMAIN, entities)
        )

    try:
        _LOGGER.debug(f"Meraki HA: async_setup_sensor_entry called with async_add_entities: {type(async_add_entities)}") #added log
        await async_setup_sensor_entry(hass, entry, async_add_entities)
        return True
    except Exception as e:
        _LOGGER.error(f"Error setting up sensor entry: {e}")
        return False

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading meraki_ha config entry")
    return True