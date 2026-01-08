"""Base class for Meraki MT sensor entities."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import UnitOfTemperature
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import (
    CONF_TEMPERATURE_UNIT,
    DEFAULT_TEMPERATURE_UNIT,
    DOMAIN,
    TEMPERATURE_UNIT_FAHRENHEIT,
)
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiMtSensor(CoordinatorEntity, SensorEntity, RestoreEntity):
    """Representation of a Meraki MT sensor.

    Uses RestoreEntity to preserve state across Home Assistant restarts.
    """

    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        device: Mapping[str, Any],
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self.entity_description = entity_description
        self._attr_unique_id = f"{self._device['serial']}_{self.entity_description.key}"
        self._attr_name = f"{self._device['name']} {self.entity_description.name}"
        self._restored_value: str | float | bool | None = None

    async def async_added_to_hass(self) -> None:
        """Restore state when entity is added to HA."""
        await super().async_added_to_hass()

        # Restore previous state on restart
        if (last_state := await self.async_get_last_state()) is not None:
            # Try to restore numeric value for sensors
            try:
                self._restored_value = float(last_state.state)
            except (ValueError, TypeError):
                self._restored_value = last_state.state

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        options = (
            self.coordinator.config_entry.options
            if self.coordinator.config_entry
            else {}
        )
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=format_device_name(self._device, options),
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    def _get_current_device(self) -> dict[str, Any] | None:
        """Get the current device data from the coordinator."""
        if not self.coordinator.data:
            return None
        for device in self.coordinator.data.get("devices", []):
            if device.get("serial") == self._device.get("serial"):
                return device
        return None

    def _get_readings(self) -> list[dict[str, Any]] | None:
        """Get the readings list from the current device data."""
        device = self._get_current_device()
        if not device:
            return None
        # Use readings_raw (list format) for sensor entities
        readings = device.get("readings_raw") or device.get("readings")
        if isinstance(readings, list):
            return readings
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        current = self._get_current_device()
        if current:
            self._device = current
        self.async_write_ha_state()

    @property
    def _use_fahrenheit(self) -> bool:
        """Check if Fahrenheit should be used for temperature."""
        options = (
            self.coordinator.config_entry.options
            if self.coordinator.config_entry
            else {}
        )
        temp_unit = options.get(CONF_TEMPERATURE_UNIT, DEFAULT_TEMPERATURE_UNIT)
        return temp_unit == TEMPERATURE_UNIT_FAHRENHEIT

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement for this sensor."""
        # For temperature sensors, return the configured unit
        if self.entity_description.key == "temperature":
            if self._use_fahrenheit:
                return UnitOfTemperature.FAHRENHEIT
            return UnitOfTemperature.CELSIUS
        # For other sensors, use the entity description's unit
        return self.entity_description.native_unit_of_measurement

    @property
    def native_value(self) -> str | float | bool | None:
        """Return the state of the sensor."""
        readings = self._get_readings()
        if not readings:
            # Return restored value if no fresh readings
            return self._restored_value

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                metric_data = reading.get(self.entity_description.key)
                if isinstance(metric_data, dict):
                    # Handle temperature specially based on user preference
                    if self.entity_description.key == "temperature":
                        if self._use_fahrenheit:
                            return metric_data.get("fahrenheit")
                        return metric_data.get("celsius")

                    # Map metric to the key holding its value
                    key_map = {
                        "humidity": "relativePercentage",
                        "pm25": "concentration",
                        "tvoc": "concentration",
                        "co2": "concentration",
                        "noise": "ambient",
                        "water": "present",
                        "realPower": "draw",  # API uses realPower
                        "apparentPower": "draw",
                        "voltage": "level",
                        "current": "draw",
                        "battery": "percentage",
                        "button": "pressType",
                        "indoorAirQuality": "score",
                    }
                    value_key = key_map.get(self.entity_description.key)
                    if value_key:
                        if value_key == "ambient":
                            return metric_data.get("ambient", {}).get("level")
                        return metric_data.get(value_key)
        # Fall back to restored value
        return self._restored_value

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity state attributes with update timestamp."""
        attrs: dict[str, Any] = {}
        if self.coordinator.last_successful_update:
            attrs["last_meraki_update"] = (
                self.coordinator.last_successful_update.isoformat()
            )

        # Add MQTT update timestamp if available
        serial = self._device.get("serial", "")
        mqtt_update = self.coordinator.get_mqtt_last_update(serial) if serial else None
        if mqtt_update:
            attrs["last_mqtt_update"] = mqtt_update.isoformat()
            attrs["data_source"] = "mqtt"
        elif self.coordinator.mqtt_enabled:
            attrs["data_source"] = "mqtt_pending"
        else:
            attrs["data_source"] = "api"

        return attrs

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        # Sensor is available if coordinator has data and there's a reading
        if not self.coordinator.last_update_success:
            return False

        readings = self._get_readings()
        if not readings:
            return False

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                return True
        return False
