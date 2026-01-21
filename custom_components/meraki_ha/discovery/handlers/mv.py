"""
MV (Camera) Device Handler.

This module defines the MVHandler class, which is responsible for discovering
entities for Meraki MV series (camera) devices.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

<<<<<<< HEAD
from ...binary_sensor.device.camera_motion import MerakiMotionSensor
from ...button.device.camera_snapshot import MerakiSnapshotButton
from ...camera import MerakiCamera
from ...sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
=======
from custom_components.meraki_ha.binary_sensor.device.camera_motion import (
    MerakiMotionSensor,
)
from custom_components.meraki_ha.button.device.camera_snapshot import (
    MerakiSnapshotButton,
)
from custom_components.meraki_ha.camera import MerakiCamera
from custom_components.meraki_ha.core.errors import MerakiInformationalError
from custom_components.meraki_ha.entity_descriptions import CAMERA_MOTION_DESCRIPTION
from custom_components.meraki_ha.sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
from custom_components.meraki_ha.sensor.device.rtsp_url import MerakiRtspUrlSensor
from custom_components.meraki_ha.switch.camera_controls import AnalyticsSwitch

>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from .base import BaseDeviceHandler

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

<<<<<<< HEAD
    from ....core.api.client import MerakiAPIClient
    from ....services.network_control_service import NetworkControlService
    from ....types import MerakiDevice
    from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService
=======
    from ....types import MerakiDevice
    from ...coordinator import MerakiDataUpdateCoordinator
    from ...core.coordinators.switch_port_status_coordinator import (
        SwitchPortStatusCoordinator,
    )
    from ...services.camera_service import CameraService
    from ...services.device_control_service import DeviceControlService
    from ...services.network_control_service import NetworkControlService
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


_LOGGER = logging.getLogger(__name__)


class MVHandler(BaseDeviceHandler):
    """Handler for Meraki MV (camera) devices."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
<<<<<<< HEAD
        network_control_service: NetworkControlService,
        meraki_client: MerakiAPIClient,
=======
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    ) -> None:
        """Initialize the MVHandler."""
        super().__init__(coordinator, device, config_entry)
        self._camera_service = camera_service
        self._control_service = control_service
<<<<<<< HEAD
        self._network_control_service = network_control_service
        self._meraki_client = meraki_client
=======
        self._meraki_client = coordinator.api
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    @classmethod
    def create(
        cls,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        device: MerakiDevice,
        config_entry: ConfigEntry,
        camera_service: CameraService,
        control_service: DeviceControlService,
        network_control_service: NetworkControlService,
<<<<<<< HEAD
        meraki_client: MerakiAPIClient = None,
=======
        switch_port_coordinator: SwitchPortStatusCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    ) -> MVHandler:
        """Create an instance of the handler."""
        return cls(
            coordinator,
            device,
            config_entry,
            camera_service,
            control_service,
<<<<<<< HEAD
            network_control_service,
            meraki_client,
=======
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        )

    async def discover_entities(self) -> list[Entity]:
        """Discover entities for a camera device."""
        entities: list[Entity] = []
<<<<<<< HEAD
        serial = self.device["serial"]
=======
        serial = self.device.serial

        # If configured, ensure the RTSP stream is enabled by default
        if self._config_entry.options.get("rtsp_stream_enabled", False):
            try:
                _LOGGER.debug(
                    "RTSP stream is defaulted to on, enabling for camera %s",
                    serial,
                )
                await self._camera_service.async_set_rtsp_stream_enabled(serial, True)
            except MerakiInformationalError as e:
                _LOGGER.warning("Could not enable RTSP stream for %s: %s", serial, e)
                self._coordinator.add_status_message(
                    serial, f"Could not enable RTSP stream: {e}"
                )
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

        # Always create the base camera entity
        entities.append(
            MerakiCamera(
                self._coordinator,
                self._config_entry,
                self.device,
                self._camera_service,
            )
        )

<<<<<<< HEAD
        # The rest of the sensors should probably be created regardless of stream
        # availability
=======
        # The rest of the sensors should probably be created
        # regardless of stream availability
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        features = await self._camera_service.get_supported_analytics(serial)

        if "person_detection" in features:
            entities.append(
                MerakiPersonCountSensor(
                    self._coordinator,
                    self.device,
<<<<<<< HEAD
                    self._camera_service,
=======
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
                )
            )

        if "vehicle_detection" in features:
            entities.append(
                MerakiVehicleCountSensor(
                    self._coordinator,
                    self.device,
<<<<<<< HEAD
                    self._camera_service,
=======
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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

<<<<<<< HEAD
=======
        # Add RTSP URL sensor
        entities.append(
            MerakiRtspUrlSensor(
                self._coordinator,
                self.device,
                self._config_entry,
            )
        )

        # Add control switches
        entities.append(
            AnalyticsSwitch(
                self._coordinator,
                self._meraki_client,
                self.device,
            )
        )

>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        return entities
