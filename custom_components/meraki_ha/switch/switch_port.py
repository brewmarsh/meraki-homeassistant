"""Switch entity for controlling Meraki Switch Ports."""

from __future__ import annotations

from typing import Any, cast

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import DOMAIN
from ..coordinator import MerakiDataUpdateCoordinator
from ..core.models.device import MerakiDevice
from ..entity import MerakiEntity


class MerakiSwitchPortSwitch(MerakiEntity, SwitchEntity):
    """Representation of a Meraki Switch Port switch."""

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

        self._attr_has_entity_name = True
        self._attr_entity_category = EntityCategory.CONFIG

        port_id = self._port.get("portId") or self._port.get("number")
        self._attr_unique_id = f"{self._device.serial}_port_{port_id}_enabled"
        self._attr_name = f"Port {port_id} Enabled"

        self.entity_description = SwitchEntityDescription(
            key=f"port_{port_id}_enabled",
            name=f"Port {port_id} Enabled",
            icon="mdi:ethernet",
        )

        self._update_internal_state()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, cast(str, self._device.serial))},
        )

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return self._device.status == "online"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch based on coordinator data."""
        if self.unique_id and self.coordinator.is_pending(self.unique_id):
            return

        for device in self.coordinator.data.get("devices", []):
            if device.serial == self._device.serial:
                self._device = device
                for port in self._device.ports_statuses:
                    port_id = self._port.get("portId") or self._port.get("number")
                    if port.get("portId") == port_id or port.get("number") == port_id:
                        self._port = port
                        break
                break

        self._attr_is_on = self._port.get("enabled", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._update_port(enabled=True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._update_port(enabled=False)

    async def _update_port(self, **kwargs: Any) -> None:
        """Update the port settings."""
        port_id = self._port.get("portId") or self._port.get("number")

        # Optimistic update
        if "enabled" in kwargs:
            self._attr_is_on = kwargs["enabled"]
            self.async_write_ha_state()

        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

        await self.coordinator.api.switch.update_device_switch_port(
            serial=cast(str, self._device.serial),
            port_id=str(port_id),
            **kwargs,
        )
