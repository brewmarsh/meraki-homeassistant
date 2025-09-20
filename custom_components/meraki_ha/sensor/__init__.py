"""Sensor platform for the Meraki Home Assistant integration."""

import logging

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
    # All entities are discovered and created in the main __init__.py's
    # async_setup_entry function. They are stored in hass.data.
    # This platform setup function simply needs to filter for the
    # sensor entities that have already been created.
    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Add discovered entities
    discovered_entities = entry_data.get("entities", [])

    sensor_entities = [e for e in discovered_entities if isinstance(e, SensorEntity)]

    if sensor_entities:
        async_add_entities(sensor_entities)

    return True
