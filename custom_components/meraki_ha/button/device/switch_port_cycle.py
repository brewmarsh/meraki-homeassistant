"""
Meraki-HA button platform.

This module defines the MerakiSwitchPortCycleButton class, a button entity
for cycling a switch port.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from ...core.utils.naming_utils import format_entity_name
from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...services.switch_port_service import SwitchPortService
    from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiSwitchPortCycleButton(ButtonEntity):
    """A button to cycle a switch port."""

    def __init__(
        self,
        switch_port_service: SwitchPortService,
        device: MerakiDevice,
        config_entry: ConfigEntry,
        port_id: str,
        port_info: dict[str, Any],
    ) -> None:
        """Initialize the switch port cycle button."""
        self._service = switch_port_service
        self._device = device
        self._config_entry = config_entry
        self._port_id = port_id
        self._port_info = port_info

        self._attr_name = format_entity_name(
            device, config_entry.options, f"Cycle Port {port_id}"
        )
        self._attr_unique_id = f"{device.serial}_cycle_port_{port_id}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return resolve_device_info(self._device, self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._service.async_cycle_port(self._device.serial, self._port_id)
