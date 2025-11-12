"""Sensor platform for the Meraki Home Assistant integration."""

import logging
import asyncio

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity

from ..const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki sensor entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    discovered_entities = entry_data.get("entities", [])
    sensor_entities = [e for e in discovered_entities if isinstance(e, SensorEntity)]

    if sensor_entities:
        _LOGGER.debug("Adding %d sensor entities", len(sensor_entities))
        chunk_size = 50
        for i in range(0, len(sensor_entities), chunk_size):
            chunk = sensor_entities[i:i + chunk_size]
            async_add_entities(chunk)
            if len(sensor_entities) > chunk_size:
                await asyncio.sleep(1)

    return True
