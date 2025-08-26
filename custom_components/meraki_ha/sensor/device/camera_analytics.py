"""
Sensor entities for camera analytics.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator

if TYPE_CHECKING:
    from ...services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiAnalyticsSensor(CoordinatorEntity[MerakiDataCoordinator], SensorEntity):
    """Base class for Meraki analytics sensors."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Dict[str, Any],
        camera_service: CameraService,
        object_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._camera_service = camera_service
        self._object_type = object_type
        self._attr_unique_id = f"{self._device['serial']}-{object_type}-count"
        self._attr_name = (
            f"{self._device['name']} {object_type.capitalize()} Count"
        )
        self._analytics_data: Dict[str, Any] = {}

    @property
    def native_value(self) -> Optional[int]:
        """Return the state of the sensor."""
        if not self._analytics_data:
            return None
        # Assuming a single zone for simplicity. In a real scenario, this might
        # need to aggregate data from multiple zones.
        return self._analytics_data[0].get(self._object_type)

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        if not self._analytics_data:
            return {}
        return {"raw_data": self._analytics_data}

    async def async_update(self) -> None:
        """Update the sensor."""
        serial = self._device["serial"]
        try:
            self._analytics_data = (
                await self._camera_service.get_analytics_data(
                    serial, self._object_type
                )
            )
        except Exception as e:
            _LOGGER.error(
                "Error updating analytics sensor for %s: %s", serial, e
            )
            self._analytics_data = {}


class MerakiPersonCountSensor(MerakiAnalyticsSensor):
    """Representation of a person count sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Dict[str, Any],
        camera_service: CameraService,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device, camera_service, "person")
        self._attr_native_unit_of_measurement = "people"


class MerakiVehicleCountSensor(MerakiAnalyticsSensor):
    """Representation of a vehicle count sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Dict[str, Any],
        camera_service: CameraService,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device, camera_service, "vehicle")
        self._attr_native_unit_of_measurement = "vehicles"
