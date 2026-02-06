"""Switch entity for controlling Meraki Switch Ports."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.models.device import MerakiDevice
from ..entity import MerakiEntity
from ..helpers.device_info_helpers import resolve_device_info


class MerakiSwitchPortSwitch(MerakiEntity, SwitchEntity):
    """Representation of a Meraki Switch Port switch."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device = device
        self._port = port

        # Identify port ID (number for MX, portId for MS)
        # Since this is for SwitchPortProvider, it usually comes from ports_statuses
        self._port_id = str(self._port.get("portId") or self._port.get("number"))

        # Unique ID: {serial}_port_{port_id}_switch
        self._attr_unique_id = f"{device.serial}_port_{self._port_id}_switch"
        self._attr_name = f"Port {self._port_id} Enabled"
        self._attr_has_entity_name = True

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        return self._attr_unique_id

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    @property
    def is_on(self) -> bool | None:
        """Return True if the switch is on."""
        return self._port.get("enabled", False)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self._device.status == "online"
            and self._device.serial is not None
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Find updated device
        new_device = self.coordinator.get_device(self._device.serial)
        if not new_device:
            return

        self._device = new_device

        # Find updated port in ports_statuses
        ports = self._device.ports_statuses or []
        for port in ports:
            p_id = str(port.get("portId") or port.get("number"))
            if p_id == self._port_id:
                self._port = port
                self.async_write_ha_state()
                break

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._set_port_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._set_port_state(False)

    async def _set_port_state(self, enabled: bool) -> None:
        """Set the port state."""
        # Optimistic update
        self._port["enabled"] = enabled
        self.async_write_ha_state()

        # Call API
        try:
            await self.coordinator.api.switch.update_device_switch_port(
                self._device.serial,
                self._port_id,
                enabled=enabled,
            )
        except Exception:
            # Revert state on failure
            self._port["enabled"] = not enabled
            self.async_write_ha_state()
            raise
