"""Sensor for Meraki switch PoE."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinators import MerakiSwitchCoordinator
from ...core.models import MerakiSwitchDevice
from ...helpers.device_info_helpers import resolve_device_info


class MerakiSwitchPoESensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki switch port PoE sensor."""

    coordinator: MerakiSwitchCoordinator

    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:power-plug"

    def __init__(
        self,
        coordinator: MerakiSwitchCoordinator,
        device: MerakiSwitchDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._config_entry = config_entry

        self._attr_has_entity_name = True
        port_id = self._port.get("portId") or self._port.get("number")
        self._attr_unique_id = f"{self._device.serial}_port_{port_id}_poe"
        self._attr_name = f"Port {port_id} PoE"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return resolve_device_info(self._device, self._config_entry)

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return self._device.status == "online"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device.serial == self._device.serial:
                self._device = device
                for port in self._device.switch_ports:
                    port_id = self._port.get("portId") or self._port.get("number")
                    if port.get("portId") == port_id or port.get("number") == port_id:
                        self._port = port
                        break
                break
        self.async_write_ha_state()

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        power_usage = self._port.get("powerUsage", {})
        if isinstance(power_usage, dict) and "power" in power_usage:
            return float(power_usage["power"])
        return 0.0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        power_usage = self._port.get("powerUsage", {})
        if not isinstance(power_usage, dict):
            power_usage = {}

        return {
            "current": power_usage.get("current"),
            "power": power_usage.get("power"),
            "voltage": power_usage.get("voltage"),
        }
