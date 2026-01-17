"""Binary sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from ..entity_descriptions import (
    CAMERA_MOTION_DESCRIPTION,
    MT20_DOOR_DESCRIPTION,
    SWITCH_PORT_DESCRIPTION,
)
from .device.camera_motion import MerakiMotionSensor
from .device.mt20_open_close import MerakiMt20OpenCloseSensor
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
    camera_service = entry_data.get("camera_service")

    binary_sensor_entities: list[Entity] = []
    devices = coordinator.data.get("devices", [])

    # Pre-check for camera service to avoid repeated checks in the loop
    has_camera_service = camera_service is not None

    for device in devices:
        product_type = device.get("productType", "")
        model = device.get("model", "")

        # Add motion sensors for cameras
        if product_type.startswith("camera") and has_camera_service:
            binary_sensor_entities.append(
                MerakiMotionSensor(
                    coordinator,
                    device,
                    camera_service,
                    config_entry,
                    CAMERA_MOTION_DESCRIPTION,
                )
            )

        # Add open/close sensors for MT20 devices
        if model.startswith("MT20"):
            binary_sensor_entities.append(
                MerakiMt20OpenCloseSensor(
                    coordinator, device, config_entry, MT20_DOOR_DESCRIPTION
                )
            )

        # Add switch port sensors
        if product_type == "switch":
            for port in device.get("ports_statuses", []):
                binary_sensor_entities.append(
                    SwitchPortSensor(
                        coordinator, device, port, SWITCH_PORT_DESCRIPTION
                    )
                )

    if binary_sensor_entities:
        async_add_entities(binary_sensor_entities)

    return True
