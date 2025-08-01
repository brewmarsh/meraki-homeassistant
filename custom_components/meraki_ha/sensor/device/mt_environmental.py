"""Sensors for Meraki MT environmental sensors."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.coordinators.device import MerakiDeviceCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiTemperatureSensor(CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity):
    """Representation of a Meraki temperature sensor.

    This sensor displays the temperature reading from a Meraki MT sensor.
    """

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device['serial']}_temperature"
        self._attr_name = f"{self._device['name']} Temperature"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
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
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        readings = self._device.get("readings")
        if not readings or not isinstance(readings, list):
            return None

        for reading in readings:
            if reading.get("metric") == "temperature":
                return reading.get("value")
        return None


class MerakiHumiditySensor(CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity):
    """Representation of a Meraki humidity sensor.

    This sensor displays the humidity reading from a Meraki MT sensor.
    """

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device['serial']}_humidity"
        self._attr_name = f"{self._device['name']} Humidity"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
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
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        readings = self._device.get("readings")
        if not readings or not isinstance(readings, list):
            return None

        for reading in readings:
            if reading.get("metric") == "humidity":
                return reading.get("value")
        return None


class MerakiWaterDetectionSensor(
    CoordinatorEntity[MerakiDeviceCoordinator], SensorEntity
):
    """Representation of a Meraki water detection sensor.

    This sensor displays the water detection status from a Meraki MT sensor.
    """

    _attr_device_class = SensorDeviceClass.MOISTURE

    def __init__(
        self,
        coordinator: MerakiDeviceCoordinator,
        device: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"{self._device['serial']}_water"
        self._attr_name = f"{self._device['name']} Water Detection"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
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
    def native_value(self) -> bool | None:
        """Return the state of the sensor."""
        readings = self._device.get("readings")
        if not readings or not isinstance(readings, list):
            return None

        for reading in readings:
            if reading.get("metric") == "water":
                return reading.get("value")
        return None
