"""Switch entity for controlling Meraki Switch Ports."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.models.device import MerakiAppliancePort, MerakiDevice
from ..entity import MerakiEntity
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiSwitchPortToggle(MerakiEntity, SwitchEntity):
    """Representation of a Meraki Switch Port toggle entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Switch Port toggle entity."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._config_entry = config_entry

        port_id = self._port.get("portId") or self._port.get("number")

        # Standardized unique ID logic: uses the key to differentiate from sensors
        self.entity_description = SwitchEntityDescription(
            key=f"port_switch_{port_id}",
            name=f"Port {port_id} enabled",
        )
        self._update_internal_state()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return resolve_device_info(self._device, self._config_entry)

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


class MerakiAppliancePortSwitch(MerakiSwitchPortToggle):
    """Representation of a Meraki Appliance Port toggle entity."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: MerakiAppliancePort,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Appliance Port toggle entity."""
        super().__init__(coordinator, device, port.to_dict(), config_entry)
        self._appliance_port = port

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self._device.serial:
            return
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            for port in device.appliance_ports:
                if port.number == self._appliance_port.number:
                    self._appliance_port = port
                    self._port = port.to_dict()
                    break

        self._update_internal_state()
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (enable the port)."""
        if (
            not self._device.serial
            or not self._device.network_id
            or self._appliance_port.number is None
        ):
            _LOGGER.error(
                "Cannot enable port: Missing serial, network ID or port number."
            )
            return

        # Optimistic update
        self._attr_is_on = True
        self.async_write_ha_state()

        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

        try:
            await self.coordinator.api.appliance.update_network_appliance_port(
                network_id=self._device.network_id,
                port_id=str(self._appliance_port.number),
                enabled=True,
            )
        except Exception:
            self._attr_is_on = False
            if self.unique_id:
                self.coordinator.cancel_pending_update(self.unique_id)
            self.async_write_ha_state()
            raise

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (disable the port)."""
        if (
            not self._device.serial
            or not self._device.network_id
            or self._appliance_port.number is None
        ):
            _LOGGER.error(
                "Cannot disable port: Missing serial, network ID or port number."
            )
            return

        # Optimistic update
        self._attr_is_on = False
        self.async_write_ha_state()

        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

        try:
            await self.coordinator.api.appliance.update_network_appliance_port(
                network_id=self._device.network_id,
                port_id=str(self._appliance_port.number),
                enabled=False,
            )
        except Exception:
            self._attr_is_on = True
            if self.unique_id:
                self.coordinator.cancel_pending_update(self.unique_id)
            self.async_write_ha_state()
            raise
