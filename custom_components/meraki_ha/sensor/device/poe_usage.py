"""Sensor for Meraki switch PoE usage."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import UnitOfPower
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN, CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
from ...core.coordinators.device import MerakiDeviceCoordinator
from ...helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiPoeUsageSensor(CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity):
    """Representation of a Meraki switch PoE usage sensor.

    This sensor displays the aggregated PoE usage for a Meraki MS switch
    in watts. The attributes provide a breakdown of PoE usage per port.
    """

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_icon = "mdi:power-plug"

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device['serial']}_poe_usage"
        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            f"{self._device['name']} PoE Usage", "sensor", name_format, apply_format=False
        )

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
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        port_statuses = self._device.get("port_statuses")
        if not port_statuses or not isinstance(port_statuses, list):
            return None

        total_poe_usage = 0
        for port in port_statuses:
            if port.get("poe"):
                total_poe_usage += port["poe"].get("power", 0)

        return round(total_poe_usage, 2)

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        port_statuses = self._device.get("port_statuses")
        if not port_statuses or not isinstance(port_statuses, list):
            return {}

        attributes = {}
        for port in port_statuses:
            if port.get("poe"):
                attributes[f"port_{port['portId']}_poe_usage"] = port["poe"].get(
                    "power"
                )

        return attributes
