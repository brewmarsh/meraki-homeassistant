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
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const.integration import DOMAIN
from ...coordinators import MerakiSwitchCoordinator
from ...core.models import MerakiSwitchDevice


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
        self._device_serial = str(device.serial)
        self._port = port
        self._config_entry = config_entry

        self._attr_has_entity_name = True
        port_id = self._port.get("portId") or self._port.get("number")
        self._attr_unique_id = f"{self._device.serial}_port_{port_id}_poe"
        self._attr_name = f"Port {port_id} PoE"
        self._last_state = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info linking this port to its parent hardware."""
        from ...core.utils.naming_utils import format_device_name

        # Action 3: Robust lookup for correct parent linkage
        device = self.coordinator.get_device(self._device_serial) or self._device

        return DeviceInfo(
            identifiers={(DOMAIN, self._device_serial)},
            name=format_device_name(
                device,
                self.coordinator.config_entry.options
                if self.coordinator.config_entry
                else {},
            ),
            manufacturer="Cisco Meraki",
            model=getattr(device, "model", "Unknown"),
            sw_version=getattr(device, "firmware", ""),
        )

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        if self.coordinator.data is None:
            return False
        return self._device.status == "online"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator, deduplicating unchanged states."""
        if self.coordinator.data is None:
            return
        devices = self.coordinator.data.get("devices", [])
        if not isinstance(devices, list):
            return

        for device in devices:
            if not hasattr(device, "serial"):
                continue
            if device.serial == self._device_serial:
                self._device = device
                switch_ports = getattr(self._device, "switch_ports", [])
                if not isinstance(switch_ports, list):
                    break

                for port in switch_ports:
                    if not isinstance(port, dict):
                        continue
                    port_id = self._port.get("portId") or self._port.get("number")
                    if port.get("portId") == port_id or port.get("number") == port_id:
                        self._port = port
                        break
                break

        # Action 2: Only trigger an expensive UI write if the status actually changed
        current_state = self.native_value
        if self._last_state != current_state:
            self._last_state = current_state
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
