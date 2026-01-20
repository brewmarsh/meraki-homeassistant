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
        device: dict[str, Any] | Any,
        camera_service: CameraService,
        object_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._camera_service = camera_service
        self._object_type = object_type
        serial = device.serial if hasattr(device, "serial") else device["serial"]
        name = device.name if hasattr(device, "name") else device["name"]
        self._attr_unique_id = f"{serial}-{object_type}-count"
        self._attr_name = f"[Camera] {name} {object_type.capitalize()} Count"
        self._analytics_data: dict[str, Any] = {}

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        return self._analytics_data.get(self._object_type)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self._analytics_data:
            return {}
        return {"raw_data": [self._analytics_data]}

    async def async_update(self) -> None:
        """Update the sensor."""
        serial = (
            self._device.serial
            if hasattr(self._device, "serial")
            else self._device["serial"]
        )
        try:
            analytics_data = await self._camera_service.get_analytics_data(
                serial, self._object_type
            )
            if isinstance(analytics_data, list) and analytics_data:
                self._analytics_data = analytics_data[0]
            else:
                self._analytics_data = {}
        except Exception as e:
            _LOGGER.error("Error updating analytics sensor for %s: %s", serial, e)
            self._analytics_data = {}


class MerakiPersonCountSensor(MerakiAnalyticsSensor):
    """Representation of a person count sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: dict[str, Any] | Any,
        camera_service: CameraService,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device, camera_service, "person")
        self._attr_native_unit_of_measurement = "people"


class MerakiVehicleCountSensor(MerakiAnalyticsSensor):
    """Representation of a vehicle count sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: dict[str, Any] | Any,
        camera_service: CameraService,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device, camera_service, "vehicle")
        self._attr_native_unit_of_measurement = "vehicles"
