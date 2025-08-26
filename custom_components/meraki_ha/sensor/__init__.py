"""Sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

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

    # New discovery service setup
    from ..discovery.service import DeviceDiscoveryService

    discovery_service = DeviceDiscoveryService(coordinator, config_entry)
    discovered_entities = await discovery_service.discover_entities()
    entities.extend(discovered_entities)

    if entities:
        async_add_entities(entities)

    return True
