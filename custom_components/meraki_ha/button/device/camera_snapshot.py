"""
Button entity for taking a camera snapshot.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator

if TYPE_CHECKING:
    from ...services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiSnapshotButton(CoordinatorEntity[MerakiDataCoordinator], ButtonEntity):
    """Representation of a snapshot button."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Dict[str, Any],
        camera_service: CameraService,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._device = device
        self._camera_service = camera_service
        self._attr_unique_id = f"{self._device['serial']}-snapshot"
        self._attr_name = f"{self._device['name']} Snapshot"

    async def async_press(self) -> None:
        """Handle the button press."""
        serial = self._device["serial"]
        _LOGGER.info("Snapshot button pressed for %s", serial)
        try:
            url = await self._camera_service.generate_snapshot(serial)
            if url:
                _LOGGER.info("Snapshot URL for %s: %s", serial, url)
            else:
                _LOGGER.warning("Failed to get snapshot URL for %s", serial)
        except Exception as e:
            _LOGGER.error("Error generating snapshot for %s: %s", serial, e)
