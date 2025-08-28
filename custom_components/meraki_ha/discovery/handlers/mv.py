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
from ...sensor.device.rtsp_url import MerakiRtspUrlSensor
from ...switch.camera_controls import RTSPStreamSwitch, AnalyticsSwitch

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity
    from ....types import MerakiDevice
    from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService
    from ...core.api.client import MerakiAPIClient


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
        meraki_client: "MerakiAPIClient",
    ) -> None:
        """Initialize the MVHandler."""
        super().__init__(coordinator, device, config_entry)
        self._camera_service = camera_service
        self._control_service = control_service
        self._meraki_client = meraki_client

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
        meraki_client: "MerakiAPIClient",
    ) -> "MVHandler":
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            camera_service,
            control_service,
            meraki_client,
        )

    async def discover_entities(self) -> List[Entity]:
        """Discover entities for a camera device."""
        entities: List[Entity] = []
        serial = self.device["serial"]

        # If configured, ensure the RTSP stream is enabled by default
        if self._config_entry.options.get("rtsp_stream_enabled", False):
            try:
                _LOGGER.debug(
                    "RTSP stream is defaulted to on, enabling for camera %s",
                    serial,
                )
                await self._camera_service.async_set_rtsp_stream_enabled(serial, True)
            except MerakiInformationalError as e:
                _LOGGER.warning(
                    "Could not enable RTSP stream for %s: %s", serial, e
                )

        # Always create the base camera entity
        entities.append(
            MerakiCamera(
                self._coordinator,
                self._config_entry,
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

        # Add RTSP URL sensor
        entities.append(
            MerakiRtspUrlSensor(
                self._coordinator,
                self.device,
                self._camera_service,
            )
        )

        # Add control switches
        entities.append(
            RTSPStreamSwitch(
                self._coordinator,
                self._meraki_client,
                self.device,
            )
        )
        entities.append(
            AnalyticsSwitch(
                self._coordinator,
                self._meraki_client,
                self.device,
            )
        )

        return entities
