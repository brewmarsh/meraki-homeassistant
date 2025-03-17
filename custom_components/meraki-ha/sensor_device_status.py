"""Sensor platform for the meraki_ha integration."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Device Status sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Device Status sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{device['name']} Status"
        self._attr_unique_id = f"{device['serial']}_status"
        self._attr_icon = "mdi:information-outline"
        self._attr_extra_state_attributes = {
            "model": device.get("model"),
            "serial_number": device.get("serial"),
            "firmware_version": device.get("firmware"),
        }
        _LOGGER.debug(f"Meraki: Device Status Sensor Initialized: {self._attr_name}")

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        if self._device.get("productType") == "appliance":
            return "Appliance"
        elif self._device.get("productType") == "wireless":
            return "Wireless"
        elif self._device.get("productType") == "switch":
            return "Switch"
        elif self._device.get("productType") == "camera":
            return "Camera"
        elif self._device.get("productType") == "sensor":
            return "Sensor"
        else:
            return "Unknown"

    @property
    def device_info(self):
        """Return device information about this entity."""
        device_icon = "mdi:router-network"  # Default icon for devices

        if self._device["model"].startswith("MR"):
            device_icon = "mdi:access-point"
        elif self._device["model"].startswith("MX"):
            device_icon = "mdi:router"
        elif self._device["model"].startswith("MS"):
            device_icon = "mdi:switch"
        elif self._device["model"].startswith("MV"):
            device_icon = "mdi:video"
        elif self._device["model"].startswith("MT"):
            device_icon = "mdi:thermometer"
        # Add more device types as needed
        _LOGGER.debug(f"Domain: {self.coordinator.domain}")
        _LOGGER.debug(f"Serial Number: {self._device['serial']}")
        _LOGGER.debug(f"Device Data: {self._device}")

        return {
            "identifiers": {(self.coordinator.domain, self._device["serial"])},
            "name": self._device["name"],
            "manufacturer": "Cisco Meraki",
            "model": self._device["model"],
            "icon": device_icon,
        }
