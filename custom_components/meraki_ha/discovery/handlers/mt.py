"""
Device handler for Meraki MT sensors.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from ....types import MerakiDevice
    from homeassistant.helpers.entity import Entity
    from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from homeassistant.config_entries import ConfigEntry
    from ...services.device_control_service import DeviceControlService
    from ...services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MTHandler(BaseDeviceHandler):
    """Handler for MT series sensors."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: "CameraService",
        control_service: DeviceControlService,
    ) -> None:
        """Initialize the MTHandler."""
        super().__init__(coordinator, device, config_entry, camera_service)
        self._control_service = control_service

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for the device."""
        entities: List[Entity] = []
        _LOGGER.debug("Discovering entities for MT device %s", self.device["serial"])
        return entities
