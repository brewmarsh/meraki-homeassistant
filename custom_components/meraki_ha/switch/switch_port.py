"""Switch entity for controlling Meraki Switch Ports."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Protocol

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.models import MerakiAppliancePort
from ..core.models.device import MerakiDevice
from ..entity import MerakiEntity
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


def _get_port_identifier_from_data(port_data: dict[str, Any]) -> str | None:
    """Extracts the port identifier (portId or number) from port data."""
    port_id = port_data.get("portId")
    if port_id is not None:
        return str(port_id)
    port_number = port_data.get("number")
    if port_number is not None:
        return str(port_number)
    return None


class MerakiPortApiCommand(Protocol):
    """Protocol for API commands to update a Meraki port."""

    async def __call__(self, enabled: bool) -> Any:
        """Call method for the API command."""
        ...


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
        coordinator: MerakiDataUpdateCoordinator,
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

    @abstractmethod
    def _refresh_port_data_from_coordinator(self) -> None:
        """Abstract method to refresh port data from coordinator."""
        pass

    def _get_port_identifier(self) -> str | None:
        """Get the primary identifier for the port."""
        return _get_port_identifier_from_data(self._port)

    def _update_internal_state(self) -> None:
        """Update the internal state of the switch."""
        # If there is a command in flight, don't let the poller overwrite the state yet
        if self.unique_id and self.coordinator.is_pending(self.unique_id):
            return
        self._attr_is_on = self._port.get("enabled", False)

    async def _execute_port_command(
        self,
        enabled: bool,
        api_command_func: MerakiPortApiCommand,
        port_description: str,
    ) -> None:
        """Execute a port enable/disable command with optimistic update and error handling."""
        port_identifier = self._get_port_identifier()
        if not self._device.serial or not port_identifier:
            _LOGGER.error(
                "Cannot %s %s: Missing device serial (%s) or port identifier (%s).",
                "enable" if enabled else "disable",
                port_description,
                self._device.serial,
                port_identifier,
            )
            return

        # Optimistic update
        previous_state = self._attr_is_on
        self._attr_is_on = enabled
        self.async_write_ha_state()

        if self.unique_id:
            self.coordinator.register_pending_update(self.unique_id)

        try:
            await api_command_func(enabled)
            _LOGGER.debug(
                "Successfully set %s for %s (device: %s, port: %s).",
                "enabled" if enabled else "disabled",
                port_description,
                self._device.serial,
                port_identifier,
            )
        except Exception as e:
            _LOGGER.error(
                "Failed to %s %s (device: %s, port: %s): %s",
                "enable" if enabled else "disable",
                port_description,
                self._device.serial,
                port_identifier,
                e,
            )
            # Revert state on failure
            self._attr_is_on = previous_state
            if self.unique_id:
                self.coordinator.cancel_pending_update(self.unique_id)
            self.async_write_ha_state()
            raise  # Re-raise the exception to HA

    @abstractmethod
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        pass

    @abstractmethod
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        pass


class MerakiSwitchPortToggle(_MerakiPortSwitchBase):
    """Representation of a Meraki Switch Port toggle entity."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
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

    def _refresh_port_data_from_coordinator(self) -> None:
        """Refresh switch port data from the coordinator."""
        updated_device = self.coordinator.get_device(self._device.serial)
        if updated_device:
            self._device = updated_device
            current_port_identifier = self._get_port_identifier()
            if not current_port_identifier:
                _LOGGER.warning(
                    "Could not find identifier for current switch port for device %s.",
                    self._device.serial,
                )
                return

            ports_statuses = getattr(self._device, "switch_ports", [])
            for port_data in ports_statuses:
                if _get_port_identifier_from_data(port_data) == current_port_identifier:
                    self._port = port_data
                    _LOGGER.debug(
                        "Refreshed switch port %s for device %s",
                        current_port_identifier,
                        self._device.serial,
                    )
                    return
            _LOGGER.warning(
                "Switch port %s not found in updated data for device %s. It may have been removed or changed.",
                current_port_identifier,
                self._device.serial,
            )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (enable the port)."""
        port_id = self._get_port_identifier()
        if not port_id:
            _LOGGER.error("Cannot enable switch port: Port identifier is missing.")
            return

        await self._execute_port_command(
            enabled=True,
            api_command_func=lambda enabled: self.coordinator.api.switch.update_device_switch_port(
                serial=self._device.serial,
                port_id=str(port_id),
                enabled=enabled,
            ),
            port_description=f"switch port {port_id}",
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (disable the port)."""
        port_id = self._get_port_identifier()
        if not port_id:
            _LOGGER.error("Cannot disable switch port: Port identifier is missing.")
            return

        await self._execute_port_command(
            enabled=False,
            api_command_func=lambda enabled: self.coordinator.api.switch.update_device_switch_port(
                serial=self._device.serial,
                port_id=str(port_id),
                enabled=enabled,
            ),
            port_description=f"switch port {port_id}",
        )


class MerakiAppliancePortSwitch(_MerakiPortSwitchBase):
    """Representation of a Meraki Appliance Port toggle entity."""

    _appliance_port: MerakiAppliancePort

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
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
        self._appliance_port = port  # Keep original model for direct access

    def _refresh_port_data_from_coordinator(self) -> None:
        """Refresh appliance port data from the coordinator."""
        updated_device = self.coordinator.get_device(self._device.serial)
        if updated_device:
            self._device = updated_device
            current_port_number = self._appliance_port.number
            if current_port_number is None:
                _LOGGER.warning(
                    "Appliance port number is missing for device %s. Cannot refresh.",
                    self._device.serial,
                )
                return

            for port in self._device.appliance_ports:
                if port.number == current_port_number:
                    self._appliance_port = port
                    self._port = port.to_dict()  # Update base _port dict
                    _LOGGER.debug(
                        "Refreshed appliance port %s for device %s",
                        current_port_number,
                        self._device.serial,
                    )
                    return
            _LOGGER.warning(
                "Appliance port %s not found in updated data for device %s. It may have been removed or changed.",
                current_port_number,
                self._device.serial,
            )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (enable the port)."""
        port_number = self._appliance_port.number
        if not self._device.network_id or port_number is None:
            _LOGGER.error(
                "Cannot enable appliance port: Missing network ID (%s) or port number (%s).",
                self._device.network_id,
                port_number,
            )
            return

        await self._execute_port_command(
            enabled=True,
            api_command_func=lambda enabled: self.coordinator.api.appliance.update_network_appliance_port(
                network_id=self._device.network_id,
                port_id=str(port_number),
                enabled=enabled,
            ),
            port_description=f"appliance port {port_number}",
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (disable the port)."""
        port_number = self._appliance_port.number
        if not self._device.network_id or port_number is None:
            _LOGGER.error(
                "Cannot disable appliance port: Missing network ID (%s) or port number (%s).",
                self._device.network_id,
                port_number,
            )
            return

        await self._execute_port_command(
            enabled=False,
            api_command_func=lambda enabled: self.coordinator.api.appliance.update_network_appliance_port(
                network_id=self._device.network_id,
                port_id=str(port_number),
                enabled=enabled,
            ),
            port_description=f"appliance port {port_number}",
        )
