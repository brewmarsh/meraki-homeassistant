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
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name
from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiMtSensor(CoordinatorEntity, RestoreSensor):
    """Representation of a Meraki MT sensor."""

    coordinator: MerakiDataUpdateCoordinator

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
        self._attr_unique_id = f"{device.serial}_{self.entity_description.key}"
        self._attr_has_entity_name = True
        if self.entity_description.name is not UNDEFINED:
            self._attr_name = cast(str | None, self.entity_description.name)
        self._attr_native_value: Any = None
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

    def _update_native_value(self) -> None:
        """Update the native value of the sensor."""
        self._attr_native_value = None
        key = self.entity_description.key

        readings = self._device.readings
        if not readings or not isinstance(readings, list):
            # Fallback for older MT devices that don't use the readings structure
            if key == "noise":
                self._attr_native_value = self._maybe_get_value(
                    self._device.ambient_noise
                )
            elif key == "pm25":
                self._attr_native_value = self._maybe_get_value(self._device.pm25)
            elif key == "door":
                self._attr_native_value = self._maybe_get_value(self._device.door_open)
            return

        for reading in readings:
            metric = reading.get("metric")
            # Handle mismatch between API metric name and entity key
            if metric == key or (key == "realPower" and metric == "power"):
                metric_data = reading.get(metric)
                if isinstance(metric_data, dict):
                    # Map metric keys to the nested dictionary key that holds the value
                    key_map = {
                        "battery": "percentage",
                        "temperature": "celsius",
                        "humidity": "relativePercentage",
                        "tvoc": "concentration",
                        "co2": "concentration",
                        "pm25": "concentration",
                        "water": "present",
                        "button": "pressType",
                        # MT40 Power Monitoring
                        "realPower": "draw",
                        "current": "draw",
                        "voltage": "level",  # fallback to draw if level is missing
                        "powerFactor": "percentage",
                        "frequency": "level",
                        "energy": "draw",
                    }
                    value_key = key_map.get(key)
                    if value_key:
                        self._attr_native_value = self._maybe_get_value(
                            metric_data.get(value_key)
                        )
                        # Special case for voltage fallback
                        if key == "voltage" and self._attr_native_value is None:
                            self._attr_native_value = self._maybe_get_value(
                                metric_data.get("draw")
                            )
                        return

                    # Special case for noise (nested structure)
                    if key == "noise":
                        self._attr_native_value = self._maybe_get_value(
                            metric_data.get("ambient", {}).get("level")
                        )
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
        # Available if it has a value from the coordinator or a restored state
        if self.native_value is not None:
            return True

        # The sensor is available if there is a reading for its metric.
        # This prevents creating sensors for metrics that a device doesn't support.
        readings = self._device.readings
        if not readings or not isinstance(readings, list):
            return False

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                return True
        return False
