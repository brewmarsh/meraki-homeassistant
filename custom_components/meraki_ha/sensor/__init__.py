"""Sensor platform for the Meraki Home Assistant integration."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from ..const import DOMAIN, DATA_CLIENT
from .setup_helpers import async_setup_sensors
from ..core.repository import MerakiRepository
from ..core.repositories.camera_repository import CameraRepository
from ..services.device_control_service import DeviceControlService
from ..services.camera_service import CameraService


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
    meraki_repository = MerakiRepository(api_client)
    control_service = DeviceControlService(meraki_repository)

    # Camera functionality
    camera_repository = CameraRepository(api_client, api_client.organization_id)
    camera_service = CameraService(camera_repository)

    # Legacy sensor setup
    entities = async_setup_sensors(hass, config_entry, coordinator)

    # New discovery service setup
    from ..discovery.service import DeviceDiscoveryService
    from homeassistant.components.sensor import SensorEntity

    discovery_service = DeviceDiscoveryService(
        coordinator, config_entry, camera_service, control_service
    )
    discovered_entities = await discovery_service.discover_devices()
    entities.extend([e for e in discovered_entities if isinstance(e, SensorEntity)])

    if entities:
        async_add_entities(entities)

    return True
