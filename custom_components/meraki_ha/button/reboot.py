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
from homeassistant.helpers.entity import DeviceInfo

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
        if not super().available:
            return False

        device = self.coordinator.get_device(self._device.serial)
        is_avail = device is not None
        if not is_avail:
            _LOGGER.debug(
                "Reboot Button %s unavailable: device %s not found in coordinator",
                self.unique_id,
                self._device.serial,
            )
        return is_avail

    async def async_press(self) -> None:
        """Handle the button press."""
        if self._device.serial:
            await self._control_service.async_reboot(self._device.serial)
