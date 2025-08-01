"""Sensors for Meraki switch port counts."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.coordinators.device import MerakiDeviceCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiPortsInUseSensor(CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity):
    """Representation of a Meraki switch ports in use sensor.

    This sensor displays the number of ports that are currently in use
    (i.e., have a "connected" status) on a Meraki MS switch.
    """

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:lan-connect"

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device['serial']}_ports_in_use"
        self._attr_name = f"{self._device['name']} Ports In Use"

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
                self._device = device
                self.async_write_ha_state()
                return

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        port_statuses = self._device.get("port_statuses")
        if not port_statuses or not isinstance(port_statuses, list):
            return None

        return len([p for p in port_statuses if p.get("status") == "connected"])


class MerakiPortsAvailableSensor(
    CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity
):
    """Representation of a Meraki switch ports available sensor.

    This sensor displays the number of ports that are currently available
    (i.e., do not have a "connected" status) on a Meraki MS switch.
    """

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:lan-pending"

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device['serial']}_ports_available"
        self._attr_name = f"{self._device['name']} Ports Available"

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
                self._device = device
                self.async_write_ha_state()
                return

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        port_statuses = self._device.get("port_statuses")
        if not port_statuses or not isinstance(port_statuses, list):
            return None

        return len([p for p in port_statuses if p.get("status") != "connected"])
