"""Sensor entities for Meraki camera settings.

This module defines sensor entities for camera sense and audio detection status.
"""

import logging
from typing import Any, Dict, Optional
from datetime import datetime # Added import

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription # Updated import
from homeassistant.core import callback
# from homeassistant.helpers.entity import EntityDescription # No longer needed
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinators import MerakiDataUpdateCoordinator # Ensure this is the correct path
from ..const import DOMAIN

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
            name="Sense Enabled",  # This name is used by HA to generate the friendly name
            native_unit_of_measurement=None, # Categorical sensor, no unit
            state_class=None, # Categorical sensor
            # icon can also be defined here if static, e.g., icon="mdi:camera-iris"
        )
        # Explicitly set attributes that are not part of SensorEntityDescription
        # or need to be None for this sensor type.
        # self._attr_state_class = None # Now handled by SensorEntityDescription
        # self._attr_native_unit_of_measurement = None # Now handled by SensorEntityDescription

        # The following properties are overridden to return None, as they are not applicable.
        # - options
        # - suggested_unit_of_measurement (already None via SensorEntityDescription)
        # - suggested_display_precision
        # - last_reset
        # Their explicit @property methods have been removed.

        self._update_sensor_data()
        _LOGGER.debug(
            "MerakiCameraSenseStatusSensor Initialized for %s (Serial: %s)",
            device_data.get("name", self._device_serial),
            self._device_serial,
        )

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator.

        The coordinator's data is expected to have camera-specific settings already merged.
        """
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state (native_value and icon) from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data: # Should be caught by `available` property first
            self._attr_native_value = None
            self._attr_icon = "mdi:help-rhombus"
            return

        sense_enabled_value = current_device_data.get("senseEnabled")

        if sense_enabled_value is None: # Explicitly check for None, as False is a valid state
            self._attr_native_value = None # Or "unknown"
            self._attr_icon = "mdi:camera-question" # Icon indicating data is missing
            _LOGGER.debug("senseEnabled data not found for %s", self._device_serial)
        else:
            sense_enabled = bool(sense_enabled_value)
            self._attr_native_value = "enabled" if sense_enabled else "disabled"
            self._attr_icon = "mdi:camera-iris" if sense_enabled else "mdi:camera-off-outline"

        self._attr_extra_state_attributes = {
            "serial_number": self._device_serial,
            # Add other relevant attributes if needed
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_data()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available and data is present."""
        if not super().available: # Checks coordinator's last_update_success
            return False

        current_device_data = self._get_current_device_data()
        if not current_device_data:
            return False # Device not in coordinator data

        # Check for presence of the specific attribute this sensor relies on
        if "senseEnabled" not in current_device_data:
            _LOGGER.debug("Sensor %s unavailable, senseEnabled missing from device data", self.unique_id)
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
            name="Audio Detection", # This name is used by HA
            native_unit_of_measurement=None, # Categorical sensor
            state_class=None, # Categorical sensor
            # icon can also be defined here if static, e.g., icon="mdi:microphone-settings"
        )
        # Explicitly set attributes that are not part of SensorEntityDescription
        # or need to be None for this sensor type.
        # self._attr_state_class = None # Now handled by SensorEntityDescription
        # self._attr_native_unit_of_measurement = None # Now handled by SensorEntityDescription

        # The following properties are overridden to return None, as they are not applicable.
        # - options
        # - suggested_unit_of_measurement (already None via SensorEntityDescription)
        # - suggested_display_precision
        # - last_reset
        # Their explicit @property methods have been removed.

        self._update_sensor_data()
        _LOGGER.debug(
            "MerakiCameraAudioDetectionSensor Initialized for %s (Serial: %s)",
            device_data.get("name", self._device_serial),
            self._device_serial,
        )

    # @property
    # def options(self) -> list[str] | None: # Commented out, was "Added options here"
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

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator.

        The coordinator's data is expected to have camera-specific settings already merged.
        """
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state (native_value and icon) from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data: # Should be caught by `available` property first
            self._attr_native_value = None
            self._attr_icon = "mdi:help-rhombus"
            return

        audio_detection_data = current_device_data.get("audioDetection")

        if not isinstance(audio_detection_data, dict) or "enabled" not in audio_detection_data:
            self._attr_native_value = None # Or "unknown"
            self._attr_icon = "mdi:microphone-question" # Icon indicating data is missing/malformed
            _LOGGER.debug("audioDetection.enabled data not found or malformed for %s", self._device_serial)
        else:
            audio_enabled = bool(audio_detection_data["enabled"])
            self._attr_native_value = "enabled" if audio_enabled else "disabled"
            self._attr_icon = "mdi:microphone" if audio_enabled else "mdi:microphone-off"

        self._attr_extra_state_attributes = {
            "serial_number": self._device_serial,
            # Add other relevant attributes if needed
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_data()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available and data is present."""
        if not super().available: # Checks coordinator's last_update_success
            return False

        current_device_data = self._get_current_device_data()
        if not current_device_data:
            return False # Device not in coordinator data

        # Check for presence and correct structure of the specific attribute
        audio_data = current_device_data.get("audioDetection")
        if not isinstance(audio_data, dict) or "enabled" not in audio_data:
            _LOGGER.debug("Sensor %s unavailable, audioDetection.enabled missing/malformed", self.unique_id)
            return False

        return True

    # Removed custom name property. Relies on _attr_has_entity_name and self.entity_description.name.


class MerakiCameraRTSPUrlSensor(CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity):
    """Representation of a Meraki Camera RTSP URL Sensor.

    This sensor displays the RTSP URL for a Meraki camera when RTSP streaming
    is enabled on the camera.
    """

    _attr_has_entity_name = True # Uses device name + entity_description.name

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info_data: Dict[str, Any], # This is the camera's device data from the coordinator
    ) -> None:
        """Initialize the Meraki Camera RTSP URL Sensor."""
        super().__init__(coordinator)
        self._device_serial: str = device_info_data["serial"]

        self.entity_description = SensorEntityDescription(
            key="rtsp_url",
            name="RTSP Stream URL",
            icon="mdi:video-stream", # Using an icon related to video streaming
        )

        self._attr_unique_id = f"{self._device_serial}_{self.entity_description.key}"

        # Link this sensor to the same camera device as the switch
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)}
        )

        # Initialize state
        self._update_state()
        _LOGGER.debug(
            "%s initialized for %s (Serial: %s)",
            self.__class__.__name__,
            device_info_data.get("name", self._device_serial),
            self._device_serial,
        )

    @property
    def native_value(self) -> Optional[str]:
        """Return the state of the sensor (the RTSP URL or None)."""
        # _attr_native_value is updated by _update_state
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
                self._attr_native_value = None # Or an empty string, or "Unavailable"
        else:
            self._attr_native_value = None # Or an empty string
            _LOGGER.debug(
                "Device data for serial '%s' not found in coordinator for sensor '%s'.",
                self._device_serial,
                self.unique_id,
            )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # Availability is determined by the coordinator's success and presence of device data.
        # The actual value being None if RTSP is off is handled by the sensor's state.
        if not self.coordinator.last_update_success:
            return False

        # Check if the device data itself is present in the coordinator
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    # Check for the presence of the keys this sensor relies on,
                    # even if their values might lead to a None state.
                    # If externalRtspEnabled is missing, we can't determine if URL should be shown.
                    if "externalRtspEnabled" not in dev_data:
                         _LOGGER.debug("Sensor %s unavailable, externalRtspEnabled missing from coordinator data", self.unique_id)
                         return False
                    # rtspUrl can be optional if not enabled, so its absence when externalRtspEnabled is false is fine.
                    return True
        return False
