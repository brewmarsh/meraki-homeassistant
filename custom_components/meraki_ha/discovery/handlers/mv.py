"""
MV (Camera) Device Handler.

This module defines the MVHandler class, which is responsible for discovering
entities for Meraki MV series (camera) devices.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...binary_sensor.device.camera_motion import MerakiMotionSensor
from ...button.device.camera_snapshot import MerakiSnapshotButton
from ...camera import MerakiCamera
from ...const import CONF_ENABLE_CAMERA_ENTITIES
from ...sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
from ...sensor.device.camera_audio_detection import MerakiCameraAudioDetectionSensor
from ...sensor.device.camera_sense_status import MerakiCameraSenseStatusSensor
from ...sensor.device.meraki_firmware_status import MerakiFirmwareStatusSensor
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...core.api.client import MerakiAPIClient
    from ...meraki_data_coordinator import MerakiDataCoordinator
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService
    from ...services.network_control_service import NetworkControlService
    from ...types import MerakiDevice


_LOGGER = logging.getLogger(__name__)


class MVHandler(BaseDeviceHandler):
    """Handler for Meraki MV (camera) devices."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
        meraki_client: MerakiAPIClient | None = None,
    ) -> None:
        """Initialize the MVHandler."""
        super().__init__(coordinator, device, config_entry)
        self._camera_service = camera_service
        self._control_service = control_service
        self._network_control_service = network_control_service
        self._meraki_client = meraki_client

    @classmethod
    def create(
        cls,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
        meraki_client: MerakiAPIClient | None = None,
    ) -> MVHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            camera_service,
            control_service,
            network_control_service,
            meraki_client,
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for a camera device."""
        entities: list[Entity] = []
        serial = self.device["serial"]

        # Check if camera entities are enabled
        if not self._config_entry.options.get(CONF_ENABLE_CAMERA_ENTITIES, True):
            return entities

        # Always create the base camera entity
        entities.append(
            MerakiCamera(
                self._coordinator,
                self._config_entry,
                self.device,
                self._camera_service,
            )
        )

        # The rest of the sensors should probably be created regardless of stream
        # availability
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
                self._config_entry,
            )
        )

        # Add snapshot button
        entities.append(
            MerakiSnapshotButton(
                self._coordinator,
                self.device,
                self._camera_service,
                self._config_entry,
            )
        )

        # Camera sense status sensor
        entities.append(
            MerakiCameraSenseStatusSensor(
                self._coordinator,
                self.device,
                self._config_entry,
            )
        )

        # Camera audio detection sensor
        entities.append(
            MerakiCameraAudioDetectionSensor(
                self._coordinator,
                self.device,
                self._config_entry,
            )
        )

        # Firmware status sensor
        entities.append(
            MerakiFirmwareStatusSensor(
                self._coordinator,
                self.device,
                self._config_entry,
            )
        )

        return entities
