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

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.models.device import MerakiDevice
from ...core.utils.naming_utils import format_device_name
from ...entity import MerakiSensor

_LOGGER = logging.getLogger(__name__)


class MerakiMtSensor(MerakiSensor, RestoreSensor):
    """Representation of a Meraki MT sensor."""

    _attr_native_value: str | float | bool | None

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
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
        self._update_native_value()

    def _maybe_get_value(self, value: Any) -> Any | None:
        """Return the value if not UNDEFINED, else None."""
        return value if value is not UNDEFINED else None

    async def async_added_to_hass(self) -> None:
        """Handle entity which provides state restoration."""
        await super().async_added_to_hass()
        if (last_sensor_data := await self.async_get_last_sensor_data()) is not None:
            if last_sensor_data.native_value is not UNDEFINED:
                self._attr_native_value = last_sensor_data.native_value

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, cast(str, self._device.serial))},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device.model,
            manufacturer="Cisco Meraki",
        )

    def _get_value_from_legacy_device_attributes(self, key: str) -> Any | None:
        """Retrieve value from older MT device attributes."""
        if key == "noise":
            return self._maybe_get_value(self._device.ambient_noise)
        if key == "pm25":
            return self._maybe_get_value(self._device.pm25)
        if key == "door":
            return self._maybe_get_value(self._device.door_open)
        return None

    def _extract_value_from_metric_data(
        self, key: str, metric_data: dict[str, Any]
    ) -> Any | None:
        """Extract value from a metric_data dictionary based on key and specific rules."""
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
            "energy": "draw",
        }
        value_key = key_map.get(key)

        if value_key:
            value = self._maybe_get_value(metric_data.get(value_key))
            if value is not None:
                return value

            # Fallbacks for power monitoring if primary key_map value is None
            if key == "voltage":
                return self._maybe_get_value(metric_data.get("draw"))
            if key == "energy":
                return self._maybe_get_value(
                    metric_data.get("energyUsage")
                ) or self._maybe_get_value(metric_data.get("apparentPower"))
            if key == "powerFactor":
                return self._maybe_get_value(metric_data.get("factor"))
            return None  # No value found after fallbacks

        if key == "noise":
            return self._maybe_get_value(metric_data.get("ambient", {}).get("level"))

        return None

    def _get_value_from_readings_list(
        self, key: str, readings: list[dict[str, Any]]
    ) -> Any | None:
        """Iterate through readings list to find a matching metric and extract its value."""
        for reading in readings:
            metric = reading.get("metric")
            # Handle "realPower" which might be reported as "power"
            if metric == key or (key == "realPower" and metric == "power"):
                metric_data = reading.get(metric)
                if isinstance(metric_data, dict):
                    if value := self._extract_value_from_metric_data(key, metric_data):
                        return value
        return None

    def _get_value_from_generic_device_attributes(self, key: str) -> Any | None:
        """Retrieve value from generic device attributes using getattr."""
        attr_map: dict[str, str] = {
            "frequency": "frequency",
            "powerFactor": "power_factor",
            "energy": "energy",
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
        key = self.entity_description.key

        # 1. Try values from legacy device attributes
        if value := self._get_value_from_legacy_device_attributes(key):
            self._attr_native_value = value
            return

        # 2. Try values from the 'readings' list if available
        if self._device.readings and isinstance(self._device.readings, list):
            if value := self._get_value_from_readings_list(key, self._device.readings):
                self._attr_native_value = value
                return

        # 3. Fallback to generic device attributes
        if value := self._get_value_from_generic_device_attributes(key):
            self._attr_native_value = value
            return

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if not self._device.serial:
            return
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            self._update_native_value()
            self.async_write_ha_state()

    @property
    def native_value(self) -> str | float | bool | None:
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        if self.native_value is not None:
            return True

        readings = self._device.readings
        if not readings or not isinstance(readings, list):
            return False

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                return True
        return False
