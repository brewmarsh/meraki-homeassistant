"""Switch entity for Meraki switch ports."""

from __future__ import annotations

import logging
from typing import Any, cast

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory

from ..const import DOMAIN
from ..coordinator import MerakiDataUpdateCoordinator
from ..core.models.device import MerakiDevice
from ..entity import MerakiEntity

_LOGGER = logging.getLogger(__name__)


class MerakiSwitchPortSwitch(MerakiEntity, SwitchEntity):
    """Representation of a Meraki switch port switch."""

    entity_description: SwitchEntityDescription
    _attr_entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._config_entry = config_entry

        port_id = self._port.get("portId") or self._port.get("number")

        self.entity_description = SwitchEntityDescription(
            key=f"port_{port_id}_enabled",
            name=f"Port {port_id}",
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
        for device in self.coordinator.data.get("devices", []):
            if device.serial == self._device.serial:
                self._device = device
                for port in self._device.ports_statuses:
                    port_id = self._port.get("portId") or self._port.get("number")
                    if port.get("portId") == port_id or port.get("number") == port_id:
                        self._port = port
                        break
                break
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch."""
        # Use optimistic state if pending update
        if self.unique_id and self.coordinator.is_pending(self.unique_id):
            return

        self._attr_is_on = self._port.get("enabled", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._set_port_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._set_port_state(False)

    async def _set_port_state(self, enabled: bool) -> None:
        """Set the port state."""
        port_id = self._port.get("portId") or self._port.get("number")
        if not port_id:
            _LOGGER.error("Port ID missing for %s", self.name)
            return

        # Optimistic update
        self._attr_is_on = enabled
        self.async_write_ha_state()

        try:
            await self.coordinator.api.switch.update_device_switch_port(
                serial=self._device.serial,
                port_id=str(port_id),
                enabled=enabled,
            )
            if self.unique_id:
                self.coordinator.register_pending_update(self.unique_id)
        except Exception as e:
            _LOGGER.error(
                "Failed to set port %s state for device %s: %s",
                port_id,
                self._device.serial,
                e,
            )
            # Revert state on failure
            self._update_internal_state()
            self.async_write_ha_state()
