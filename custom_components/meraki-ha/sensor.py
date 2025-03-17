"""Sensor platform for the meraki_ha integration."""

import logging

from homeassistant.components.sensor import SensorEntity
from typing import List
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_COORDINATOR, DOMAIN
from .sensor_connected_clients import MerakiConnectedClientsSensor
from .sensor_radio_settings import MerakiRadioSettingsSensor
from .sensor_uplink_status import MerakiUplinkStatusSensor
from .sensor_device_status import MerakiDeviceStatusSensor
from .meraki_api.networks import (
    get_network_clients_count,
    get_network_ids_and_names,
)
import aiohttp

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform for the Meraki integration."""
    _LOGGER.debug("Meraki: sensor.py async_setup_entry called")
    try:
        coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

        sensors: List[SensorEntity] = []
        for device in coordinator.data:
            _LOGGER.debug(f"Meraki: Processing device: {device['name']}")
            sensors.append(MerakiDeviceStatusSensor(coordinator, device))
            if device["model"].startswith("MR") or device["model"].startswith("GR"):
                _LOGGER.debug(f"Meraki: Adding MR/GR sensors for {device['name']}")
                sensors.append(MerakiConnectedClientsSensor(coordinator, device))
                sensors.append(MerakiRadioSettingsSensor(coordinator, device))
            elif device["model"].startswith("MX"):
                _LOGGER.debug(f"Meraki: Adding MX sensors for {device['name']}")
                sensors.append(MerakiUplinkStatusSensor(coordinator, device))

        async with aiohttp.ClientSession() as session:
            networks = await get_network_ids_and_names(
                coordinator.api_key, coordinator.org_id, session
            )
        _LOGGER.debug(f"sensor.py: Networks retrieved: {networks}")

        if networks is not None:
            for network in networks:
                sensors.append(
                    MerakiNetworkClientCountSensor(
                        coordinator, network["id"], network["name"]
                    )
                )

        async_add_entities(sensors)
    except KeyError as e:
        _LOGGER.error(f"Meraki: KeyError setting up meraki_ha sensors: {e}")
    except TypeError as e:
        _LOGGER.error(f"Meraki: TypeError setting up meraki_ha sensors: {e}")
    except ValueError as e:
        _LOGGER.error(f"Meraki: ValueError setting up meraki_ha sensors: {e}")
    except Exception as e:
        _LOGGER.error(f"Meraki: Unexpected error setting up meraki_ha sensors: {e}")
        _LOGGER.error(f"Meraki: Error setting up meraki_ha sensors: {e}")


class MerakiNetworkClientCountSensor(SensorEntity):
    def __init__(self, coordinator, network_id, network_name):
        """
        Initialize the sensor.

        Args:
        """

    async def async_update(self):
        async with aiohttp.ClientSession() as session:
            self._attr_native_value = await get_network_clients_count(
                self._coordinator.api_key, self._network_id, session
            )
        self.async_write_ha_state()

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._network_id)},
            "name": self._network_name,
            "manufacturer": "Cisco Meraki",
            "model": "Network",
        }
