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

from ..coordinator import MerakiDataUpdateCoordinator
from ..core.utils.naming_utils import format_entity_name
from ..helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class SwitchPortSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Meraki switch port sensor."""

    _attr_state_color = True
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: dict[str, Any] | Any,
        port: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        serial = device.serial if hasattr(device, "serial") else device["serial"]
        self._attr_unique_id = f"{serial}_{self._port['portId']}"
        self._attr_name = f"Port {self._port['portId']}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        serial = (
            self._device.serial
            if hasattr(self._device, "serial")
            else self._device["serial"]
        )
        device = self.coordinator.get_device(serial)
        if device:
            self._device = device
            # device is a MerakiDevice dataclass here (from get_device)
            # ports_statuses is a list of dicts
            ports = (
                device.ports_statuses
                if hasattr(device, "ports_statuses")
                else device.get("ports_statuses", [])
            )
            for port in ports:
                if port["portId"] == self._port["portId"]:
                    self._port = port
                    self.async_write_ha_state()
                    return

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self._port.get("status") == "Connected"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "port_id": self._port.get("portId"),
            "speed": self._port.get("speed"),
            "duplex": self._port.get("duplex"),
            "vlan": self._port.get("vlan"),
            "enabled": self._port.get("enabled"),
        }
