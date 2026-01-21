"""Sensor for camera analytics."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from ...helpers.device_info_helpers import resolve_device_info
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

if TYPE_CHECKING:
    from ...services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiAnalyticsSensor(CoordinatorEntity, SensorEntity):
    """Base class for Meraki analytics sensors."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device: dict[str, Any],
        camera_service: CameraService,
=======
        coordinator: MerakiDataUpdateCoordinator,
        device: "MerakiDevice",
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        object_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
<<<<<<< HEAD
        self._camera_service = camera_service
        self._object_type = object_type
        self._attr_unique_id = f"{self._device['serial']}-{object_type}-count"
        self._attr_name = f"{self._device['name']} {object_type.capitalize()} Count"
        self._analytics_data: dict[str, Any] = {}
=======
        self._object_type = object_type
        self._attr_unique_id = f"{device.serial}-{object_type}-count"
        self._attr_name = f"[Camera] {device.name} {object_type.capitalize()} Count"
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
<<<<<<< HEAD
        return self._analytics_data.get(self._object_type)
=======
        device = self.coordinator.get_device(self._device.serial)
        if device and device.analytics:
            for reading in device.analytics:
                if reading.get("zoneId") == 0:  # Assuming zone 0 is the entire frame
                    return reading.get(f"{self._object_type}_count", 0)
        return 0
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
<<<<<<< HEAD
        if not self._analytics_data:
            return {}
        return {"raw_data": [self._analytics_data]}

    async def async_update(self) -> None:
        """Update the sensor."""
        serial = self._device["serial"]
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
=======
        device = self.coordinator.get_device(self._device.serial)
        if device and device.analytics:
            return {"raw_data": device.analytics}
        return {}
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


class MerakiPersonCountSensor(MerakiAnalyticsSensor):
    """Representation of a person count sensor."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device: dict[str, Any],
        camera_service: CameraService,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device, camera_service, "person")
=======
        coordinator: MerakiDataUpdateCoordinator,
        device: "MerakiDevice",
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device, "person")
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        self._attr_native_unit_of_measurement = "people"


class MerakiVehicleCountSensor(MerakiAnalyticsSensor):
    """Representation of a vehicle count sensor."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device: dict[str, Any],
        camera_service: CameraService,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device, camera_service, "vehicle")
=======
        coordinator: MerakiDataUpdateCoordinator,
        device: "MerakiDevice",
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device, "vehicle")
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        self._attr_native_unit_of_measurement = "vehicles"
