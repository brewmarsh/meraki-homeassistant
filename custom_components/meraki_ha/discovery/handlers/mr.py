"""
MR (Wireless) Device Handler

This module defines the MRHandler class, which is responsible for discovering
entities for Meraki MR series (wireless) devices.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.helpers.entity import Entity
    from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from homeassistant.config_entries import ConfigEntry
    from ....types import MerakiDevice
    from ...services.device_control_service import DeviceControlService


_LOGGER = logging.getLogger(__name__)


class MRHandler(BaseDeviceHandler):
    """Handler for Meraki MR (wireless) devices."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: "CameraService",
        control_service: "DeviceControlService",
    ) -> None:
        """Initialize the MRHandler."""
        super().__init__(coordinator, device, config_entry, camera_service)
        self._control_service = control_service

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for a wireless device."""
        _LOGGER.debug(
            "Discovering entities for MR device: %s", self.device.get("serial")
        )
        entities: List[Entity] = []

        # In the future, this is where we would create entities like:
        # - Radio settings sensors
        # - Connected client count sensors
        # - etc.
        #
        # For example:
        # if "radio_settings" in self.device:
        #     entities.append(RadioSettingsSensor(self.device))

        return entities
