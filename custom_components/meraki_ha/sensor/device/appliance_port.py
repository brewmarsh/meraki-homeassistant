"""Sensor for Meraki appliance port status."""

from __future__ import annotations

import logging
from typing import Any, cast

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.models import MerakiAppliancePort
from ...core.models.device import MerakiDevice
from ...core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


class MerakiAppliancePortSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki appliance port sensor."""

    coordinator: MerakiDataUpdateCoordinator

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: MerakiAppliancePort,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{device.serial}_port_{self._port.number}"
        self._attr_name = f"Port {self._port.number}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        if self.coordinator.config_entry:
            format_device_name(self._device, self.coordinator.config_entry.options)
        return DeviceInfo(
            identifiers={(DOMAIN, cast(str, self._device.serial))},
            name=format_device_name(
                self._device,
                self.coordinator.config_entry.options
                if self.coordinator.config_entry
                else {},
            ),
            model=self._device.model,
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self._device.serial:
            return
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            for port in device.appliance_ports:
                if port.number == self._port.number:
                    self._port = port
                    self.async_write_ha_state()
                    return

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        # Strictly return "connected" or "disconnected"
        if self._port.status and self._port.status.lower() == "connected":
            return "connected"
        return "disconnected"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return (
            "mdi:ethernet"
            if self.native_value == "connected"
            else "mdi:ethernet-cable-off"
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "port_number": self._port.number,
            "link_speed": self._port.speed,
            "vlan": self._port.vlan,
            "type": self._port.type,
            "access_policy": self._port.access_policy,
            "enabled": self._port.enabled,
            "icon_color": "green" if self.native_value == "connected" else "grey",
        }
