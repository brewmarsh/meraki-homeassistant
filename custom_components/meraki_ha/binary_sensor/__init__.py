"""Binary sensor platform for the Meraki Home Assistant integration."""

import asyncio

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, ENTITY_CHUNK_DELAY, ENTITY_CHUNK_SIZE
from ..helpers.logging_helper import MerakiLoggers
from .mqtt_status import async_setup_mqtt_sensors
from .webhook_health import MerakiWebhookHealthSensor

_LOGGER = MerakiLoggers.SENSOR


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki binary sensor entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data.get("coordinator")

    discovered_entities = entry_data.get("entities", [])
    binary_sensor_entities = [
        e for e in discovered_entities if isinstance(e, BinarySensorEntity)
    ]

    # Add MQTT status sensors if MQTT is enabled
    if coordinator is not None:
        mqtt_sensors = await async_setup_mqtt_sensors(hass, config_entry, coordinator)
        binary_sensor_entities.extend(mqtt_sensors)

        # Add webhook health sensor if webhooks are enabled
        webhook_manager = entry_data.get("webhook_manager")
        if webhook_manager:
            webhook_health_sensor = MerakiWebhookHealthSensor(
                coordinator, config_entry, webhook_manager
            )
            binary_sensor_entities.append(webhook_health_sensor)

    if binary_sensor_entities:
        _LOGGER.debug("Adding %d binary_sensor entities", len(binary_sensor_entities))
        for i in range(0, len(binary_sensor_entities), ENTITY_CHUNK_SIZE):
            chunk = binary_sensor_entities[i : i + ENTITY_CHUNK_SIZE]
            async_add_entities(chunk)
            if len(binary_sensor_entities) > ENTITY_CHUNK_SIZE:
                await asyncio.sleep(ENTITY_CHUNK_DELAY)

    return True
