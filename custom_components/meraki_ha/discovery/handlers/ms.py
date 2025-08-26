"""
Meraki MS Switch Handler

This module defines the MSHandler class, which is responsible for discovering
entities for Meraki MS switches.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler
from ...binary_sensor.switch_port import SwitchPortSensor

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity
    from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ....services.device_control_service import DeviceControlService
    from ....services.camera_service import CameraService
    from ....types import MerakiDevice


_LOGGER = logging.getLogger(__name__)


class MSHandler(BaseDeviceHandler):
    """Handler for Meraki MS switches."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        camera_service: "CameraService",
        control_service: "DeviceControlService",
    ) -> None:
        """Initialize the MSHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service
        self._camera_service = camera_service

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for the MS switch."""
        _LOGGER.debug("Discovering entities for MS switch %s", self.device["serial"])
        entities: List[Entity] = []

        # Add switch port sensors
        ports = self.device.get("ports_statuses", [])
        for port in ports:
            entities.append(SwitchPortSensor(self._coordinator, self.device, port))

        return entities
