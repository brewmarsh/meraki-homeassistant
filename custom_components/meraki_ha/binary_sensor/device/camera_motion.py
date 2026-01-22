"""Binary sensor for Meraki camera motion detection."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...services.camera_service import CameraService
    from ...types import MerakiDevice


_LOGGER = logging.getLogger(__name__)


class MerakiMotionSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a motion sensor."""

    _attr_device_class = BinarySensorDeviceClass.MOTION

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        camera_service: CameraService,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._camera_service = camera_service
        self._config_entry = config_entry
        self._attr_unique_id = f"{device.serial}-motion"
        self._attr_has_entity_name = True
        self._attr_name = "Motion"
        self._motion_events: list[dict[str, Any]] = []

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self._config_entry)

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return len(self._motion_events) > 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {"motion_events": self._motion_events}

    async def async_update(self) -> None:
        """Update the sensor."""
        if not self._device.serial:
            return
        try:
            self._motion_events = await self._camera_service.get_motion_history(
                self._device.serial
            )
        except Exception as e:
            _LOGGER.error(
                "Error updating motion sensor for %s: %s", self._device.serial, e
            )
            self._motion_events = []
