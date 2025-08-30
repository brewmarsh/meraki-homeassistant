"""
Sensor entity for displaying the RTSP URL of a camera.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiRtspUrlSensor(CoordinatorEntity[MerakiDataCoordinator], SensorEntity):
    """Representation of an RTSP URL sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Dict[str, Any],
        camera_service: CameraService,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._camera_service = camera_service
        self._attr_unique_id = f"{self._device['serial']}-rtsp-url"
        self._attr_name = f"{self._device['name']} RTSP URL"
        self._attr_native_value = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    async def async_update(self) -> None:
        """Update the sensor."""
        serial = self._device["serial"]
        try:
            self._attr_native_value = await self._camera_service.get_video_stream_url(
                serial
            )
        except Exception as e:
            _LOGGER.error("Error updating RTSP URL sensor for %s: %s", serial, e)
            self._attr_native_value = None
