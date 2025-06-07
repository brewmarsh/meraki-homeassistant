"""Sensor entities for Meraki camera settings.

This module defines sensor entities for camera sense and audio detection status.
"""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
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

        # Placeholder for actual API data
        # sense_enabled = current_device_data.get("senseEnabled", False) # Example from API doc
        sense_enabled = True # Placeholder
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
        """Return True if entity is available."""
        if not super().available:
            return False
        if self.coordinator.data and self.coordinator.data.get("devices"):
            return any(
                dev.get("serial") == self._device_serial
                for dev in self.coordinator.data["devices"]
            )
        return False

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        # Fallback name if device_data or its name is not available
        device_name = "Camera"
        current_device_data = self._get_current_device_data()
        if current_device_data and current_device_data.get("name"):
            device_name = current_device_data.get("name")
        return f"{device_name} Sense Enabled"


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

        # Placeholder for actual API data
        # audio_detection_enabled = current_device_data.get("audioDetection", {}).get("enabled", False) # Example from API
        audio_detection_enabled = True # Placeholder
        self._attr_native_value = "enabled" if audio_detection_enabled else "disabled"
        self._attr_icon = "mdi:microphone" if audio_detection_enabled else "mdi:microphone-off"

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
        """Return True if entity is available."""
        if not super().available:
            return False
        if self.coordinator.data and self.coordinator.data.get("devices"):
            return any(
                dev.get("serial") == self._device_serial
                for dev in self.coordinator.data["devices"]
            )
        return False

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        device_name = "Camera" # Fallback name
        current_device_data = self._get_current_device_data()
        if current_device_data and current_device_data.get("name"):
            device_name = current_device_data.get("name")
        return f"{device_name} Audio Detection"
