"""Sensor for Meraki appliance port status."""

from typing import Any, Dict

from ....core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiDeviceSensor


class MerakiAppliancePortSensor(MerakiDeviceSensor):
    """Representation of a Meraki appliance port sensor."""

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Dict[str, Any],
        port: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            device,
            coordinator.config_entry,
            f"port_{port['number']}",
        )
        self._port = port
        self._attr_name = f"Port {self._port['number']}"
        self._attr_icon = "mdi:ethernet-port"

    def _update_state(self) -> None:
        """Update the state of the sensor."""
        device_data = self._get_current_device_data()
        if device_data:
            for port in device_data.get("ports", []):
                if port["number"] == self._port["number"]:
                    self._port = port
                    break
        if not self._port.get("enabled"):
            self._attr_native_value = "disabled"
        elif self._port.get("status") == "connected":
            self._attr_native_value = "connected"
        else:
            self._attr_native_value = "disconnected"

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
