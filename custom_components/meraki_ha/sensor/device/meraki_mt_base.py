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
            value = last_sensor_data.native_value
            if value is not UNDEFINED:
                if isinstance(value, (str, float, bool)):
                    self._attr_native_value = value
                elif isinstance(value, int):
                    self._attr_native_value = float(value)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device information."""
        return resolve_device_info(self._device, self.coordinator.config_entry)

    def _get_readings_list(self) -> list[dict[str, Any]] | None:
        """Return the device readings as a list if valid."""
        if not self.coordinator.data or not self._serial:
            return None
        readings_map = self.coordinator.data.get("sensor_readings")
        if not isinstance(readings_map, dict):
            return None
        return readings_map.get(self._serial)

    def _fuzzy_match_metric(self, metric: str, target: str) -> bool:
        """Perform a fuzzy match on metric keys to handle API variations (e.g. pm2_5 vs pm25)."""
        if not metric or not target:
            return False
        m_clean = str(metric).lower().replace("_", "")
        t_clean = str(target).lower().replace("_", "")
        return m_clean == t_clean or (t_clean == "realpower" and m_clean == "power")

    def _extract_from_readings_robustly(self) -> Any | None:
        """Ultra-resilient data extraction that bypasses strict mapping."""
        readings = self._get_readings_list()
        if not readings:
            return None

        target_key = self.entity_description.key

        for reading in readings:
            metric = reading.get("metric")
            if self._fuzzy_match_metric(metric, target_key):
                # The payload is usually nested under the EXACT metric string
                # e.g., {"metric": "pm25", "pm25": {"concentration": ...}}
                payload = reading.get(metric)
                if isinstance(payload, dict):
                    # Check all known Meraki value keys. Whichever hits first is our value!
                    for val_key in [
                        "concentration", 
                        "celsius", 
                        "relativePercentage", 
                        "percentage", 
                        "level", 
                        "draw", 
                        "kWh", 
                        "present", 
                        "pressType", 
                        "factor"
                    ]:
                        if val_key in payload:
                            return self._maybe_get_value(payload[val_key])
                    
                    # Fallback for noise: noise -> ambient -> level
                    if "ambient" in payload and isinstance(payload["ambient"], dict):
                        return self._maybe_get_value(payload["ambient"].get("level"))
                        
        return None

    def _update_native_value(self) -> None:
        """Update the native value of the sensor."""
        self._attr_native_value = None

        # 1. Try robust readings extraction first (Primary God Module Path)
        if value := self._extract_from_readings_robustly():
            self._attr_native_value = value
            return

        # 2. Fallback to generic object attributes (e.g., pm2_5 or pm25 as direct properties)
        target_key = self.entity_description.key
        fallback_keys = [
            target_key,
            target_key.replace("_", ""),
            "energyApparent",
            "energy_kWh",
            "doorOpen",
            "door_open",
            "ambientNoise",
            "ambient_noise"
        ]
        
        device_dict = self._device if isinstance(self._device, dict) else vars(self._device)
        
        for fk in fallback_keys:
            val = self._maybe_get_value(device_dict.get(fk)) if isinstance(self._device, dict) else self._maybe_get_value(getattr(self._device, fk, UNDEFINED))
            if val is not None:
                self._attr_native_value = val
                return

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if device := self.device_data:
            self._device = device
            self._update_native_value()

        super()._handle_coordinator_update()

    @property
    def native_value(self) -> str | float | bool | None:
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        if not super().available:
            return False

        if self.native_value is not None:
            return True

        readings = self._get_readings_list()
        if readings:
            target_key = self.entity_description.key
            for reading in readings:
                if self._fuzzy_match_metric(reading.get("metric"), target_key):
                    return True
        return False
