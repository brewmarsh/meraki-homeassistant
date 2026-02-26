"""Sensor for Meraki switch port status."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

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
from ...core.models.device import MerakiDevice
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiSwitchPortBaseSensor(CoordinatorEntity, SensorEntity, ABC):
    """Base representation of a Meraki switch port sensor."""

    coordinator: MerakiDataUpdateCoordinator
    _device: MerakiDevice
    _port: dict[str, Any]
    _config_entry: ConfigEntry

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: MerakiDevice,
        port: dict[str, Any],
        config_entry: ConfigEntry,
        unique_id_suffix: str,
        name_suffix: str,
    ) -> None:
        """Initialize the base sensor."""
        super().__init__(coordinator)
        self._device = device
        self._port = port
        self._config_entry = config_entry

        port_id = self._get_port_id_from_data(port)
        self._attr_unique_id = f"{self._device.serial}_port_{port_id}{unique_id_suffix}"
        self._attr_name = f"Port {port_id}{name_suffix}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return resolve_device_info(self._device, self._config_entry)

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        # An entity is only available if its parent device is online.
        return self._device.status == "online"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        updated_device, updated_port = self._find_updated_device_and_port()
        if updated_device and updated_port:
            self._device = updated_device
            self._port = updated_port
            self.async_write_ha_state()
        else:
            current_port_id = self._get_port_id_from_data(self._port)
            _LOGGER.debug(
                "Could not find updated data for device serial '%s', port ID '%s' in coordinator data. Sensor might be stale or unavailable.",
                self._device.serial,
                current_port_id,
            )
            # If the device or port is not found, the entity should eventually reflect unavailability.
            # For now, it will keep its last known state, and 'available' property check handles device online status.

    def _get_port_id_from_data(self, port_data: dict[str, Any]) -> str | int | None:
        """Extract the port ID from port data, preferring 'portId' then 'number'."""
        return port_data.get("portId") or port_data.get("number")

    def _find_updated_device_and_port(
        self,
    ) -> tuple[MerakiDevice | None, dict[str, Any] | None]:
        """Find the updated device and port data from the coordinator's data."""
        current_port_id = self._get_port_id_from_data(self._port)
        if not current_port_id:
            _LOGGER.warning(
                "Current port data for sensor '%s' is missing 'portId' or 'number'. Cannot update.",
                self.unique_id,
            )
            return None, None

        for device in self.coordinator.data.get("devices", []):
            if device.serial == self._device.serial:
                for port in device.switch_ports:
                    port_id_candidate = self._get_port_id_from_data(port)
                    if port_id_candidate == current_port_id:
                        return device, port
                _LOGGER.debug(
                    "Port ID '%s' not found in updated device '%s' port statuses. Sensor '%s' might be stale.",
                    current_port_id,
                    self._device.serial,
                    self.unique_id,
                )
                # Device found, but the specific port was not in its updated ports_statuses.
                # This could mean the port was removed or its data is temporarily missing.
                return device, None  # Return device, but not the specific port
        _LOGGER.debug(
            "Device serial '%s' not found in coordinator data for sensor '%s'. Sensor might be stale or unavailable.",
            self._device.serial,
            self.unique_id,
        )
        return None, None

    @property
    @abstractmethod
    def native_value(self) -> Any:
        """Return the native value of the sensor."""
        # This must be implemented by subclasses
        pass


class MerakiSwitchPortSensor(MerakiSwitchPortBaseSensor):
    """Representation of a Meraki switch port status sensor."""

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
        super().__init__(
            coordinator,
            device,
            port,
            config_entry,
            unique_id_suffix="",
            name_suffix=" status",
        )

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor (port status)."""
        return self._port.get("status")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        port_id = self._get_port_id_from_data(self._port)
        return {
            "enabled": self._port.get("enabled"),
            "speed": self._port.get("speed"),
            "duplex": self._port.get("duplex"),
            "vlan": self._port.get("vlan"),
            "port_id": port_id,
            "mac": self._device.mac,  # MAC is a device-level attribute
        }


class MerakiSwitchPortPowerSensor(MerakiSwitchPortBaseSensor):
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
        super().__init__(
            coordinator,
            device,
            port,
            config_entry,
            unique_id_suffix="_power",
            name_suffix=" power",
        )

    @property
    def native_value(self) -> float:
        """Return the state of the sensor (power in Watts)."""
        power_usage_wh = self._port.get("powerUsageInWh", 0) or 0
        if power_usage_wh > 0:
            # FIX: Force 24h window (86400s) as discussed
            timespan = 86400
            # Power (W) = Energy (Wh) * 3600 (s/h) / Timespan (s)
            return round(float(power_usage_wh * 3600 / timespan), 2)
        return 0.0


class MerakiSwitchPortEnergySensor(MerakiSwitchPortBaseSensor):
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
        super().__init__(
            coordinator,
            device,
            port,
            config_entry,
            unique_id_suffix="_energy",
            name_suffix=" energy",
        )

    @property
    def native_value(self) -> float:
        """Return the state of the sensor (energy in Watt-hours)."""
        return round(float(self._port.get("powerUsageInWh", 0) or 0), 2)
