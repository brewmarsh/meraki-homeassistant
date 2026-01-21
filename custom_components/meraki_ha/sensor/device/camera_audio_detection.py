"""Sensor entity for Meraki camera audio detection status."""

<<<<<<< HEAD
import logging
from typing import Any
=======
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
<<<<<<< HEAD
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name

if TYPE_CHECKING:
    from ...types import MerakiDevice
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

_LOGGER = logging.getLogger(__name__)


class MerakiCameraAudioDetectionSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Camera Audio Detection Status sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device_data: dict[str, Any],
=======
        coordinator: MerakiDataUpdateCoordinator,
        device_data: MerakiDevice,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Camera Audio Detection sensor."""
        super().__init__(coordinator)
<<<<<<< HEAD
        self._device_serial: str = device_data["serial"]
=======
        self._device_serial: str = device_data.serial
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        self._attr_unique_id = f"{self._device_serial}_camera_audio_detection_status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(device_data, config_entry.options),
<<<<<<< HEAD
            model=device_data.get("model"),
=======
            model=device_data.model,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            manufacturer="Cisco Meraki",
        )
        self.entity_description = SensorEntityDescription(
            key="camera_audio_detection_status",
            name="Audio Detection",
            native_unit_of_measurement=None,
            state_class=None,
        )

        self._update_sensor_data()

<<<<<<< HEAD
    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    return dev_data
        return None
=======
    def _get_current_device_data(self) -> MerakiDevice | None:
        """Retrieve the latest data for this sensor's device from the coordinator."""
        return self.coordinator.get_device(self._device_serial)
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    def _update_sensor_data(self) -> None:
        """Update sensor state (native_value and icon) from coordinator data."""
        current_device_data = self._get_current_device_data()

        if not current_device_data:
            self._attr_native_value = None
            self._attr_icon = "mdi:help-rhombus"
            return

<<<<<<< HEAD
        audio_detection_data = current_device_data.get("audioDetection")
=======
        # Audio detection is part of sense settings
        sense_settings = getattr(current_device_data, "sense_settings", None)

        if not isinstance(sense_settings, dict):
             self._attr_native_value = None
             self._attr_icon = "mdi:microphone-question"
             return

        audio_detection_data = sense_settings.get("audioDetection")
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

        if (
            not isinstance(audio_detection_data, dict)
            or "enabled" not in audio_detection_data
        ):
            self._attr_native_value = None
            self._attr_icon = "mdi:microphone-question"
        else:
            audio_enabled = bool(audio_detection_data["enabled"])
            self._attr_native_value = "enabled" if audio_enabled else "disabled"
            self._attr_icon = (
                "mdi:microphone" if audio_enabled else "mdi:microphone-off"
            )

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

<<<<<<< HEAD
        audio_data = current_device_data.get("audioDetection")
=======
        sense_settings = getattr(current_device_data, "sense_settings", None)
        if not isinstance(sense_settings, dict):
            return False

        audio_data = sense_settings.get("audioDetection")
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if not isinstance(audio_data, dict) or "enabled" not in audio_data:
            return False

        return True
