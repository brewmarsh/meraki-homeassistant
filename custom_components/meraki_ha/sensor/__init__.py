"""Sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import CONF_ENABLE_ORG_SENSORS, DOMAIN
from ..discovery.service import DeviceDiscoveryService

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki sensor entities from a config entry."""
    if config_entry.entry_id not in hass.data[DOMAIN]:
        return False

    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    discovery_service: DeviceDiscoveryService = entry_data["discovery_service"]

    # Entities have already been discovered in __init__.py
    sensor_entities = [
        entity
        for entity in discovery_service.all_entities
        if entity.platform.domain == "sensor"
    ]

    # Filter out organization sensors if disabled
    if not config_entry.options.get(CONF_ENABLE_ORG_SENSORS, True):
        _LOGGER.debug("Organization sensors are disabled.")
        filtered_entities = []
        for entity in sensor_entities:
            if "MerakiOrganization" in entity.__class__.__name__:
                _LOGGER.debug("Skipping organization sensor %s", entity.name)
                continue
            filtered_entities.append(entity)
        sensor_entities = filtered_entities

    if sensor_entities:
        async_add_entities(sensor_entities)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Assuming that discovery_service.all_entities is cleared on unload
    return True  # Entities are handled by the main __init__.py unload logic.
