"""Meraki MS Switch Handler."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
    from ...meraki_data_coordinator import MerakiDataCoordinator


_LOGGER = logging.getLogger(__name__)


class MSHandler(BaseDeviceHandler):
    """Handler for Meraki MS switches."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> None:
        """Initialize the MSHandler."""
        super().__init__(coordinator, device, config_entry)
        self._control_service = control_service
        self._network_control_service = network_control_service

    @classmethod
    def create(
        cls,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
    ) -> MSHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            control_service,
            network_control_service,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for the MS switch."""
        from ...binary_sensor.switch_port import SwitchPortSensor
        from ...sensor.device.switch_energy import MerakiSwitchEnergySensor
        from ...sensor.device.switch_power import MerakiSwitchPowerSensor

        entities: list[Entity] = []

        entities.append(MerakiSwitchPowerSensor(self._coordinator, self.device))
        entities.append(MerakiSwitchEnergySensor(self._coordinator, self.device))

        if self.device and self.device.get("ports_statuses"):
            for port in self.device["ports_statuses"]:
                entities.append(SwitchPortSensor(self._coordinator, self.device, port))
        return entities
