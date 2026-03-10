"""
Meraki-HA button platform.

This module defines the MerakiRebootButton class, a generic button entity
for rebooting Meraki devices.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ..const.device import DEFAULT_CAPS, DEVICE_CAPABILITIES
from ..entity import MerakiEntity
from ..helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ..coordinators import MerakiDeviceCoordinator
    from ..core.models.device import MerakiDevice
    from ..services.device_control_service import DeviceControlService

_LOGGER = logging.getLogger(__name__)


class MerakiRebootButton(MerakiEntity, ButtonEntity):
    """A button to reboot a Meraki device."""

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        control_service: DeviceControlService,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the reboot button."""
        super().__init__(coordinator)
        self._control_service = control_service
        self._device = device
        self._config_entry = config_entry
        self._attr_name = "Reboot"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return resolve_device_info(self._device, self._config_entry)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # 1. Check parent availability (ensures coordinator has data)
        # We don't call super().available because we want reboot to work
        # even if device is 'offline'
        if not self.coordinator.data:
            _LOGGER.warning("[%s] Unavailable: coordinator.data is empty", self.name)
            return False

        if not self._serial:
            _LOGGER.warning("[%s] Unavailable: serial missing", self.name)
            return False

        device = self.device_data
        if device is None:
            _LOGGER.warning(
                "[%s] Unavailable: device_data is None for serial %s",
                self.name,
                self._serial,
            )
            return False

        # 2. Check static hardware capabilities based on device model
        # Strip suffixes like "-8LP" or " HW" to get the base model (e.g., "MS120")
        model_str = (
            self._device.get("model", "")
            if isinstance(self._device, dict)
            else getattr(self._device, "model", "")
        ) or ""
        model = model_str.split("-")[0].split(" ")[0]

        # Use DEFAULT_CAPS to assume basic network gear can reboot if model
        # isn't hardcoded.
        capabilities = DEVICE_CAPABILITIES.get(model, DEFAULT_CAPS)
        has_reboot = "reboot" in capabilities
        if not has_reboot:
            _LOGGER.warning(
                "[%s] Unavailable: reboot capability missing for model %s",
                self.name,
                model,
            )
        return has_reboot

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if device := self.device_data:
            self._device = device
        super()._handle_coordinator_update()

    async def async_press(self) -> None:
        """Handle the button press."""
        if serial := self._serial:
            await self._control_service.async_reboot(serial)
