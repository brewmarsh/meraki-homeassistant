"""Meraki Switch Port Cycle Button."""

from __future__ import annotations

from typing import Any

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ...coordinator import MerakiDataUpdateCoordinator
from ...core.models.device import MerakiDevice
from ...entity import MerakiEntity
from ...helpers.device_info_helpers import resolve_device_info


class MerakiPoECycleButton(MerakiEntity, ButtonEntity):
    """A button to cycle a Meraki switch port."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the switch port cycle button."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._config_entry = config_entry

        port_id = self._port.get("portId") or self._port.get("number")
        self.entity_description = ButtonEntityDescription(
            key=f"port_cycle_{port_id}",
            name=f"Port {port_id} cycle",
            icon="mdi:restart",
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return resolve_device_info(self._device, self._config_entry)

    async def async_press(self) -> None:
        """Handle the button press."""
        port_id = self._port.get("portId") or self._port.get("number")
        await self.coordinator.api.switch.cycle_device_switch_ports(
            serial=str(self._device.serial),
            ports=[str(port_id)],
        )
