"""Sensor entities for Meraki camera settings.

This module defines sensor entities for camera sense and audio detection status.
"""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import callback
# from homeassistant.helpers.entity import EntityDescription # No longer needed
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinators import MerakiDataUpdateCoordinator
from ...const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSenseStatusSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Camera Sense Status sensor.

    This sensor entity displays the MV Sense enabled status for a Meraki camera.
    It uses SensorEntityDescription to define its properties.
    The state ("enabled"/"disabled") is derived from the 'senseEnabled'
    key in the device data, fetched and processed by DataAggregationCoordinator.
    """

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Camera Sense Status sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._attr_unique_id = f"{self._device_serial}_camera_sense_status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)}
        )
        self.entity_description = SensorEntityDescription(
            key="camera_sense_status",
            name="Sense Enabled",
            native_unit_of_measurement=None,
            state_class=None,
        )

        self._update_sensor_data()

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state (native_value and icon) from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = None
            self._attr_icon = "mdi:help-rhombus"
            return

        sense_enabled_value = current_device_data.get("senseEnabled")

        if sense_enabled_value is None:
            self._attr_native_value = None
            self._attr_icon = "mdi:camera-question"
        else:
            sense_enabled = bool(sense_enabled_value)
            self._attr_native_value = "enabled" if sense_enabled else "disabled"
            self._attr_icon = "mdi:camera-iris" if sense_enabled else "mdi:camera-off-outline"

        self._attr_extra_state_attributes = {
            "serial_number": self._device_serial,
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_data()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available and data is present."""
        if not super().available:
            return False

        current_device_data = self._get_current_device_data()
        if not current_device_data:
            return False

        if "senseEnabled" not in current_device_data:
            return False

        return True

    # @property
    # def options(self) -> list[str] | None:
    #     return None
    #
    # @property
    # def suggested_unit_of_measurement(self) -> str | None:
    #     return None
    #
    # @property
    # def suggested_display_precision(self) -> int | None:
    #     return None
    #
    # @property
    # def last_reset(self) -> datetime | None:
    #     return None

    # Removed custom name property. Relies on _attr_has_entity_name and self.entity_description.name
    # for the entity-specific part of the name ("Sense Enabled").
    # The full friendly name is composed by Home Assistant using the device name.


class MerakiCameraAudioDetectionSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Camera Audio Detection Status sensor.

    This sensor entity displays the audio detection enabled status for a Meraki camera.
    It uses SensorEntityDescription to define its properties.
    The state ("enabled"/"disabled") is derived from the 'audioDetection.enabled'
    key in the device data, fetched and processed by DataAggregationCoordinator.
    """

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Camera Audio Detection sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_data["serial"]
        self._attr_unique_id = f"{self._device_serial}_camera_audio_detection_status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)}
        )
        self.entity_description = SensorEntityDescription(
            key="camera_audio_detection_status",
            name="Audio Detection",
            native_unit_of_measurement=None,
            state_class=None,
        )

        self._update_sensor_data()

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state (native_value and icon) from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = None
            self._attr_icon = "mdi:help-rhombus"
            return

        audio_detection_data = current_device_data.get("audioDetection")

        if not isinstance(audio_detection_data, dict) or "enabled" not in audio_detection_data:
            self._attr_native_value = None
            self._attr_icon = "mdi:microphone-question"
        else:
            audio_enabled = bool(audio_detection_data["enabled"])
            self._attr_native_value = "enabled" if audio_enabled else "disabled"
            self._attr_icon = "mdi:microphone" if audio_enabled else "mdi:microphone-off"

        self._attr_extra_state_attributes = {
            "serial_number": self._device_serial,
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_data()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available and data is present."""
        if not super().available:
            return False

        current_device_data = self._get_current_device_data()
        if not current_device_data:
            return False

        audio_data = current_device_data.get("audioDetection")
        if not isinstance(audio_data, dict) or "enabled" not in audio_data:
            return False

        return True

    # Removed custom name property. Relies on _attr_has_entity_name and self.entity_description.name.


class MerakiCameraRTSPUrlSensor(CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity):
    """Representation of a Meraki Camera RTSP URL Sensor.

    This sensor displays the RTSP URL for a Meraki camera when RTSP streaming
    is enabled on the camera.
    """

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
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

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)}
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
        current_device_data = None
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    current_device_data = dev_data
                    break

        if current_device_data:
            is_rtsp_enabled = current_device_data.get("externalRtspEnabled", False)
            rtsp_url = current_device_data.get("rtspUrl")

            if is_rtsp_enabled and rtsp_url:
                self._attr_native_value = rtsp_url
            else:
                self._attr_native_value = None
        else:
            self._attr_native_value = None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.last_update_success:
            return False

        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    if "externalRtspEnabled" not in dev_data:
                        return False
                    return True
        return False
