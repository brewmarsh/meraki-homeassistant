"""Sensor entities for Meraki camera settings.

This module defines sensor entities for camera sense and audio detection status.
"""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityDescription # Corrected import path
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinators import MerakiDataUpdateCoordinator
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiCameraSenseStatusSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Camera Sense Status sensor."""

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
        self.entity_description = EntityDescription(
            key="camera_sense_status",
            name="Sense Enabled"
        )
        self._update_sensor_data()
        _LOGGER.debug(
            "MerakiCameraSenseStatusSensor Initialized for %s (Serial: %s)",
            device_data.get("name", self._device_serial),
            self._device_serial,
        )

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        # This will be updated later to fetch actual camera sense data
        # For now, return the base device data
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    # Placeholder: In the future, this should merge/fetch specific sense API data
                    return dev_data
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
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

    # Removed custom name property. Relies on _attr_has_entity_name and self.entity_description.name.


class MerakiCameraAudioDetectionSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Camera Audio Detection Status sensor."""

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
        self.entity_description = EntityDescription(
            key="camera_audio_detection_status",
            name="Audio Detection"
        )
        self._update_sensor_data()
        _LOGGER.debug(
            "MerakiCameraAudioDetectionSensor Initialized for %s (Serial: %s)",
            device_data.get("name", self._device_serial),
            self._device_serial,
        )

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        # This will be updated later to fetch actual camera audio detection data
        # For now, return the base device data
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    # Placeholder: In the future, this should merge/fetch specific audio API data
                    return dev_data
        return None

    def _update_sensor_data(self) -> None:
        """Update sensor state from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
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
