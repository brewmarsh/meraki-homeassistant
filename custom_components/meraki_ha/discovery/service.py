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
from .handlers.mx import MXHandler
from .handlers.gx import GXHandler
from .handlers.ms import MSHandler
from .handlers.mt import MTHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity
    from ..core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ..hubs.organization import OrganizationHub
    from ..services.camera_service import CameraService
    from ..services.device_control_service import DeviceControlService
    from ...types import MerakiDevice


_LOGGER = logging.getLogger(__name__)

HANDLER_MAPPING = {
    "MR": MRHandler,
    "MV": MVHandler,
    "MX": MXHandler,
    "GX": GXHandler,
    "MS": MSHandler,
    "GS": MSHandler,
    "MT": MTHandler,
    "GR": GXHandler,
}


class DeviceDiscoveryService:
    """A service to discover devices and create corresponding entities."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
    ) -> None:
        """Initialize the DeviceDiscoveryService."""
        self._coordinator = coordinator
        self._config_entry = config_entry
        self._camera_service = camera_service
        self._control_service = control_service
        self._devices: List[MerakiDevice] = self._coordinator.data.get("devices", [])

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
            model = device.get("model")
            if not model:
                _LOGGER.warning("Device %s has no model, skipping", device.get("serial"))
                continue

            handler_class = None
            for prefix, handler in HANDLER_MAPPING.items():
                if model.startswith(prefix):
                    handler_class = handler
                    break

            if not handler_class:
                _LOGGER.debug(
                    "No handler found for model '%s', skipping device %s",
                    model,
                    device.get("serial"),
                )
                continue

            _LOGGER.debug(
                "Using handler %s for device %s",
                handler_class.__name__,
                device.get("serial"),
            )
            
            handler = handler_class(
                self._coordinator,
                device,
                self._config_entry,
                self._camera_service,
                self._control_service,
            )
                
            entities = await handler.discover_entities()
            all_entities.extend(entities)

        _LOGGER.info("Entity discovery complete. Found %d entities.", len(all_entities))
        return all_entities
