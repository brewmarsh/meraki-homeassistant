"""Sensor platform for meraki_ha."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DATA_CLIENT, DATA_COORDINATOR

_LOGGER = logging.getLogger(__name__)
ATTRIBUTION = "Data provided by the Meraki Dashboard API"

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Meraki sensor platform."""
    _LOGGER.debug("Meraki HA: async_setup_entry in sensor.py called")
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    await coordinator.async_config_entry_first_refresh()

    sensors = [MerakiDeviceSensor(coordinator, device) for device in coordinator.data]

    async_add_entities(sensors)

class MerakiDeviceSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Device Sensor."""

    def __init__(self, coordinator, device):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = device["name"]
        self._attr_unique_id = device["serial"]
        self._attr_state = device.get("firmware", "Unknown")
        self._attr_extra_state_attributes = {
            "model": device["model"],
            "mac": device["mac"],
            "publicIp": device.get("publicIp"),
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self._device["serial"])},
            "name": self._device["name"],
            "manufacturer": "Cisco Meraki",
            "model": self._device["model"],
            "sw_version": self._device.get("firmware"),
        }

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self._device["serial"])},
            "name": self._device["name"],
            "manufacturer": "Cisco Meraki",
            "model": self._device["model"],
            "sw_version": self._device.get("firmware"),
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._attr_state