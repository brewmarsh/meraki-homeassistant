"""Provider for camera analytics and stream entities."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from ...binary_sensor.device.camera_motion import MerakiMotionSensor
from ...button.device.camera_snapshot import MerakiSnapshotButton
from custom_components.meraki_ha.const.integration import CONF_ENABLE_CAMERA_ENTITIES, CONF_RTSP_STREAM_ENABLED, from...core.errors import MerakiInformationalError
from ...sensor.device.camera_analytics import (
    MerakiPersonCountSensor,
    MerakiVehicleCountSensor,
)
from ...sensor.device.rtsp_url import MerakiRtspUrlSensor
from ...switch.camera_controls import AnalyticsSwitch

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.helpers.entity import Entity

    from ...core.models.device import MerakiDevice
    from ...services.camera_service import CameraService
    from ..coordinators import MerakiCameraCoordinator

_LOGGER = logging.getLogger(__name__)


class CameraAnalyticsProvider:
    """Provider for camera analytics entities."""

    @staticmethod
    async def get_entities(
        coordinator: MerakiCameraCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities."""
        camera_service: CameraService | None = kwargs.get("camera_service")
        if not camera_service or not device.serial:
            return []

        entities: list[Entity] = []
        try:
            features = await camera_service.get_supported_analytics(device.serial)
            if "person_detection" in features:
                entities.append(MerakiPersonCountSensor(coordinator, device))
            if "vehicle_detection" in features:
                entities.append(MerakiVehicleCountSensor(coordinator, device))
        except Exception:
            _LOGGER.debug("Could not fetch analytics features for %s", device.serial)

        return entities


class CameraStreamProvider:
    """Provider for camera stream entities."""

    @staticmethod
    async def get_entities(
        coordinator: MerakiCameraCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        **kwargs: Any,
    ) -> list[Entity]:
        """Get entities."""
        camera_service: CameraService | None = kwargs.get("camera_service")
        if not camera_service or not device.serial:
            return []

        # If configured, ensure the RTSP stream is enabled by default for cameras
        if config_entry.options.get(CONF_RTSP_STREAM_ENABLED, False):
            try:
                _LOGGER.debug(
                    "RTSP stream is defaulted to on, enabling for camera %s",
                    device.serial,
                )
                await camera_service.async_set_rtsp_stream_enabled(device.serial, True)
            except MerakiInformationalError as e:
                _LOGGER.warning(
                    "Could not enable RTSP stream for %s: %s", device.serial, e
                )
                coordinator.add_status_message(
                    device.serial, f"Could not enable RTSP stream: {e}"
                )

        if not config_entry.options.get(CONF_ENABLE_CAMERA_ENTITIES, True):
            return []

        return [
            MerakiMotionSensor(
                coordinator,
                device,
                camera_service,
                config_entry,
            ),
            MerakiSnapshotButton(
                coordinator,
                device,
                camera_service,
                config_entry,
            ),
            MerakiRtspUrlSensor(
                coordinator,
                device,
                config_entry,
            ),
            AnalyticsSwitch(coordinator, coordinator.api, device),
        ]
