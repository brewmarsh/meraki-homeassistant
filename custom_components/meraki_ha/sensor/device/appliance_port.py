"""Sensor for Meraki appliance port status."""

from collections.abc import Mapping
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...helpers.device_info_helpers import resolve_device_info
from ...helpers.entity_helpers import format_entity_name
from ...helpers.logging_helper import MerakiLoggers
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = MerakiLoggers.SENSOR


class MerakiAppliancePortSensor(CoordinatorEntity, SensorEntity):  # type: ignore[type-arg]
    """Representation of a Meraki appliance port sensor."""

    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Mapping[str, Any],
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
    def device_info(self) -> DeviceInfo | None:
        """Return device information with network hierarchy."""
        if self.coordinator.config_entry is None:
            return None
        return resolve_device_info(
            entity_data=self._device,
            config_entry=self.coordinator.config_entry,
        )

    def _get_current_device_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this device from the coordinator."""
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device["serial"]:
                    return dev_data
        return None

    def _get_current_port_data(self) -> dict[str, Any] | None:
        """Retrieve the latest data for this port from the coordinator."""
        device = self._get_current_device_data()
        if not device:
            return None
        for port in device.get("ports", []):
            if port.get("number") == self._port.get("number"):
                return port
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        current_device = self._get_current_device_data()
        if current_device:
            self._device = current_device
            current_port = self._get_current_port_data()
            if current_port:
                self._port = current_port
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        return self._get_current_port_data() is not None

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        # Always get fresh data from coordinator
        port = self._get_current_port_data() or self._port
        if not port.get("enabled"):
            return "disabled"
        if port.get("status") == "connected":
            return "connected"
        return "disconnected"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        # Always get fresh data from coordinator
        port = self._get_current_port_data() or self._port
        return {
            "port_number": port.get("number"),
            "link_speed": port.get("speed"),
            "vlan": port.get("vlan"),
            "type": port.get("type"),
            "access_policy": port.get("accessPolicy"),
        }
