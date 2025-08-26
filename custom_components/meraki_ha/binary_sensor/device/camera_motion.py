"""
Binary sensor for camera motion.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, Optional

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
    from ....services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiMotionSensor(CoordinatorEntity[MerakiDataCoordinator], BinarySensorEntity):
    """Representation of a motion sensor."""

    _attr_device_class = BinarySensorDeviceClass.MOTION

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
        self._attr_unique_id = f"{self._device['serial']}-motion"
        self._attr_name = f"{self._device['name']} Motion"

    @property
    def is_on(self) -> Optional[bool]:
        """Return true if the binary sensor is on."""
        # This will be implemented later
        return None
