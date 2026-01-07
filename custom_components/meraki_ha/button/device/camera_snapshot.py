"""Button entity for taking a camera snapshot."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...helpers.device_info_helpers import resolve_device_info
from ...meraki_data_coordinator import MerakiDataCoordinator

if TYPE_CHECKING:
    from ...services.camera_service import CameraService


_LOGGER = logging.getLogger(__name__)


class MerakiSnapshotButton(CoordinatorEntity, ButtonEntity):
    """Representation of a snapshot button."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Mapping[str, Any],
        camera_service: CameraService,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._device = device
        self._camera_service = camera_service
        self._config_entry = config_entry
        self._attr_unique_id = f"{self._device['serial']}-snapshot"
        self._attr_name = f"{self._device['name']} Snapshot"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self._config_entry)

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device["serial"]:
                    return dev_data
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        current_data = self._get_current_device_data()
        if current_data:
            self._device = current_data
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not super().available:
            return False
        return self._get_current_device_data() is not None

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
