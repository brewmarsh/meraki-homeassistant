"""Base class for Meraki MT sensor entities."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorEntityDescription,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name
from ...types import MerakiDevice

_LOGGER = logging.getLogger(__name__)


class MerakiMtSensor(CoordinatorEntity, RestoreSensor):
    """Representation of a Meraki MT sensor."""

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
        self._attr_name = self.entity_description.name
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """Handle entity which provides state restoration."""
        await super().async_added_to_hass()
        if (last_sensor_data := await self.async_get_last_sensor_data()) is not None:
            self._attr_native_value: str | None | int | float | bool = (
                last_sensor_data.native_value
            )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device.serial)},
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

        if key == "noise":
            self._attr_native_value = self._device.ambient_noise
        elif key == "pm25":
            self._attr_native_value = self._device.pm25
        elif key == "power":
            self._attr_native_value = self._device.real_power
        elif key == "power_factor":
            self._attr_native_value = self._device.power_factor
        elif key == "current":
            self._attr_native_value = self._device.current
        elif key == "door":
            self._attr_native_value = self._device.door_open
        else:
            readings = self._device.readings
            if not readings or not isinstance(readings, list):
                return

            for reading in readings:
                if reading.get("metric") == key:
                    metric_data = reading.get(key)
                    if isinstance(metric_data, dict):
                        key_map = {
                            "battery": "percentage",
                            "temperature": "celsius",
                            "humidity": "relativePercentage",
                            "tvoc": "concentration",
                            "co2": "concentration",
                            "water": "present",
                            "voltage": "level",
                        }
                        value_key = key_map.get(key)
                        if value_key:
                            self._attr_native_value = metric_data.get(value_key)
                            return

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        device = self.coordinator.get_device(self._device.serial)
        if device:
            self._device = device
            self._update_native_value()
            self.async_write_ha_state()

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
