"""Base class for Meraki MT sensor entities."""

from __future__ import annotations

import logging
from typing import Any, cast

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorEntityDescription,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.typing import UNDEFINED

from ...coordinators import MerakiSensorCoordinator
from ...core.models.device import MerakiDevice
from ...entity import MerakiSensor
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiMtSensor(MerakiSensor, RestoreSensor):
    """Representation of a Meraki MT sensor."""

    _attr_native_value: str | float | bool | None

    def __init__(
        self,
        coordinator: MerakiSensorCoordinator,
        device: MerakiDevice,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self.entity_description = entity_description

        # We no longer set _attr_unique_id here as the @property below handles it.
        self._attr_has_entity_name = True

        if self.entity_description.name is not UNDEFINED:
            self._attr_name = cast(str | None, self.entity_description.name)

        self._attr_native_value = None
        
        # Translate HA entity key to Meraki Metric key immediately
        self._meraki_metric_key = self._translate_ha_key(self.entity_description.key)
        
        self._update_native_value()

    def _translate_ha_key(self, ha_key: str) -> str:
        """Translate a Home Assistant standard key to a Meraki API metric key."""
        translations = {
            "pm2_5": "pm25",
        }
        return translations.get(ha_key, ha_key)

    def _maybe_get_value(self, value: Any) -> Any | None:
        """Return the value if not UNDEFINED, else None."""
        return value if value is not UNDEFINED else None

    async def async_added_to_hass(self) -> None:
        """Handle entity which provides state restoration."""
        await super().async_added_to_hass()
        if (last_sensor_data := await self.async_get_last_sensor_data()) is not None:
            value = last_sensor_data.native_value
            if value is not UNDEFINED:
                # Type check and conversion for MyPy compatibility
                if isinstance(value, (str, float, bool)):
                    self._attr_native_value = value
                elif isinstance(value, int):  # Handle int->float conversion safely
                    self._attr_native_value = float(value)
                # Ignore other types (e.g. datetime) that don't match our state type

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    def _get_value_from_legacy_device_attributes(self, key: str) -> Any | None:
        """Retrieve value from older MT device attributes."""
        if isinstance(self._device, dict):
            if key == "noise":
                return self._maybe_get_value(self._device.get("ambientNoise"))
            if key == "pm25":
                val = self._maybe_get_value(self._device.get("pm25"))
                if val is not None:
                    return val
                return self._maybe_get_value(self._device.get("pm2_5"))
            if key == "door":
                return self._maybe_get_value(self._device.get("doorOpen"))
            return None

        if key == "noise":
            return self._maybe_get_value(getattr(self._device, "ambient_noise", UNDEFINED))
        if key == "pm25":
            val = self._maybe_get_value(getattr(self._device, "pm25", UNDEFINED))
            if val is not None:
                return val
            return self._maybe_get_value(getattr(self._device, "pm2_5", UNDEFINED))
        if key == "door":
            return self._maybe_get_value(getattr(self._device, "door_open", UNDEFINED))
        return None

    def _get_metric_fallback(self, key: str, metric_data: dict[str, Any]) -> Any | None:
        """Get fallback values for specific metrics if primary key is missing."""
        if key == "voltage":
            return self._maybe_get_value(metric_data.get("draw"))
        if key == "energy":
            for fallback_key in (
                "kWh", # MT40 Energy is usually reported in kWh
                "energyUsage",
                "apparentPower",
                "energy",
                "energyApparent",
                "energy_kWh",
            ):
                val = self._maybe_get_value(metric_data.get(fallback_key))
                if val is not None:
                    return val
            return None
        if key == "powerFactor":
            return self._maybe_get_value(metric_data.get("factor"))
        return None

    def _extract_value_from_metric_data(
        self, key: str, metric_data: dict[str, Any]
    ) -> Any | None:
        """Extract value from metric_data based on key and specific rules."""
        key_map: dict[str, str] = {
            "battery": "percentage",
            "temperature": "celsius",
            "humidity": "relativePercentage",
            "tvoc": "concentration",
            "co2": "concentration",
            "pm25": "concentration",
            "rssi": "level",
            "water": "present",
            "button": "pressType",
            "realPower": "draw",
            "current": "draw",
            "voltage": "level",
            "powerFactor": "percentage",
            "frequency": "level",
            "energy": "kWh", # CRITICAL FIX: MT40 Energy uses kWh
            "apparentPower": "draw",
        }

        if value_key := key_map.get(key):
            if (value := self._maybe_get_value(metric_data.get(value_key))) is not None:
                return value
            return self._get_metric_fallback(key, metric_data)

        if key == "noise":
            return self._maybe_get_value(metric_data.get("ambient", {}).get("level"))

        return None

    def _extract_from_reading(self, key: str, reading: dict[str, Any]) -> Any | None:
        """Extract value if the reading metric matches the desired key."""
        metric = reading.get("metric")
        # Handle "realPower" which might be reported as "power"
        if (
            metric == key
            or (key == "realPower" and metric == "power")
        ):
            metric_data = reading.get(metric)
            if isinstance(metric_data, dict):
                return self._extract_value_from_metric_data(key, metric_data)
        return None

    def _get_readings_list(self) -> list[dict[str, Any]] | None:
        """Return the device readings as a list if valid."""
        if not self.coordinator.data or not self._serial:
            return None
        readings_map = self.coordinator.data.get("sensor_readings")
        if not isinstance(readings_map, dict):
            return None
        return readings_map.get(self._serial)

    def _get_value_from_readings_list(
        self, key: str, readings: list[dict[str, Any]]
    ) -> Any | None:
        """Find a matching metric in readings and extract its value."""
        for reading in readings:
            if value := self._extract_from_reading(key, reading):
                return value
        return None

    def _get_value_from_generic_device_attributes(self, key: str) -> Any | None:
        """Retrieve value from generic device attributes."""
        if isinstance(self._device, dict):
            if key == "energy":
                for fallback_key in ("energy", "energyApparent", "energy_kWh"):
                    val = self._maybe_get_value(self._device.get(fallback_key))
                    if val is not None:
                        return val
                return None
            # Add other generic mappings if needed
            attr_map_dict = {
                "frequency": "frequency",
                "powerFactor": "powerFactor",
                "realPower": "realPower",
                "voltage": "voltage",
                "current": "current",
            }
            if attr_name := attr_map_dict.get(key):
                return self._maybe_get_value(self._device.get(attr_name))
            return None

        if key == "energy":
            for fallback_attr in ("energy", "energy_apparent", "energy_kwh"):
                val = self._maybe_get_value(getattr(self._device, fallback_attr, UNDEFINED))
                if val is not None:
                    return val
            return None

        attr_map: dict[str, str] = {
            "frequency": "frequency",
            "powerFactor": "power_factor",
            "realPower": "real_power",
            "voltage": "voltage",
            "current": "current",
        }
        if attr_name := attr_map.get(key):
            return self._maybe_get_value(getattr(self._device, attr_name, UNDEFINED))
        return None

    def _update_native_value(self) -> None:
        """Update the native value of the sensor by trying different data sources."""
        self._attr_native_value = None

        # 1. Try values from legacy device attributes
        if value := self._get_value_from_legacy_device_attributes(self._meraki_metric_key):
            self._attr_native_value = value
            return

        # 2. Try values from the 'readings' list if available
        readings = self._get_readings_list()
        if readings and (value := self._get_value_from_readings_list(self._meraki_metric_key, readings)):
            self._attr_native_value = value
            return

        # 3. Fallback to generic device attributes
        if value := self._get_value_from_generic_device_attributes(self._meraki_metric_key):
            self._attr_native_value = value
            return

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if device := self.device_data:
            self._device = device
            self._update_native_value()

        # Ensure we call the parent callback to write the state and handle upstream logic
        super()._handle_coordinator_update()

    @property
    def native_value(self) -> str | float | bool | None:
        """Return the state of the sensor."""
        return self._attr_native_value

    def _is_metric_in_readings(self, readings: list[dict[str, Any]]) -> bool:
        """Check if the sensor's metric exists in the given readings list."""
        for reading in readings:
            metric = reading.get("metric")
            if (
                metric == self._meraki_metric_key
                or (self._meraki_metric_key == "realPower" and metric == "power")
            ):
                return True
        return False

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        # Defer to the parent MerakiEntity logic which checks the coordinator state
        if not super().available:
            return False

        if self.native_value is not None:
            return True

        readings = self._get_readings_list()
        return readings is not None and self._is_metric_in_readings(readings)
