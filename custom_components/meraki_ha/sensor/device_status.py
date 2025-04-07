"""
Sensor platform for the meraki_ha integration.
"""

import logging
from homeassistant.components.sensor import SensorEntity

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from typing import Dict, Any
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Device Status sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Device Status sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{device['name']} Status"
        self._attr_unique_id = f"{device['serial']}_status"
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
        return {
            "identifiers": {(DOMAIN, self._device["serial"])},
            "name": self._device["name"],
            "manufacturer": "Cisco Meraki",
            "model": self._device["model"],
            "sw_version": self._device.get("firmware"),
        }

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self._device["model"].startswith("MR"):
            return "mdi:access-point"
        elif self._device["model"].startswith("MX"):
            return "mdi:router"
        elif self._device["model"].startswith("MS"):
            return "mdi:switch"
        elif self._device["model"].startswith("MV"):
            return "mdi:video"
        elif self._device["model"].startswith("MT"):
            return "mdi:thermometer"
        else:
            return "mdi:router-network"  # Default icon
