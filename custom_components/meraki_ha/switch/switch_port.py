"""Switch entity for controlling Meraki Switch Ports."""

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
    """Representation of a Meraki Switch Port switch entity."""

    entity_category = EntityCategory.CONFIG
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Switch Port switch entity."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._config_entry = config_entry

        port_id = self._port.get("portId") or self._port.get("number")
        
        # Standardized unique ID logic: uses the key to differentiate from sensors
        self.entity_description = SwitchEntityDescription(
            key=f"port_switch_{port_id}",
            name=f"Port {port_id} Enabled",
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
        """Return True if entity is available."""
        return self._device.status == "online"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Refresh the device and port data from the coordinator data dump
        for device in self.coordinator.data.get("devices", []):
            if device.serial == self._device.serial:
                self._device = device
                ports = getattr(self._device, "ports_statuses", []) or []
                for port in ports:
                    port_id = self._port.get("portId") or self._port.get("number")
                    if port.get("portId") == port_id or port.get("number") == port_id:
                        self._port = port
                        break
                break
        
        self._update_internal_state()
        self.async_write_ha_state()

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch."""
        # If there is a command in flight, don't let the poller overwrite the state yet
        if self.unique_id and self.coordinator.is_pending(self.unique_id):
            return

        self._attr_is_on = self._port.get("enabled", False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (enable the port)."""
        port_id = self._port.get("portId") or self._port.get("number")
        if not self._device.serial or not port_id:
            _LOGGER.error("Cannot enable port: Missing serial or port ID.")
            return

        # Optimistic update: change UI immediately
        self._attr_is_on = True
        self.async_write_ha_state()

        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

        try:
            await self.coordinator.api.switch.update_device_switch_port(
                serial=self._device.serial,
                port_id=str(port_id),
                enabled=True,
            )
        except Exception:
            # Revert state on failure
            self._attr_is_on = False
            if self.unique_id:
                self.coordinator.cancel_pending_update(self.unique_id)
            self.async_write_ha_state()
            raise

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (disable the port)."""
        port_id = self._port.get("portId") or self._port.get("number")
        if not self._device.serial or not port_id:
            _LOGGER.error("Cannot disable port: Missing serial or port ID.")
            return

        # Optimistic update: change UI immediately
        self._attr_is_on = False
        self.async_write_ha_state()

        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

        try:
            await self.coordinator.api.switch.update_device_switch_port(
                serial=self._device.serial,
                port_id=str(port_id),
                enabled=False,
            )
        except Exception:
            # Revert state on failure
            self._attr_is_on = True
            if self.unique_id:
                self.coordinator.cancel_pending_update(self.unique_id)
            self.async_write_ha_state()
            raise