"""Base class for Meraki MT sensor entities."""

import logging
from typing import Any

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

_LOGGER = logging.getLogger(__name__)


class MerakiMtSensor(CoordinatorEntity, RestoreSensor):
    """Representation of a Meraki MT sensor."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device: dict[str, Any],
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self.entity_description = entity_description
        self._attr_unique_id = f"{self._device['serial']}_{self.entity_description.key}"
        self._attr_name = f"{self._device['name']} {self.entity_description.name}"
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """Handle entity which provides state restoration."""
        await super().async_added_to_hass()
        if (last_sensor_data := await self.async_get_last_sensor_data()) is not None:
            self._attr_native_value = last_sensor_data.native_value

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    def _update_native_value(self) -> None:
        """Update the native value of the sensor."""
        readings = self._device.get("readings")
        if not readings or not isinstance(readings, list):
            self._attr_native_value = None
            return

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                metric_data = reading.get(self.entity_description.key)

                # Handle battery metric
                if self.entity_description.key == "battery":
                    self._attr_native_value = metric_data.get("percentage")
                    return

                # Handle noise metric
                if self.entity_description.key == "noise":
                    if "ambient" in metric_data:
                        self._attr_native_value = metric_data["ambient"].get("level")
                    return

                # Handle other metrics with a generic key map
                if isinstance(metric_data, dict):
                    key_map = {
                        "temperature": "celsius",
                        "humidity": "relativePercentage",
                        "pm25": "concentration",
                        "tvoc": "concentration",
                        "co2": "concentration",
                        "water": "present",
                        "power": "draw",
                        "voltage": "level",
                        "current": "draw",
                    }
                    value_key = key_map.get(self.entity_description.key)
                    if value_key:
                        self._attr_native_value = metric_data.get(value_key)
                        return

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                self._device = device
                self._update_native_value()
                self.async_write_ha_state()
                return

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        # A sensor is available if it has a value from the coordinator or a restored state
        if self.native_value is not None:
            return True

        # The sensor is available if there is a reading for its metric.
        # This prevents creating sensors for metrics that a device doesn't support.
        readings = self._device.get("readings")
        if not readings or not isinstance(readings, list):
            return False

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                return True
        return False
