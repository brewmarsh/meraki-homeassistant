"""Sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN, DATA_CLIENT
from ..discovery.service import DeviceDiscoveryService
from .setup_helpers import async_setup_sensors
from ..core.repository import MerakiRepository
from ..core.repositories.camera_repository import CameraRepository
from ..services.device_control_service import DeviceControlService
from ..services.camera_service import CameraService
from ..services.network_control_service import NetworkControlService


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

    # Initialize repositories and services for the new architecture
    # MerakiRepository is used for all general device services
    meraki_repository = MerakiRepository(api_client)
    control_service = DeviceControlService(meraki_repository)

    # CameraRepository and CameraService are specifically for camera functionality
    camera_repository = CameraRepository(api_client)
    camera_service = CameraService(camera_repository)

    # Instantiate the new NetworkControlService
    network_control_service = NetworkControlService(api_client, coordinator)

    # Legacy sensor setup
    entities = async_setup_sensors(hass, config_entry, coordinator)

    # New discovery service setup. We now pass both the control and camera services.
    discovery_service = DeviceDiscoveryService(
        coordinator,
        config_entry,
        camera_service,
        control_service,
        network_control_service,
    )
    # The discover_entities method is asynchronous and must be awaited
    discovered_entities = await discovery_service.discover_entities()
    entities.extend(discovered_entities)

    if entities:
        async_add_entities(entities)

    return True
