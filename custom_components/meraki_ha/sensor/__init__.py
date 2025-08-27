"""Sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.text import TextEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.button import ButtonEntity

from ..const import DOMAIN, DATA_CLIENT
from ..core.repository import MerakiRepository
from ..core.repositories.camera_repository import CameraRepository
from ..services.device_control_service import DeviceControlService
from ..services.camera_service import CameraService
from ..services.network_control_service import NetworkControlService
from ..discovery.service import DeviceDiscoveryService
from ..camera import MerakiCamera
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
    api_client = entry_data.get(DATA_CLIENT)

    # Instantiate repositories
    repository = MerakiRepository(api_client)
    camera_repository = CameraRepository(api_client)

    # Instantiate services
    control_service = DeviceControlService(repository)
    camera_service = CameraService(camera_repository)
    network_control_service = NetworkControlService(api_client, coordinator)

    # New discovery service setup. We now pass all necessary services.
    discovery_service = DeviceDiscoveryService(
        coordinator,
        config_entry,
        api_client,
        camera_service,
        control_service,
        network_control_service,
    )

    # The discover_devices method is asynchronous and must be awaited
    discovered_entities = await discovery_service.discover_entities()

    # The new discovery service finds ALL entities, so we no longer need the
    # legacy sensor setup.

    if discovered_entities:
        async_add_entities(discovered_entities)

    return True
