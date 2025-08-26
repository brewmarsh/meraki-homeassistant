"""Sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import Entity

from ..const import DOMAIN
from .setup_helpers import async_setup_sensors


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
    # This is a bit of a hack, we should have a better way to identify sensor entities
    # For now, we will assume that any entity that is not a camera, switch, or text is a sensor
    from ..camera import MerakiCamera
    from ..switch import MerakiSwitch
    from ..text import MerakiText

    sensor_entities = [
        e
        for e in discovered_entities
        if not isinstance(e, (MerakiCamera, MerakiSwitch, MerakiText))
    ]

    entities.extend(sensor_entities)


    if entities:
        async_add_entities(entities)

    return True
