"""Binary sensor for Meraki camera person detection."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry

from ...coordinators import MerakiCameraCoordinator
from ...entity import MerakiBinarySensor

if TYPE_CHECKING:
    from ...core.models.device import MerakiDevice
    from ...services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiPersonSensor(MerakiBinarySensor):
    """Representation of a person detection sensor."""

    _attr_device_class = BinarySensorDeviceClass.MOTION

    def __init__(
        self,
        coordinator: MerakiCameraCoordinator,
        device: MerakiDevice,
        camera_service: CameraService,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._device_serial = device.serial
        self._camera_service = camera_service
        self._config_entry = config_entry
        self._attr_unique_id = f"{device.serial}-person"
        self._attr_name = "Person"

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        device = self.device_data
        if not device or not getattr(device, "last_person_detected_event", None):
            return False

        import time

        last_event = device.last_person_detected_event
        last_event_time = last_event.get("timestamp", 0)
        # Check if the event happened within the last 30 seconds
        return (time.time() - last_event_time) < 30

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        device = self.device_data
        if not device:
            return {}
        return {
            "last_person_detected_event": getattr(
                device, "last_person_detected_event", None
            )
        }
