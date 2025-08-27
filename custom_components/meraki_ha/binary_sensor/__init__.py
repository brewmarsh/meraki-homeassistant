"""Binary sensor platform for the Meraki Home Assistant integration."""

import logging
import asyncio

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.binary_sensor import BinarySensorEntity

from ..const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki binary sensor entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    discovered_entities = entry_data.get("entities", [])
    binary_sensor_entities = [e for e in discovered_entities if isinstance(e, BinarySensorEntity)]

    if binary_sensor_entities:
        _LOGGER.debug("Adding %d binary_sensor entities", len(binary_sensor_entities))
        chunk_size = 50
        for i in range(0, len(binary_sensor_entities), chunk_size):
            chunk = binary_sensor_entities[i:i + chunk_size]
            async_add_entities(chunk)
            if len(binary_sensor_entities) > chunk_size:
                await asyncio.sleep(1)

    return True
