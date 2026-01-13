"""Binary sensor platform for the Meraki Home Assistant integration."""

<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
from .device.camera_motion import MerakiMotionSensor
from .device.mt20_open_close import MerakiMt20OpenCloseSensor
from .switch_port import SwitchPortSensor
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
import asyncio
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
<<<<<<< HEAD
<<<<<<< HEAD
from .device.camera_motion import MerakiMotionSensor
from .device.mt20_open_close import MerakiMt20OpenCloseSensor
from .switch_port import SwitchPortSensor
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up Meraki binary sensor entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
<<<<<<< HEAD
<<<<<<< HEAD
    coordinator = entry_data["coordinator"]
    camera_service = entry_data.get("camera_service")
=======
<<<<<<< HEAD
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
                MerakiMotionSensor(coordinator, device, camera_service, config_entry)
            )

        # Add open/close sensors for MT20 devices
        if model.startswith("MT20"):
            binary_sensor_entities.append(
                MerakiMt20OpenCloseSensor(coordinator, device, config_entry)
            )

        # Add switch port sensors
        if product_type == "switch":
            for port in device.get("ports_statuses", []):
                binary_sensor_entities.append(
                    SwitchPortSensor(coordinator, device, port)
                )

    if binary_sensor_entities:
        async_add_entities(binary_sensor_entities)
=======
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

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
                MerakiMotionSensor(coordinator, device, camera_service, config_entry)
            )

        # Add open/close sensors for MT20 devices
        if model.startswith("MT20"):
            binary_sensor_entities.append(
                MerakiMt20OpenCloseSensor(coordinator, device, config_entry)
            )

        # Add switch port sensors
        if product_type == "switch":
            for port in device.get("ports_statuses", []):
                binary_sensor_entities.append(
                    SwitchPortSensor(coordinator, device, port)
                )

    if binary_sensor_entities:
<<<<<<< HEAD
        async_add_entities(binary_sensor_entities)
=======
        _LOGGER.debug("Adding %d binary_sensor entities", len(binary_sensor_entities))
        chunk_size = 50
        for i in range(0, len(binary_sensor_entities), chunk_size):
            chunk = binary_sensor_entities[i : i + chunk_size]
            async_add_entities(chunk)
            if len(binary_sensor_entities) > chunk_size:
                await asyncio.sleep(1)
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

    return True
