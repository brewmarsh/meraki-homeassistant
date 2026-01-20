"""
Meraki Switch Port Cycle Button.

This module defines the MerakiSwitchPortCycleButton class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from ...helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ...services.switch_port_service import SwitchPortService
    from ...types import MerakiDevice


class MerakiSwitchPortCycleButton(ButtonEntity):
    """A button to cycle a Meraki switch port."""

    def __init__(
        self,
        service: SwitchPortService,
        device: MerakiDevice,
        port_info: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the switch port cycle button."""
        self._service = service
        self._device = device
        self._port_id = port_info["portId"]
        self._port_number = port_info.get("portId")  # Meraki uses portId as number usually
        self._config_entry = config_entry

        self._attr_name = f"{device.name} Port {self._port_id} Cycle"
        self._attr_unique_id = f"{device.serial}_port_{self._port_id}_cycle"
        self._attr_icon = "mdi:restart"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return resolve_device_info(self._device, self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._service.async_cycle_ports(self._device.serial, [self._port_id])
