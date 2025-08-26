"""
MV (Camera) Device Handler

This module defines the MVHandler class, which is responsible for discovering
entities for Meraki MV series (camera) devices.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

from .base import BaseDeviceHandler
from ...core.errors import MerakiInformationalError

# These are no longer needed here as they are now handled by the import below
# from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
# from ...services.camera_service import CameraService
from ...camera import MerakiCamera
from ...sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
from ...binary_sensor.device.camera_motion import MerakiMotionSensor
from ...button.device.camera_snapshot import MerakiSnapshotButton

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity
    from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService


_LOGGER = logging.getLogger(__name__)


class MVHandler(BaseDeviceHandler):
    """Handler for Meraki MV (camera) devices."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: dict,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
    ) -> None:
        """Initialize the MVHandler."""
        super().__init__(coordinator, device, config_entry, camera_service)
        self._coordinator = coordinator
        self._config_entry = config_entry
        self._camera_service = camera_service
        self._control_service = control_service

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for a camera device."""
        _LOGGER.debug("Discovering entities for MV device: %s", self.device.get("serial"))
        entities: List[Entity] = []
        serial = self.device["serial"]

        # Check for stream availability before creating the camera entity
        try:
            stream_available = await self._camera_service.get_video_stream_url(serial)
            if stream_available:
                _LOGGER.debug("RTSP stream found for %s, creating camera entity.", serial)
                entities.append(
                    MerakiCamera(
                        self._coordinator,
                        self.device,
                        self._camera_service,
                    )
                )
            else:
                _LOGGER.info("No RTSP stream found for %s, not creating camera entity.", serial)
        except MerakiInformationalError as e:
            _LOGGER.info(
                "Not creating camera entity for %s due to informational error: %s",
                serial,
                e,
            )
        except Exception as e:
            _LOGGER.error(
                "Unexpected error checking for stream for camera %s: %s", serial, e
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
