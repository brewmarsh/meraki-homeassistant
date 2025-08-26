"""Sensor entity for Meraki camera RTSP URL."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...helpers.device_info_helpers import resolve_device_info
from ...helpers.entity_helpers import format_entity_name
from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiCameraRTSPUrlSensor(
    CoordinatorEntity[MerakiDataCoordinator], SensorEntity
):
    """Representation of a Meraki Camera RTSP URL Sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Camera RTSP URL Sensor."""
        super().__init__(coordinator)
        self._device = device
        self._config_entry = config_entry
        self._attr_native_value: str | None = None

        self.entity_description = SensorEntityDescription(
            key="rtsp_url",
            name="RTSP Stream URL",
            icon="mdi:video-stream",
        )

        self._attr_unique_id = f"{self._device['serial']}_{self.entity_description.key}"
        self._attr_device_info = resolve_device_info(
            entity_data=self._device,
            config_entry=self._config_entry,
        )
        self._update_state()

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor (the RTSP URL or None)."""
        return self._attr_native_value

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        """Update the sensor's state based on coordinator data."""
        current_device_data = self.coordinator.get_device(self._device["serial"])

        if current_device_data and (video_settings := current_device_data.get("video_settings")):
            is_rtsp_enabled = video_settings.get("externalRtspEnabled", False)
            rtsp_url = video_settings.get("rtspUrl")
            self._attr_native_value = rtsp_url if is_rtsp_enabled else None
        else:
            self._attr_native_value = None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success and bool(
            self.coordinator.get_device(self._device["serial"])
        )
