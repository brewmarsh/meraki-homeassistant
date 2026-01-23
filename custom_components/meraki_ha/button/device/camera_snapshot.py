"""Button entity for taking a camera snapshot."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_entity_name
from ...helpers.device_info_helpers import resolve_device_info
from ...types import MerakiDevice

if TYPE_CHECKING:
    from ...services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiSnapshotButton(CoordinatorEntity, ButtonEntity):
    """Representation of a snapshot button."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        camera_service: CameraService,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._device = device
        self._camera_service = camera_service
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device.serial}-snapshot"
        self._attr_name = format_entity_name(device, config_entry.options, "Snapshot")

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        serial = self._device.serial
        _LOGGER.info("Snapshot button pressed for %s", serial)
        try:
            url = await self._camera_service.generate_snapshot(str(serial))
            if url:
                _LOGGER.info("Snapshot URL for %s: %s", serial, url)
            else:
                _LOGGER.warning("Failed to get snapshot URL for %s", serial)
        except Exception as e:
            _LOGGER.error("Error generating snapshot for %s: %s", serial, e)
