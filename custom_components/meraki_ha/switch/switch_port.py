"""Switch entity for controlling Meraki Switch Ports."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ..coordinators import MerakiSwitchCoordinator
from ..core.models import MerakiAppliancePort
from ..core.models.device import MerakiDevice
from ..entity import MerakiEntity
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


def _get_port_identifier_from_data(port_data: dict[str, Any]) -> str | None:
    """Extract the port identifier (portId or number) from port data."""
    port_id = port_data.get("portId")
    if port_id is not None:
        return str(port_id)
    port_number = port_data.get("number")
    if port_number is not None:
        return str(port_number)
    return None


class _MerakiPortSwitchBase(MerakiEntity, SwitchEntity, ABC):
    """Base class for Meraki Switch Port toggle entities."""

    _attr_has_entity_name = True
    _device: MerakiDevice
    _config_entry: ConfigEntry
    _port: dict[
        str, Any
    ]  # This will hold the common dictionary representation of the port

    def __init__(
        self,
        coordinator: MerakiSwitchCoordinator,
        device: MerakiDevice,
        port_data: dict[str, Any],  # Raw dictionary representation of the port
        config_entry: ConfigEntry,
        entity_key_prefix: str,
    ) -> None:
        """Initialize the base Meraki Port toggle entity."""
        super().__init__(coordinator)
        self._device = device
        self._port = port_data
        self._config_entry = config_entry

        port_id_str = self._get_port_identifier()
        if not port_id_str:
            _LOGGER.error(
                "Failed to initialize %s entity: Port identifier is missing in data %s. "
                "This entity might not function correctly.",
                self.__class__.__name__,
                port_data,
            )
            # Ensure the key is always a string, even if identifier is missing.
            # This entity might not be fully functional but prevents errors during setup.
            port_id_str = "unknown"

        self.entity_description = SwitchEntityDescription(
            key=f"{entity_key_prefix}_{port_id_str}",
            name=f"Port {port_id_str} enabled",
        )
        self._update_internal_state()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return resolve_device_info(self._device, self._config_entry)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # Entity is available if the underlying Meraki device is online.
        return self._device.status == "online"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._refresh_port_data_from_coordinator()
        self._update_internal_state()
        self.async_write_ha_state()

    def _refresh_port_data_from_coordinator(self) -> None:
        """Refresh port data from the coordinator."""
        updated_device = self.coordinator.get_device(self._device.serial)
        if not updated_device:
            return

        self._device = updated_device
        current_port_id = self._get_port_identifier()
        if not current_port_id:
            _LOGGER.warning(
                "Could not find identifier for current port for device %s.",
                self._device.serial,
            )
            return

        for port_data in self._get_device_ports():
            port_dict = (
                port_data if isinstance(port_data, dict) else port_data.to_dict()
            )
            if _get_port_identifier_from_data(port_dict) == current_port_id:
                self._port = port_dict
                _LOGGER.debug(
                    "Refreshed port %s for device %s",
                    current_port_id,
                    self._device.serial,
                )
                return

        _LOGGER.warning(
            "Port %s not found in updated data for device %s. It may have been removed or changed.",
            current_port_id,
            self._device.serial,
        )

    def _get_port_identifier(self) -> str | None:
        """Get the primary identifier for the port."""
        return _get_port_identifier_from_data(self._port)

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch."""
        # If there is a command in flight, don't let the poller overwrite the state yet
        if self.unique_id and self.coordinator.is_pending(self.unique_id):
            return
        self._attr_is_on = self._port.get("enabled", False)

    async def _toggle_port(self, enabled: bool) -> None:
        """Execute a port enable/disable command with optimistic update and error handling."""
        port_id = self._get_port_identifier()
        if not self._device.serial or not port_id:
            _LOGGER.error(
                "Cannot %s port: Missing device serial (%s) or port identifier (%s).",
                "enable" if enabled else "disable",
                self._device.serial,
                port_id,
            )
            return

        # Optimistic update
        previous_state = self._attr_is_on
        self._attr_is_on = enabled
        self.async_write_ha_state()

        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

        try:
            await self._async_update_port_status(port_id, enabled)
            _LOGGER.debug(
                "Successfully set %s for port %s (device: %s).",
                "enabled" if enabled else "disabled",
                port_id,
                self._device.serial,
            )
        except Exception as e:
            _LOGGER.error(
                "Failed to %s port %s (device: %s): %s",
                "enable" if enabled else "disable",
                port_id,
                self._device.serial,
                e,
            )
            # Revert state on failure
            self._attr_is_on = previous_state
            if self.unique_id:
                self.coordinator.cancel_pending_update(self.unique_id)
            self.async_write_ha_state()
            raise  # Re-raise the exception to HA

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._toggle_port(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._toggle_port(False)

    @abstractmethod
    def _get_device_ports(self) -> list[Any]:
        """Return the list of ports for this device from the coordinator data."""

    @abstractmethod
    async def _async_update_port_status(self, port_id: str, enabled: bool) -> Any:
        """Execute the API call to update the port status."""


class MerakiSwitchPortToggle(_MerakiPortSwitchBase):
    """Representation of a Meraki Switch Port toggle entity."""

    def __init__(
        self,
        coordinator: MerakiSwitchCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Switch Port toggle entity."""
        super().__init__(
            coordinator,
            device,
            port,
            config_entry,
            entity_key_prefix="port_switch",
        )

    def _get_device_ports(self) -> list[Any]:
        """Get switch ports for the device."""
        return getattr(self._device, "switch_ports", [])

    async def _async_update_port_status(self, port_id: str, enabled: bool) -> Any:
        """Update switch port status via API."""
        return await self.coordinator.api.switch.update_device_switch_port(
            serial=self._device.serial,
            port_id=port_id,
            enabled=enabled,
        )


class MerakiAppliancePortSwitch(_MerakiPortSwitchBase):
    """Representation of a Meraki Appliance Port toggle entity."""

    def __init__(
        self,
        coordinator: MerakiSwitchCoordinator,
        device: MerakiDevice,
        port: MerakiAppliancePort,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Meraki Appliance Port toggle entity."""
        super().__init__(
            coordinator,
            device,
            port.to_dict(),  # Pass dictionary representation to base
            config_entry,
            entity_key_prefix="port_switch",  # Keep consistent with switch port unique IDs
        )

    def _get_device_ports(self) -> list[Any]:
        """Get appliance ports for the device."""
        return getattr(self._device, "appliance_ports", [])

    async def _async_update_port_status(self, port_id: str, enabled: bool) -> Any:
        """Update appliance port status via API."""
        if not self._device.network_id:
            raise ValueError(f"Missing network ID for device {self._device.serial}")
        return await self.coordinator.api.appliance.update_network_appliance_port(
            network_id=self._device.network_id,
            port_id=port_id,
            enabled=enabled,
        )
