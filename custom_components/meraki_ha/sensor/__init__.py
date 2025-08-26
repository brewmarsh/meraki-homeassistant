"""Sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.text import TextEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.button import ButtonEntity

from ..const import DOMAIN
from .setup_helpers import async_setup_sensors
from ..camera import MerakiCamera


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki sensor entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data.get("coordinator")

    # Legacy sensor setup
    entities = async_setup_sensors(hass, config_entry, coordinator)

    # Add discovered entities
    discovered_entities = entry_data.get("entities", [])

    # Filter for sensor entities
    sensor_entities = [
        e
        for e in discovered_entities
        if not isinstance(e, (MerakiCamera, SwitchEntity, TextEntity, BinarySensorEntity, ButtonEntity))
    ]

    entities.extend(sensor_entities)


    if entities:
        async_add_entities(entities)

    return True
