"""Sensor for Meraki switch port status."""

from __future__ import annotations

from datetime import datetime
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
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...types import MerakiDevice


class MerakiSwitchPortSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki switch port sensor."""

    _attr_entity_registry_enabled_default = False
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
        self._attr_unique_id = (
            f"{self._device.serial}_port_{self._port['portId']}_power"
        )
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
            # Get timespan from coordinator or default to 300s
            timespan = (
                self.coordinator.update_interval.total_seconds()
                if self.coordinator.update_interval
                else 300
            )

            # Power (W) = Energy (Wh) * 3600 (s/h) / Timespan (s)
            return round(power_usage_wh * 3600 / timespan, 2)
        return 0.0


class MerakiSwitchPortEnergySensor(CoordinatorEntity, RestoreEntity, SensorEntity):
    """Representation of a Meraki switch port energy sensor."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
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
        self._attr_unique_id = (
            f"{self._device.serial}_port_{self._port['portId']}_energy"
        )
        self._attr_name = f"Port {self._port['portId']} Energy"
        self._total_energy = 0.0
        self._last_update_timestamp: datetime | None = None

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            try:
                self._total_energy = float(state.state)
            except (ValueError, TypeError):
                self._total_energy = 0.0

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

                        # Check for duplicate updates
                        if (
                            self.coordinator.last_successful_update
                            and (
                                self._last_update_timestamp is None
                                or self.coordinator.last_successful_update
                                > self._last_update_timestamp
                            )
                        ):
                            energy_increment = port.get("powerUsageInWh", 0) or 0
                            self._total_energy += energy_increment
                            self._last_update_timestamp = (
                                self.coordinator.last_successful_update
                            )

                        break
                break
        self.async_write_ha_state()

    @property
    def native_value(self) -> float:
        """Return the state of the sensor."""
        return round(self._total_energy, 2)
