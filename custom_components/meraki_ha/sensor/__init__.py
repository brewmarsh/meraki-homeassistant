"""Sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, DATA_CLIENT
from ..discovery.service import DeviceDiscoveryService
from .setup_helpers import async_setup_sensors
from ..core.repository import MerakiRepository
from ..services.device_control_service import DeviceControlService


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki sensor entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data.get("coordinator")
    api_client = entry_data.get(DATA_CLIENT)

    repository = MerakiRepository(api_client)
    control_service = DeviceControlService(repository)

    # Legacy sensor setup
    entities = async_setup_sensors(hass, config_entry, coordinator)

    # New discovery service setup
    switch_port_coordinator = entry_data.get("switch_port_coordinator")
    discovery_service = DeviceDiscoveryService(
        coordinator, config_entry, control_service, switch_port_coordinator
    )
    discovered_entities = discovery_service.discover_entities()
    entities.extend(discovered_entities)

    if entities:
        async_add_entities(entities)

    return True
