"""Sensor for Meraki appliance port status."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...helpers.entity_helpers import format_entity_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiAppliancePortSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki appliance port sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: dict[str, Any],
        port: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._attr_unique_id = f"{self._device['serial']}_port_{self._port['number']}"
        self._attr_name = format_entity_name(
            self._device["name"],
            f"Port {self._port['number']}",
        )
        self._attr_icon = "mdi:ethernet-port"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device["serial"]:
                    return dev_data
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        current_device = self._get_current_device_data()
        if current_device:
            self._device = current_device
            for port in current_device.get("ports", []):
                if port["number"] == self._port["number"]:
                    self._port = port
                    break
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        return self._get_current_device_data() is not None

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        if not self._port.get("enabled"):
            return "disabled"
        if self._port.get("status") == "connected":
            return "connected"
        return "disconnected"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "port_number": self._port.get("number"),
            "link_speed": self._port.get("speed"),
            "vlan": self._port.get("vlan"),
            "type": self._port.get("type"),
            "access_policy": self._port.get("accessPolicy"),
        }
