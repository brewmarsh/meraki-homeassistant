"""Binary sensor for Meraki switch port status."""

import logging
<<<<<<< HEAD
from typing import Any
=======
from typing import TYPE_CHECKING, Any
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

<<<<<<< HEAD
from ..helpers.device_info_helpers import resolve_device_info
from ..helpers.entity_helpers import get_device_from_coordinator
from ..meraki_data_coordinator import MerakiDataCoordinator
=======
from ..coordinator import MerakiDataUpdateCoordinator
from ..helpers.device_info_helpers import resolve_device_info

if TYPE_CHECKING:
    from ..types import MerakiDevice
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

_LOGGER = logging.getLogger(__name__)


class SwitchPortSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Meraki switch port sensor."""

    _attr_state_color = True
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device: dict[str, Any],
=======
        coordinator: MerakiDataUpdateCoordinator,
        device: "MerakiDevice",
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        port: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
<<<<<<< HEAD
        self._attr_unique_id = f"{self._device['serial']}_{self._port['portId']}"
=======
        self._attr_unique_id = f"{device.serial}_{self._port['portId']}"
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        self._attr_name = f"Port {self._port['portId']}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
<<<<<<< HEAD
        device = get_device_from_coordinator(self.coordinator, self._device["serial"])
        if device:
            self._device = device
            for port in self._device.get("ports_statuses", []):
=======
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            for port in device.ports_statuses:
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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
