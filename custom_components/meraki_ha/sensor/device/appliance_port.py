"""Sensor for Meraki appliance port status."""

<<<<<<< HEAD
=======
from __future__ import annotations

>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
<<<<<<< HEAD
from ...core.utils.naming_utils import format_device_name
from ...helpers.entity_helpers import format_entity_name
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name, format_entity_name
from ...types import MerakiAppliancePort, MerakiDevice
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

_LOGGER = logging.getLogger(__name__)


class MerakiAppliancePortSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki appliance port sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device: dict[str, Any],
        port: dict[str, Any],
=======
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: MerakiAppliancePort,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
<<<<<<< HEAD
        self._attr_unique_id = f"{self._device['serial']}_port_{self._port['number']}"
        self._attr_name = format_entity_name(
            self._device["name"],
            f"Port {self._port['number']}",
=======
        self._attr_unique_id = f"{device.serial}_port_{self._port.number}"
        self._attr_name = format_entity_name(
            device,
            self.coordinator.config_entry.options,
            f"Port {self._port.number}",
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        )
        self._attr_icon = "mdi:ethernet-port"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
<<<<<<< HEAD
            identifiers={(DOMAIN, self._device["serial"])},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device["model"],
=======
            identifiers={(DOMAIN, self._device.serial)},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device.model,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
<<<<<<< HEAD
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                for port in device.get("ports", []):
                    if port["number"] == self._port["number"]:
                        self._port = port
                        self.async_write_ha_state()
                        return
=======
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            for port in device.appliance_ports:
                if port.number == self._port.number:
                    self._port = port
                    self.async_write_ha_state()
                    return
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
<<<<<<< HEAD
        if not self._port.get("enabled"):
            return "disabled"
        if self._port.get("status") == "connected":
=======
        if not self._port.enabled:
            return "disabled"
        if self._port.status == "connected":
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
            return "connected"
        return "disconnected"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
<<<<<<< HEAD
            "port_number": self._port.get("number"),
            "link_speed": self._port.get("speed"),
            "vlan": self._port.get("vlan"),
            "type": self._port.get("type"),
            "access_policy": self._port.get("accessPolicy"),
=======
            "port_number": self._port.number,
            "link_speed": self._port.speed,
            "vlan": self._port.vlan,
            "type": self._port.type,
            "access_policy": self._port.access_policy,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        }
