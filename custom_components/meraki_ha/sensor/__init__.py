"""Sensor platform for meraki_ha."""

import logging
from typing import List

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import SensorEntity

from .device_status import MerakiDeviceStatusSensor
from .connected_clients import MerakiConnectedClientsSensor
from .radio_settings import MerakiRadioSettingsSensor
from .uplink_status import MerakiUplinkStatusSensor
from .network_clients import MerakiNetworkClientCountSensor
from .ssid import create_ssid_sensors
from .ssid_availability import MerakiSSIDAvailabilitySensor
from ..meraki_api.networks import get_network_ids_and_names
from ..const import DOMAIN, DATA_COORDINATOR, ATTR_SSIDS
from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Meraki sensors."""
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]

    sensors: List[SensorEntity] = []

    devices = coordinator.data.get("devices", [])
    _LOGGER.debug(f"sensor.py: Found {len(devices)} devices in coordinator data.")

    for device in devices:
        _LOGGER.debug(
            f"Meraki: Processing device: {device.get('name')}, Serial: {device.get('serial')}, Model: {device.get('model')}"
        )
        sensors.append(MerakiDeviceStatusSensor(coordinator, device))
        if device.get("model", "").startswith("MR") or device.get(
            "model", ""
        ).startswith("GR"):
            _LOGGER.debug(f"Meraki: Adding MR/GR sensors for {device.get('name')}")
            sensors.append(MerakiConnectedClientsSensor(coordinator, device))
            sensors.append(MerakiRadioSettingsSensor(coordinator, device))
            if device.get(ATTR_SSIDS):
                for ssid in device[ATTR_SSIDS]:
                    _LOGGER.debug(
                        f"Creating SSID sensors for {ssid['name']} on device {device['serial']}"
                    )
                    sensors.extend(create_ssid_sensors(coordinator, device, ssid))
                    sensors.append(
                        MerakiSSIDAvailabilitySensor(coordinator, device, ssid)
                    )  # Add this line
        elif device.get("model", "").startswith("MX"):
            _LOGGER.debug(f"Meraki: Adding MX sensors for {device.get('name')}")
            sensors.append(MerakiUplinkStatusSensor(coordinator, device))

    networks = await get_network_ids_and_names(coordinator.api_key, coordinator.org_id)
    _LOGGER.debug(f"sensor.py: Networks retrieved: {networks}")

    if networks is not None:
        for network in networks:
            sensors.append(
                MerakiNetworkClientCountSensor(
                    coordinator, network["id"], network["name"]
                )
            )

    async_add_entities(sensors)
