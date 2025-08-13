"""Sensor for Meraki appliance port status."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN, CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...helpers.entity_helpers import format_entity_name
from ...core.utils.naming_utils import format_device_name

_LOGGER = logging.getLogger(__name__)


class MerakiAppliancePortSensor(CoordinatorEntity[MerakiDataCoordinator], SensorEntity):
    """Representation of a Meraki appliance port sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Dict[str, Any],
        port: Dict[str, Any],
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

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                for port in device.get("ports", []):
                    if port["number"] == self._port["number"]:
                        self._port = port
                        self.async_write_ha_state()
                        return

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        if not self._port.get("enabled"):
            return "disabled"
        if self._port.get("status") == "connected":
            return "connected"
        return "disconnected"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        return {
            "port_number": self._port.get("number"),
            "link_speed": self._port.get("speed"),
            "vlan": self._port.get("vlan"),
            "type": self._port.get("type"),
            "access_policy": self._port.get("accessPolicy"),
        }
