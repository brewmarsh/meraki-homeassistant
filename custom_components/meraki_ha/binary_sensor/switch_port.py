"""Binary sensor for Meraki switch port status."""

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..helpers.device_info_helpers import resolve_device_info
from ..helpers.entity_helpers import get_device_from_coordinator
from ..meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class SwitchPortSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Meraki switch port sensor."""

    _attr_state_color = True
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

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
        self._attr_unique_id = f"{self._device['serial']}_{self._port['portId']}"
        self._attr_name = f"Port {self._port['portId']}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    def _get_current_port_data(self) -> dict[str, Any] | None:
        """Get the current port data from the coordinator."""
        device = get_device_from_coordinator(self.coordinator, self._device["serial"])
        if not device:
            return None
        for port in device.get("ports_statuses", []):
            if port.get("portId") == self._port.get("portId"):
                return port
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        device = get_device_from_coordinator(self.coordinator, self._device["serial"])
        if device:
            self._device = device
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
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        # Always get fresh data from coordinator
        port = self._get_current_port_data() or self._port
        return port.get("status") == "Connected"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        # Always get fresh data from coordinator
        port = self._get_current_port_data() or self._port
        return {
            "port_id": port.get("portId"),
            "speed": port.get("speed"),
            "duplex": port.get("duplex"),
            "vlan": port.get("vlan"),
            "enabled": port.get("enabled"),
        }
