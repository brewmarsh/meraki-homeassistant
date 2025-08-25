"""Sensor entity for Meraki camera RTSP URL."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiCameraRTSPUrlSensor(CoordinatorEntity[MerakiDataCoordinator], SensorEntity):
    """Representation of a Meraki Camera RTSP URL Sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device_info_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Camera RTSP URL Sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_info_data["serial"]

        self.entity_description = SensorEntityDescription(
            key="rtsp_url",
            name="RTSP Stream URL",
            icon="mdi:video-stream",
        )

        self._attr_unique_id = f"{self._device_serial}_{self.entity_description.key}"
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, self._device_serial)})
        self._attr_name = (
            f"{device_info_data.get('name', 'Camera')} {self.entity_description.name}"
        )
        self._update_state()

    @property
    def native_value(self) -> Optional[str]:
        """Return the state of the sensor (the RTSP URL or None)."""
        return self._attr_native_value

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        """Update the sensor's state based on coordinator data."""
        current_device_data = self.coordinator.get_device(self._device_serial)

        if current_device_data:
            video_settings = current_device_data.get("video_settings", {})
            is_rtsp_enabled = video_settings.get("externalRtspEnabled", False)
            rtsp_url = video_settings.get("rtspUrl")

            if is_rtsp_enabled:
                self._attr_native_value = rtsp_url
            else:
                self._attr_native_value = None
        else:
            self._attr_native_value = None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success and bool(
            self.coordinator.get_device(self._device_serial)
        )
