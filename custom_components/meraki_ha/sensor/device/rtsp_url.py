"""Sensor entity for displaying the RTSP URL of a camera."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ....const import DOMAIN
from ....core.utils.naming_utils import format_device_name
from ....helpers.entity_helpers import format_entity_name

if TYPE_CHECKING:
    from ....services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiRtspUrlSensor(SensorEntity):
    """Representation of an RTSP URL sensor."""

    def __init__(
        self,
        device_info: dict,
        config_entry: ConfigEntry,
        camera_service: "CameraService",
    ) -> None:
        """Initialize the sensor."""
        self._device_info_data = device_info
        self._config_entry = config_entry
        self._camera_service = camera_service
        self._attr_unique_id = f"{self._device_info_data['serial']}-rtsp-url"
        self._attr_name = format_entity_name(
            format_device_name(self._device_info_data, self._config_entry.options),
            "RTSP URL",
        )
        self._attr_icon = "mdi:cctv"
        self._attr_native_value = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_info_data["serial"])},
            name=format_device_name(self._device_info_data, self._config_entry.options),
            model=self._device_info_data.get("model"),
            manufacturer="Cisco Meraki",
        )

    async def async_update(self) -> None:
        """Update the sensor."""
        serial = self._device_info_data["serial"]
        try:
            self._attr_native_value = await self._camera_service.get_video_stream_url(
                serial
            )
        except Exception as e:
            _LOGGER.error("Error updating RTSP URL sensor for %s: %s", serial, e)
            self._attr_native_value = None

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if the entity should be enabled by default."""
        # Only enable if the camera supports RTSP in the first place.
        return "videoSettings" in self._device_info_data