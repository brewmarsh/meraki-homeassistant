"""Binary sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.binary_sensor import BinarySensorEntity

from ..const import DOMAIN, DATA_COORDINATOR
from .device.camera_motion import MerakiCameraMotionSensor
from .switch_port import SwitchPortSensor


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki binary_sensor entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data[DATA_COORDINATOR]

    binary_sensor_entities = []
    devices = coordinator.data.get("devices", [])
    for device_info in devices:
        if device_info["productType"] == "camera":
            binary_sensor_entities.append(MerakiCameraMotionSensor(coordinator, device_info, config_entry))
        elif device_info["productType"] == "switch":
            for port in device_info.get("ports", []):
                binary_sensor_entities.append(SwitchPortSensor(coordinator, device_info, port))

    if binary_sensor_entities:
        async_add_entities(binary_sensor_entities)

    return True
