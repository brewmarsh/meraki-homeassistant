"""
Meraki MS Switch Handler.

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
    from ....core.coordinators.meraki_data_coordinator import (
        MerakiDataUpdateCoordinator,
    )
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )
    from ....services.device_control_service import DeviceControlService
    from ....types import MerakiDevice
    from ....services.camera_service import CameraService
    from ....services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class MSHandler(BaseDeviceHandler):
    """Handler for Meraki MS switches."""

    def __init__(
        self,
        coordinator: "MerakiDataUpdateCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        switch_port_coordinator: "SwitchPortStatusCoordinator",
        control_service: "DeviceControlService",
    ) -> None:
        """Initialize the MSHandler."""
        super().__init__(coordinator, device, config_entry)
        self._switch_port_coordinator = switch_port_coordinator
        self._control_service = control_service

    @classmethod
    def create(
        cls,
        coordinator: "MerakiDataUpdateCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        camera_service: "CameraService",
        control_service: "DeviceControlService",
        network_control_service: "NetworkControlService",
        switch_port_coordinator: "SwitchPortStatusCoordinator",
    ) -> "MSHandler":
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            switch_port_coordinator,
            control_service,
        )

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for the MS switch."""
        entities: List[Entity] = []

        # Add switch port sensors, but only for enabled ports to avoid flooding
        # the entity registry.
        ports = self.device.get("ports_statuses", [])
        for port in ports:
            if port.get("enabled"):
                entities.append(
                    SwitchPortSensor(self._switch_port_coordinator, self.device, port)
                )

        return entities
