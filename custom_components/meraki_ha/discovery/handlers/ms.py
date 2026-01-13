<<<<<<< HEAD
"""
Meraki MS Switch Handler.

This module defines the MSHandler class, which is responsible for discovering
entities for Meraki MS switches.
"""
=======
"""Meraki MS Switch Handler."""
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

<<<<<<< HEAD
from ...binary_sensor.switch_port import SwitchPortSensor
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
    from ....core.coordinators.meraki_data_coordinator import (
        MerakiDataUpdateCoordinator,
    )
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
    from ....services.camera_service import CameraService
    from ....services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
<<<<<<< HEAD
=======
    from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)


_LOGGER = logging.getLogger(__name__)


class MSHandler(BaseDeviceHandler):
    """Handler for Meraki MS switches."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        switch_port_coordinator: SwitchPortStatusCoordinator,
        control_service: DeviceControlService,
    ) -> None:
        """Initialize the MSHandler."""
        super().__init__(coordinator, device, config_entry)
        self._switch_port_coordinator = switch_port_coordinator
        self._control_service = control_service
=======
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
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)

    @classmethod
    def create(
        cls,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
<<<<<<< HEAD
        switch_port_coordinator: SwitchPortStatusCoordinator,
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
    ) -> MSHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
<<<<<<< HEAD
            switch_port_coordinator,
            control_service,
=======
            control_service,
            network_control_service,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for the MS switch."""
<<<<<<< HEAD
        entities: list[Entity] = []

        # Add switch port sensors, but only for enabled ports to avoid flooding
        # the entity registry.
        ports = self.device.get("ports_statuses", [])
        for port in ports:
            if port.get("enabled"):
                entities.append(
                    SwitchPortSensor(self._switch_port_coordinator, self.device, port)
                )

=======
        from ...binary_sensor.switch_port import SwitchPortSensor

        entities: list[Entity] = []
        if self.device and self.device.get("ports_statuses"):
            for port in self.device["ports_statuses"]:
                entities.append(SwitchPortSensor(self._coordinator, self.device, port))
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
        return entities
