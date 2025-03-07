"""Sensor platform for meraki_ha."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_MERAKI_API_KEY, CONF_MERAKI_ORG_ID, DOMAIN
from .meraki_api import get_meraki_devices

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Data provided by the Meraki Dashboard API"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Meraki sensor platform."""
    _LOGGER.debug("Meraki HA: async_setup_entry in sensor.py called")
    _LOGGER.debug(f"Meraki HA: async_setup_entry received async_add_entities of type: {type(async_add_entities)}")
    _LOGGER.debug(f"Config Entry Options: {config_entry.options}")
    api_key = config_entry.options[CONF_MERAKI_API_KEY]
    org_id = config_entry.options[CONF_MERAKI_ORG_ID]

    devices = await get_meraki_devices(api_key, org_id)

    if devices:
        sensors = []
        for device in devices:
            sensors.append(MerakiDeviceSensor(device))

        _LOGGER.debug(f"Meraki HA: async_add_entities type before call: {type(async_add_entities)}") #add this line
        await async_add_entities(sensors)
    else:
        _LOGGER.error("Failed to retrieve Meraki devices.")

class MerakiDeviceSensor(SensorEntity):
    """Representation of a Meraki Device Sensor."""

    def __init__(self, device):
        """Initialize the sensor."""
        try:
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
        except KeyError as e:
            _LOGGER.error(f"Error initializing sensor for {device.get('serial')}: {e}")
            self._attr_name = "Error"
            self._attr_unique_id = f"error-{device.get('serial')}"
            self._attr_state = "Error"
            self._attr_extra_state_attributes = {}

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

    async def async_update(self):
        """Fetch new state data for the sensor."""
        pass