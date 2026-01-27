"""Sensor platform for the Meraki Home Assistant integration."""

import asyncio
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import CONF_ENABLE_ORG_SENSORS, DOMAIN

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

    # Filter out organization sensors if disabled
    # Org sensors are typically identifiable by their unique_id starting with org prefix
    # or their class.
    # Based on inspection, org sensors are added to discovered_entities.
    # We can filter them here.

    if not config_entry.options.get(CONF_ENABLE_ORG_SENSORS, True):
        _LOGGER.debug("Organization sensors are disabled.")
        # Identify org sensors.
        # In MerakiOrganizationEntity, unique_id is f"{org_id}_{key}" usually.
        # Let's check the class name or module of the entity.
        filtered_entities = []
        for entity in sensor_entities:
            # Check if it is an org sensor
            # Using class name check or module check
            if "MerakiOrganization" in entity.__class__.__name__:
                _LOGGER.debug("Skipping organization sensor %s", entity.name)
                continue
            filtered_entities.append(entity)
        sensor_entities = filtered_entities

    if sensor_entities:
        _LOGGER.debug("Adding %d sensor entities", len(sensor_entities))
        chunk_size = 50
        for i in range(0, len(sensor_entities), chunk_size):
            chunk = sensor_entities[i : i + chunk_size]
            async_add_entities(chunk)
            if len(sensor_entities) > chunk_size:
                await asyncio.sleep(1)

    return True
