"""Sensor platform for the Meraki Home Assistant integration."""

<<<<<<< HEAD
<<<<<<< HEAD
import logging

=======
<<<<<<< HEAD
import logging

=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
import asyncio
import logging

from homeassistant.components.sensor import SensorEntity
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

<<<<<<< HEAD
<<<<<<< HEAD
from ..const import DOMAIN, PLATFORM_SENSOR
from .setup_helpers import async_setup_sensors
=======
<<<<<<< HEAD
from ..const import DOMAIN, PLATFORM_SENSOR
from .setup_helpers import async_setup_sensors
=======
from ..const import DOMAIN
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
from ..const import DOMAIN
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki sensor entities from a config entry."""
<<<<<<< HEAD
<<<<<<< HEAD
    if config_entry.entry_id not in hass.data[DOMAIN]:
        # This entry is not ready yet, we'll wait for the coordinator to be ready
        return False
=======
<<<<<<< HEAD
    if config_entry.entry_id not in hass.data[DOMAIN]:
        # This entry is not ready yet, we'll wait for the coordinator to be ready
        return False
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    camera_service = entry_data["camera_service"]

    # Set up the sensors
    sensor_entities = async_setup_sensors(
        hass, config_entry, coordinator, camera_service
    )

    if sensor_entities:
        async_add_entities(sensor_entities)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_SENSOR])
=======
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    camera_service = entry_data["camera_service"]

    # Set up the sensors
    sensor_entities = async_setup_sensors(
        hass, config_entry, coordinator, camera_service
    )

    if sensor_entities:
        async_add_entities(sensor_entities)

    return True
<<<<<<< HEAD
<<<<<<< HEAD


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, [PLATFORM_SENSOR])
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
