"""Binary sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from .device.camera_motion import MerakiMotionSensor
from .switch_port import SwitchPortSensor


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki binary sensor entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    camera_service = entry_data["camera_service"]
    switch_port_status_coordinator = entry_data["switch_port_status_coordinator"]

    binary_sensor_entities = []

    # Add motion sensors for cameras
    for device in coordinator.data.get("devices", []):
        if device.get("productType", "").startswith("camera"):
            binary_sensor_entities.append(
                MerakiMotionSensor(coordinator, device, camera_service, config_entry)
            )

    # Add switch port sensors
    for device in coordinator.data.get("devices", []):
        if device.get("productType") == "switch":
            for port in device.get("ports", []):
                binary_sensor_entities.append(
                    SwitchPortSensor(switch_port_status_coordinator, device, port)
                )

    if binary_sensor_entities:
        async_add_entities(binary_sensor_entities)

    return True
