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
from homeassistant.helpers.entity import DeviceInfo

from ..const.device import DEVICE_CAPABILITIES
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
        # Check base availability (coordinator data presence)
        if not self.coordinator.data or not self._serial:
            return False

        if self.device_data is None:
            return False

        # Check static hardware capabilities based on device model
        model = (self._device.model or "").split(" ")[0]  # Take first part of model name
        capabilities = DEVICE_CAPABILITIES.get(model, [])
        return "reboot" in capabilities

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
