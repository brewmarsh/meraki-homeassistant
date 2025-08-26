"""
Sensor entities for camera analytics.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ...services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiPersonCountSensor(CoordinatorEntity[MerakiDataCoordinator], SensorEntity):
    """Representation of a person count sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Dict[str, Any],
        camera_service: CameraService,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._camera_service = camera_service
        self._attr_unique_id = f"{self._device['serial']}-person-count"
        self._attr_name = f"{self._device['name']} Person Count"
        self._attr_native_unit_of_measurement = "people"

    @property
    def native_value(self) -> Optional[int]:
        """Return the state of the sensor."""
        # This will be implemented later
        return None


class MerakiVehicleCountSensor(CoordinatorEntity[MerakiDataCoordinator], SensorEntity):
    """Representation of a vehicle count sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Dict[str, Any],
        camera_service: CameraService,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._camera_service = camera_service
        self._attr_unique_id = f"{self._device['serial']}-vehicle-count"
        self._attr_name = f"{self._device['name']} Vehicle Count"
        self._attr_native_unit_of_measurement = "vehicles"

    @property
    def native_value(self) -> Optional[int]:
        """Return the state of the sensor."""
        # This will be implemented later
        return None
