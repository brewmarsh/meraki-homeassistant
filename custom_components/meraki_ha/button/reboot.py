"""
Meraki-HA button platform.

This module defines the MerakiRebootButton class, a generic button entity
for rebooting Meraki devices.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from ..helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ..services.device_control_service import DeviceControlService
    from ..types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiRebootButton(ButtonEntity):

    """A button to reboot a Meraki device."""

    def __init__(
        self,
        control_service: DeviceControlService,
        device: MerakiDevice,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the reboot button."""
        self._control_service = control_service
        self._device = device
        self._config_entry = config_entry
        self._attr_name = f"{device.get('name', 'Device')} Reboot"
        self._attr_unique_id = f"{device['serial']}-reboot"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return resolve_device_info(cast(dict, self._device), self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._control_service.async_reboot(self._device["serial"])
