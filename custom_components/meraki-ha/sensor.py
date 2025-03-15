"""Sensor platform for the meraki_ha integration."""

import logging

from homeassistant.components.sensor import SensorEntity
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
)  # updated import.

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

        sensors: list[SensorEntity] = []
        for device in coordinator.data:
            _LOGGER.debug(f"Meraki: Processing device: {device['name']}")
            sensors.append(
                MerakiDeviceStatusSensor(coordinator, device)
            )  # Add device status sensor
            if device["model"].startswith("MR") or device["model"].startswith("GR"):
                _LOGGER.debug(f"Meraki: Adding MR/GR sensors for {device['name']}")
                sensors.append(MerakiConnectedClientsSensor(coordinator, device))
                sensors.append(MerakiRadioSettingsSensor(coordinator, device))
            elif device["model"].startswith("MX"):
                _LOGGER.debug(f"Meraki: Adding MX sensors for {device['name']}")
                sensors.append(MerakiUplinkStatusSensor(coordinator, device))

        # Add network sensors here (logic from sensor_network_status.py)
        networks = await get_network_ids_and_names(
            coordinator.api_key, coordinator.org_id
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
        _LOGGER.debug(f"Meraki: Meraki Sensors added: {sensors}")
    except Exception as e:
        _LOGGER.error(f"Meraki: Error setting up meraki_ha sensors: {e}")


class MerakiNetworkClientCountSensor(SensorEntity):
    """Representation of a Meraki network client count sensor."""

    def __init__(self, coordinator, network_id, network_name):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._network_id = network_id
        self._network_name = network_name
        self._attr_name = f"{network_name} Clients (24h)"
        self._attr_unique_id = f"{DOMAIN}_{network_id}_clients_24h"
        self._attr_icon = "mdi:network"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._attr_native_value = await get_network_clients_count(
            self._coordinator.api_key, self._network_id
        )

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._network_id)},
            "name": self._network_name,
            "manufacturer": "Cisco Meraki",
            "model": "Network",
        }
