"""
MV (Camera) Device Handler

This module defines the MVHandler class, which is responsible for discovering
entities for Meraki MV series (camera) devices.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler
from ...camera import MerakiCamera
from ...core.errors import MerakiInformationalError
from ...sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
from ...binary_sensor.device.camera_motion import MerakiMotionSensor
from ...button.device.camera_snapshot import MerakiSnapshotButton

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity
    from ....types import MerakiDevice
    from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService
    from ....services.network_control_service import NetworkControlService
    from ....core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )


_LOGGER = logging.getLogger(__name__)


class MVHandler(BaseDeviceHandler):
    """Handler for Meraki MV (camera) devices."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        camera_service: "CameraService",
        control_service: "DeviceControlService",
        network_control_service: "NetworkControlService",
    ) -> None:
        """Initialize the MVHandler."""
        super().__init__(coordinator, device, config_entry)
        self._camera_service = camera_service
        self._control_service = control_service
        self._network_control_service = network_control_service

    @classmethod
    def create(
        cls,
        coordinator: "MerakiDataCoordinator",
        device: "MerakiDevice",
        config_entry: "ConfigEntry",
        camera_service: "CameraService",
        control_service: "DeviceControlService",
        network_control_service: "NetworkControlService",
        switch_port_coordinator: "SwitchPortStatusCoordinator",
    ) -> "MVHandler":
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            camera_service,
            control_service,
            network_control_service,
        )

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for a camera device."""
        entities: List[Entity] = []
        serial = self.device["serial"]

        # Always create the base camera entity
        entities.append(
            MerakiCamera(
                self._coordinator,
                self.device,
                self._camera_service,
            )
        )

        # The rest of the sensors should probably be created regardless of stream availability
        features = await self._camera_service.get_supported_analytics(serial)

        if "person_detection" in features:
            entities.append(
                MerakiPersonCountSensor(
                    self._coordinator,
                    self.device,
                    self._camera_service,
                )
            )

        if "vehicle_detection" in features:
            entities.append(
                MerakiVehicleCountSensor(
                    self._coordinator,
                    self.device,
                    self._camera_service,
                )
            )

        # Add motion sensor
        entities.append(
            MerakiMotionSensor(
                self._coordinator,
                self.device,
                self._camera_service,
            )
        )

        # Add snapshot button
        entities.append(
            MerakiSnapshotButton(
                self._coordinator,
                self.device,
                self._camera_service,
            )
        )

        return entities
