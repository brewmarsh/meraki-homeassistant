"""Sensor platform for meraki_ha."""

import logging

from homeassistant.components.sensor import SensorEntity

from ..entity import MerakiEntity

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDClientCountSensor(MerakiEntity, SensorEntity):
    """Meraki SSID Client Count Sensor class."""

    def __init__(self, coordinator, device, ssid):
        """Initialize the sensor."""
        super().__init__(coordinator, device, ssid)
        self._name = f"{self._device_name} {self._ssid_name} Client Count"
        self._unique_id = f"{self._device_serial}_{self._ssid_number}_client_count"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return self._unique_id

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._ssid.get("client_count")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:account-multiple"
