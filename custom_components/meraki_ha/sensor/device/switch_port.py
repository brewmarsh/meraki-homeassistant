"""Sensor for Meraki switch port status."""

from __future__ import annotations

from typing import Any, cast

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfEnergy, UnitOfPower
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...types import MerakiDevice


class MerakiSwitchPortSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki switch port sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._config_entry = config_entry

        self._attr_has_entity_name = True
        self._attr_unique_id = f"{self._device.serial}_port_{self._port['portId']}"
        self._attr_name = f"Port {self._port['portId']}"
        self._attr_native_value = self._port.get("status")

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(self.coordinator.DOMAIN, cast(str, self._device.serial))},
        )

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
                for port in self._device.ports_statuses:
                    if port["portId"] == self._port["portId"]:
                        self._port = port
                        break
                break
        self._attr_native_value = self._port.get("status")
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "enabled": self._port.get("enabled"),
            "speed": self._port.get("speed"),
            "duplex": self._port.get("duplex"),
            "vlan": self._port.get("vlan"),
            "port_id": self._port.get("portId"),
            "mac": self._device.mac,
        }


class MerakiSwitchPortPowerSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki switch port power sensor."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_translation_key = "power"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._config_entry = config_entry

        self._attr_has_entity_name = True
        self._attr_unique_id = f"{self._device.serial}_port_{self._port['portId']}_power"
        self._attr_name = f"Port {self._port['portId']} Power"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(self.coordinator.DOMAIN, cast(str, self._device.serial))},
        )

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
                for port in self._device.ports_statuses:
                    if port["portId"] == self._port["portId"]:
                        self._port = port
                        break
                break
        self.async_write_ha_state()

    @property
    def native_value(self) -> float:
        """Return the state of the sensor."""
        power_usage_wh = self._port.get("powerUsageInWh", 0) or 0
        if power_usage_wh > 0:
            return round(power_usage_wh / 24, 2)
        return 0.0


class MerakiSwitchPortEnergySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki switch port energy sensor."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_translation_key = "energy"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._config_entry = config_entry

        self._attr_has_entity_name = True
        self._attr_unique_id = f"{self._device.serial}_port_{self._port['portId']}_energy"
        self._attr_name = f"Port {self._port['portId']} Energy"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(self.coordinator.DOMAIN, cast(str, self._device.serial))},
        )

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
                for port in self._device.ports_statuses:
                    if port["portId"] == self._port["portId"]:
                        self._port = port
                        break
                break
        self.async_write_ha_state()

    @property
    def native_value(self) -> float:
        """Return the state of the sensor."""
        return self._port.get("powerUsageInWh", 0) or 0
