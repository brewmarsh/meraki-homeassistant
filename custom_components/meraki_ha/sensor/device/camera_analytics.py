"""Sensor for camera analytics."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiAnalyticsSensor(CoordinatorEntity, SensorEntity):
    """Base class for Meraki analytics sensors."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: "MerakiDevice",
        object_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._object_type = object_type
        self._attr_unique_id = f"{device.serial}-{object_type}-count"
        self._attr_name = f"[Camera] {device.name} {object_type.capitalize()} Count"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        device = self.coordinator.get_device(self._device.serial)
        if device and device.analytics:
            for reading in device.analytics:
                if reading.get("zoneId") == 0:  # Assuming zone 0 is the entire frame
                    return reading.get(f"{self._object_type}_count", 0)
        return 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        device = self.coordinator.get_device(self._device.serial)
        if device and device.analytics:
            return {"raw_data": device.analytics}
        return {}


class MerakiPersonCountSensor(MerakiAnalyticsSensor):
    """Representation of a person count sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: "MerakiDevice",
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device, "person")
        self._attr_native_unit_of_measurement = "people"


class MerakiVehicleCountSensor(MerakiAnalyticsSensor):
    """Representation of a vehicle count sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: "MerakiDevice",
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device, "vehicle")
        self._attr_native_unit_of_measurement = "vehicles"
