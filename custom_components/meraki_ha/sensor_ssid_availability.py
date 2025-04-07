"""Sensor platform for meraki_ha."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_ON, STATE_OFF

from .const import DOMAIN
from .entity import MerakiEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Meraki SSID Availability sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    devices = coordinator.data.get("devices", [])
    entities = []

    for device in devices:
        for ssid in device.get("ssids", []):
            entities.append(MerakiSSIDAvailabilitySensor(coordinator, device, ssid))

    async_add_entities(entities)


class MerakiSSIDAvailabilitySensor(MerakiEntity, SensorEntity):
    """Meraki SSID Availability Sensor class."""

    def __init__(self, coordinator, device, ssid):
        """Initialize the sensor."""
        super().__init__(coordinator, device, ssid)
        self._name = f"{self._device_name} {self._ssid_name} Availability"
        self._unique_id = f"{self._device_serial}_{self._ssid_number}_availability"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return self._unique_id

    @property
    def state(self):
        """Return the state of the sensor."""
        ssid_data = self.coordinator.data["devices"][self._device_index]["ssids"][
            self._ssid_index
        ]
        if ssid_data.get("enabled"):
            return STATE_ON
        else:
            return STATE_OFF

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:wifi"
