"""Provide sensor platform for the meraki_ha integration."""

import logging
import traceback
from typing import List

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DATA_COORDINATOR,
    DOMAIN,
    ATTR_SSIDS,
)
from .meraki_api.networks import get_network_clients_count, get_network_ids_and_names
from .sensor_connected_clients import MerakiConnectedClientsSensor
from .sensor_device_status import MerakiDeviceStatusSensor
from .sensor_radio_settings import MerakiRadioSettingsSensor
from .sensor_uplink_status import MerakiUplinkStatusSensor
from .coordinator import MerakiDataUpdateCoordinator  # Corrected import
from .sensor_ssid_availability import MerakiSSIDAvailabilitySensor
from .sensor_ssid_channel import MerakiSSIDChannelSensor
from .sensor_ssid_client_count import MerakiSSIDClientCountSensor
from .meraki_ssid_switch import MerakiSsidSwitch

_LOGGER = logging.getLogger(__name__)


def match_device_to_ssid(ssid, devices, relaxed_matching):
    """Match a device to an SSID based on tags."""
    ssid_tags = ssid.get("tags", [])
    if not ssid_tags:
        return True  # SSID has no tags, so any device can match.
    for device in devices:
        device_tags = device.get("tags", [])
        if not device_tags:
            continue
        if relaxed_matching:
            if any(tag in device_tags for tag in ssid_tags):
                return True
        else:
            if all(tag in device_tags for tag in ssid_tags):
                return True
    return False


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform for the Meraki integration."""
    _LOGGER.debug("Meraki: sensor.py async_setup_entry called")
    try:
        coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
            DATA_COORDINATOR
        ]
        _LOGGER.debug(f"Coordinator data: {coordinator.data}")

        sensors: List[SensorEntity] = []
        switches: List[SwitchEntity] = []  # added switch list

        _LOGGER.debug(f"Device Data in Coordinator: {coordinator.data.get('devices')}")

        relaxed_matching = (
            coordinator.relaxed_tag_match
        )  # Get relaxed matching from coordinator

        for device in coordinator.data.get(
            "devices", []
        ):  # Added .get to prevent KeyError
            _LOGGER.debug(f"Meraki: Processing device: {device['name']}")
            _LOGGER.debug(f"Device model: {device['model']}")
            sensors.append(MerakiDeviceStatusSensor(coordinator, device))
            if device["model"].startswith("MR") or device["model"].startswith("GR"):
                _LOGGER.debug(f"Meraki: Adding MR/GR sensors for {device['name']}")
                sensors.append(MerakiConnectedClientsSensor(coordinator, device))
                sensors.append(MerakiRadioSettingsSensor(coordinator, device))
                if device.get(ATTR_SSIDS):
                    for ssid in device[ATTR_SSIDS]:
                        _LOGGER.debug(
                            f"Creating SSID sensors for {ssid['name']} on device {device['serial']}"
                        )
                        sensors.extend(create_ssid_sensors(coordinator, device, ssid))
            elif device["model"].startswith("MX"):
                _LOGGER.debug(f"Meraki: Adding MX sensors for {device['name']}")
                sensors.append(MerakiUplinkStatusSensor(coordinator, device))

        # Add SSID switches
        for device in coordinator.data.get(
            "devices", []
        ):  # Added .get to prevent KeyError
            if device.get(ATTR_SSIDS):
                for ssid in device[ATTR_SSIDS]:
                    # Match devices to ssid using tags
                    if match_device_to_ssid(
                        ssid,
                        coordinator.data.get("devices", []),
                        relaxed_matching,  # Added .get to prevent KeyError
                    ):
                        switches.append(MerakiSsidSwitch(coordinator, device, ssid))

        networks = await get_network_ids_and_names(
            coordinator.api_key,  # Get API key from coordinator
            coordinator.org_id,  # Get org ID from coordinator
        )
        _LOGGER.debug(f"sensor.py: Networks retrieved: {networks}")

        if networks is not None:
            for network in networks:
                sensors.append(
                    MerakiNetworkClientCountSensor(
                        coordinator, network["id"], network["name"]
                    )
                )

        _LOGGER.debug(f"Total sensors added: {len(sensors)}")
        _LOGGER.debug(f"Total switches added: {len(switches)}")

        async_add_entities(sensors + switches)  # add switches to entities
    except KeyError as e:
        _LOGGER.error(f"Meraki: KeyError setting up meraki_ha sensors: {e}")
        _LOGGER.error(f"Traceback: {traceback.format_exc()}")
    except TypeError as e:
        _LOGGER.error(f"Meraki: TypeError setting up meraki_ha sensors: {e}")
        _LOGGER.error(f"Traceback: {traceback.format_exc()}")
    except ValueError as e:
        _LOGGER.error(f"Meraki: ValueError setting up meraki_ha sensors: {e}")
        _LOGGER.error(f"Traceback: {traceback.format_exc()}")
    except Exception as e:
        _LOGGER.error(f"Meraki: Unexpected error setting up meraki_ha sensors: {e}")
        _LOGGER.error(f"Traceback: {traceback.format_exc()}")


def create_ssid_sensors(coordinator, device, ssid):
    """Create sensor entities for a given SSID."""
    sensors = []
    sensors.append(MerakiSSIDAvailabilitySensor(coordinator, device, ssid))
    sensors.append(MerakiSSIDChannelSensor(coordinator, device, ssid))
    sensors.append(MerakiSSIDClientCountSensor(coordinator, device, ssid))
    # Add other sensor types as needed
    return sensors


class MerakiNetworkClientCountSensor(SensorEntity):
    def __init__(self, coordinator, network_id, network_name):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._network_id = network_id
        self._network_name = network_name
        self._attr_name = f"Meraki Network Clients {network_name}"
        self._attr_unique_id = f"meraki_network_clients_{network_id}"

    async def async_update(self):
        self._attr_native_value = await get_network_clients_count(
            self._coordinator.api_key,  # Get API key from coordinator
            self._network_id,
        )
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._network_id)},
            name=self._network_name,
            manufacturer="Cisco Meraki",
            model="Network",
        )
