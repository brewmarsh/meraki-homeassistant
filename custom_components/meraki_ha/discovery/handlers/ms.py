"""
Meraki MS Switch Handler.

This module defines the MSHandler class, which is responsible for discovering
entities for Meraki MS switches.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...binary_sensor.switch_port import SwitchPortSensor
from ...const import CONF_ENABLE_PORT_SENSORS
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ....coordinator import MerakiDataUpdateCoordinator
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice


_LOGGER = logging.getLogger(__name__)


class MSHandler(BaseDeviceHandler):
    """Handler for Meraki MS switches."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
    ) -> None:
        """Initialize the MSHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service

    @classmethod
    def create(
        cls,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
        switch_port_coordinator: SwitchPortStatusCoordinator,
    ) -> MSHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for the MS switch."""
        entities: list[Entity] = []

        # Check if port sensors are enabled
        if self._config_entry.options.get(CONF_ENABLE_PORT_SENSORS, True):
            if self.device and self.device.ports_statuses:
                for port in self.device.ports_statuses:
                    entities.append(
                        SwitchPortSensor(self._coordinator, self.device, port)
                    )
        else:
            _LOGGER.debug("Port sensors disabled for device %s", self.device.serial)

        return entities
