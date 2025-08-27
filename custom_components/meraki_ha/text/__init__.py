"""Text platform for Meraki."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.text import TextEntity

from ..const import (
    DOMAIN,
    DATA_CLIENT,
)
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
    """Set up Meraki text entities from a config entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data.get("coordinator")
    api_client = entry_data.get(DATA_CLIENT)

    # Initialize repositories and services for the new architecture
    meraki_repository = MerakiRepository(api_client)
    control_service = DeviceControlService(meraki_repository)
    camera_repository = CameraRepository(api_client, api_client.organization_id)
    camera_service = CameraService(camera_repository)
    network_control_service = NetworkControlService(api_client, coordinator)

    # New discovery service setup
    from ..discovery.service import DeviceDiscoveryService

    discovery_service = DeviceDiscoveryService(
        coordinator,
        config_entry,
        api_client,
        camera_service,
        control_service,
        network_control_service,
    )
    discovered_entities = await discovery_service.discover_devices()

    # Filter for text entities
    text_entities = [
        entity
        for entity in discovered_entities
        if isinstance(entity, TextEntity)
    ]

    if text_entities:
        async_add_entities(text_entities)

    return True
