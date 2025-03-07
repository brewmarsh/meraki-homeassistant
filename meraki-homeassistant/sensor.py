# sensor.py
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from .meraki_api import get_meraki_devices

_LOGGER = logging.getLogger(__name__)  # Create a logger instance


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Meraki binary sensors."""
    _LOGGER.debug("Setting up Meraki sensors")
    api_key = config_entry.data["meraki_api_key"]
    org_id = config_entry.data["meraki_org_id"]
    _LOGGER.debug(f"API Key: {api_key}, Org ID: {org_id}")

    try:
        devices = await get_meraki_devices(api_key, org_id)
        _LOGGER.debug(f"Devices: {devices}")

        sensors = []  # Initialize sensors as an empty list
        for device in devices:
            # if device["model"].startswith(("MX", "MS", "MR")):  # Temporarily comment out for testing
            sensors.append(MerakiDeviceSensor(device, api_key, org_id))

        _LOGGER.debug(f"Created sensors: {sensors}")
        async_add_entities(sensors)
    except Exception as e:
        _LOGGER.error(f"Error setting up Meraki sensors: {e}")


class MerakiDeviceSensor(BinarySensorEntity):
    """Representation of a Meraki device sensor."""

    def __init__(self, device, api_key, org_id):
        """Initialize the sensor."""
        self._device = device
        self._api_key = api_key
        self._org_id = org_id
        self._attr_unique_id = f"meraki_{device['serial']}_status"
        self._attr_name = f"Meraki {device['model']} {device['name']} Status"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
        self._attr_available = True

    @property
    def is_on(self):
        """Return True if the device is online."""
        return self._device["status"] == "online"

    async def async_update(self):
        """Update the sensor state."""
        try:
            devices = await get_meraki_devices(self._api_key, self._org_id)
            for device in devices:
                if device["serial"] == self._device["serial"]:
                    self._device = device
                    break
        except Exception as e:
            # Handle exceptions, log errors
            print(f"Error updating Meraki sensor: {e}")
            self._attr_available = (
                False  # set the sensor to unavailable if there is an error.
            )
            return
        self._attr_available = (
            True  # set the sensor to available if the update is successful.
        )
