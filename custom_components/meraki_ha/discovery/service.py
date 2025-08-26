"""
Device Discovery Service

This module defines the DeviceDiscoveryService, which is responsible for
discovering devices from the Meraki data and delegating entity creation
to the appropriate handlers.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List
import asyncio

from .handlers.mr import MRHandler
from .handlers.mv import MVHandler
from ..core.repositories.camera_repository import CameraRepository
from ..services.camera_service import CameraService
from ..const import DOMAIN, DATA_CLIENT

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from ..core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ..core.api.client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)
HANDLER_MAPPING = {
    "wireless": MRHandler,
    "camera": MVHandler,
}


class DeviceDiscoveryService:
    """A service to discover devices and create corresponding entities."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        config_entry: "ConfigEntry",
    ) -> None:
        """Initialize the DeviceDiscoveryService."""
        self._coordinator = coordinator
        self._config_entry = config_entry
        self._devices = self._coordinator.data.get("devices", [])
        self._api_client: MerakiAPIClient = self._coordinator.hass.data[DOMAIN][
            self._config_entry.entry_id
        ][DATA_CLIENT]
        self._camera_repository = CameraRepository(self._api_client)
        self._camera_service = CameraService(self._camera_repository)

    async def discover_entities(self) -> list:
        """
        Discover all entities for all devices.

        This method iterates through all devices in the organization and uses
        the HANDLER_MAPPING to delegate entity creation to the appropriate
        handler based on the device's product type.
        """
        all_entities = []
        _LOGGER.debug("Starting entity discovery for %d devices", len(self._devices))

        for device in self._devices:
            product_type = device.get("productType")
            if not product_type:
                _LOGGER.warning("Device %s has no product type, skipping", device.get("serial"))
                continue

            handler_class = HANDLER_MAPPING.get(product_type)
            if not handler_class:
                _LOGGER.debug(
                    "No handler found for product type '%s', skipping device %s",
                    product_type,
                    device.get("serial"),
                )
                continue

            _LOGGER.debug(
                "Using handler %s for device %s",
                handler_class.__name__,
                device.get("serial"),
            )

            handler = handler_class(
                self._coordinator, device, self._config_entry, self._camera_service
            )
            entities = await handler.discover_entities()
            all_entities.extend(entities)

        _LOGGER.info("Entity discovery complete. Found %d entities.", len(all_entities))
        return all_entities
