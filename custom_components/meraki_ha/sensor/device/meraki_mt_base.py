"""Base class for Meraki MT sensor entities."""

import logging
from typing import Any

<<<<<<< HEAD
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
=======
from homeassistant.components.sensor import (
    RestoreSensor,
    SensorEntityDescription,
)
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
<<<<<<< HEAD
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

_LOGGER = logging.getLogger(__name__)


<<<<<<< HEAD
class MerakiMtSensor(CoordinatorEntity, SensorEntity):
=======
class MerakiMtSensor(CoordinatorEntity, RestoreSensor):
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    """Representation of a Meraki MT sensor."""

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
        device: dict[str, Any],
=======
        coordinator: MerakiDataUpdateCoordinator,
        device: "MerakiDevice",
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self.entity_description = entity_description
<<<<<<< HEAD
        self._attr_unique_id = f"{self._device['serial']}_{self.entity_description.key}"
        self._attr_name = f"{self._device['name']} {self.entity_description.name}"
=======
        self._attr_unique_id = f"{device.serial}_{self.entity_description.key}"
        self._attr_has_entity_name = True
        self._attr_name = self.entity_description.name
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """Handle entity which provides state restoration."""
        await super().async_added_to_hass()
        if (last_sensor_data := await self.async_get_last_sensor_data()) is not None:
            self._attr_native_value = last_sensor_data.native_value
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
<<<<<<< HEAD
            identifiers={(DOMAIN, self._device["serial"])},
            name=format_device_name(
                self._device, self.coordinator.config_entry.options
            ),
            model=self._device["model"],
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        for device in self.coordinator.data.get("devices", []):
            if device["serial"] == self._device["serial"]:
                self._device = device
                self.async_write_ha_state()
                return

    @property
    def native_value(self) -> float | bool | None:
        """Return the state of the sensor."""
        readings = self._device.get("readings")
        if not readings or not isinstance(readings, list):
            return None

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                metric_data = reading.get(self.entity_description.key)
                if isinstance(metric_data, dict):
                    # Map metric to the key holding its value
                    key_map = {
                        "temperature": "celsius",
                        "humidity": "relativePercentage",
                        "pm25": "concentration",
                        "tvoc": "concentration",
                        "co2": "concentration",
                        "noise": "ambient",
                        "water": "present",
                        "power": "draw",
                        "voltage": "level",
                        "current": "draw",
                    }
                    value_key = key_map.get(self.entity_description.key)
                    if value_key:
                        if value_key == "ambient":
                            return metric_data.get("ambient", {}).get("level")
                        return metric_data.get(value_key)
        return None
=======
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
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
<<<<<<< HEAD
        # The sensor is available if there is a reading for its metric.
        # This prevents creating sensors for metrics that a device doesn't support.
        readings = self._device.get("readings")
=======
        # Available if it has a value from the coordinator or a restored state
        if self.native_value is not None:
            return True

        # The sensor is available if there is a reading for its metric.
        # This prevents creating sensors for metrics that a device doesn't support.
        readings = self._device.readings
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        if not readings or not isinstance(readings, list):
            return False

        for reading in readings:
            if reading.get("metric") == self.entity_description.key:
                return True
        return False
