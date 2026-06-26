"""Binary sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.meraki_ha.const.config import CONF_ENABLE_PORT_SENSORS
from custom_components.meraki_ha.const.integration import DOMAIN

from .network import async_setup_entry as async_setup_network_entry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki binary sensor entities from a config entry."""
    from ..discovery.service import DeviceDiscoveryService

    if config_entry.entry_id not in hass.data[DOMAIN]:
        return False

    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    discovery_service: DeviceDiscoveryService = entry_data["discovery_service"]
    enable_ports = config_entry.options.get(CONF_ENABLE_PORT_SENSORS, False)

    # Entities have already been discovered in __init__.py
    binary_sensor_entities = []
    for entity in discovery_service.all_entities:
        if not isinstance(entity, BinarySensorEntity):
            continue

        # Filter port-related binary sensors
        if not enable_ports:
            class_name = entity.__class__.__name__
            if "Port" in class_name or "PoE" in class_name:
                _LOGGER.debug("Skipping port-related binary sensor %s", entity.name)
                continue

        binary_sensor_entities.append(entity)

    if binary_sensor_entities:
        async_add_entities(binary_sensor_entities)

    await async_setup_network_entry(hass, config_entry, async_add_entities)

    return True
