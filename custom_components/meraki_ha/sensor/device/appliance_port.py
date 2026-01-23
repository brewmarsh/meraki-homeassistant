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
from ...core.utils.naming_utils import format_device_name, format_entity_name
from ...types import MerakiAppliancePort, MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiAppliancePortSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki appliance port sensor."""

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
        assert self._device.serial
        self._port = port
        self._attr_unique_id = f"{device.serial}_port_{self._port.number}"
        self._attr_name = format_entity_name(
            device,
            self.coordinator.config_entry.options,
            f"Port {self._port.number}",
        )
        self._attr_icon = "mdi:ethernet-port"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, cast(str, self._device.serial))},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device.model,
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
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
        if not self._port.enabled:
            return "disabled"
        if self._port.status == "connected":
            return "connected"
        return "disconnected"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "port_number": self._port.number,
            "link_speed": self._port.speed,
            "vlan": self._port.vlan,
            "type": self._port.type,
            "access_policy": self._port.access_policy,
        }
