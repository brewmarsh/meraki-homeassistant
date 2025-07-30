"""Sensor for Meraki appliance port status."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ....const import DOMAIN
from ....core.coordinators.device import MerakiDeviceCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Meraki appliance port sensors from a config entry."""
    device_coordinator = hass.data[DOMAIN][config_entry.entry_id]["device_coordinator"]
    entities = []
    for device in device_coordinator.data.get("devices", []):
        if device.get("productType") == "appliance":
            for port in device.get("ports", []):
                entities.append(MerakiAppliancePortSensor(device_coordinator, device, port))
    async_add_entities(entities, True)


class MerakiAppliancePortSensor(
    CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity
):
    """Representation of a Meraki appliance port sensor."""

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
        port: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._attr_unique_id = f"{self._device['serial']}_port_{self._port['number']}"
        self._attr_name = f"{self._device['name']} Port {self._port['number']}"
        self._attr_icon = "mdi:ethernet-port"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
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
        if self._port.get("enabled"):
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
