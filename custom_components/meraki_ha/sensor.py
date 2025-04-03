"""Provide sensor platform for the meraki_ha integration."""

import logging
import traceback
from typing import List, Any, Dict

import aiohttp

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DATA_COORDINATOR,
    DOMAIN,
    SENSOR_CLIENT_COUNT,
    SENSOR_SSID_AVAILABILITY,
    SENSOR_SSID_CHANNEL,
    ATTR_CONNECTED_CLIENTS,
    ATTR_SSIDS,
    CONF_RELAXED_TAG_MATCHING,
)
from .meraki_api.networks import get_network_clients_count, get_network_ids_and_names
from .sensor_connected_clients import MerakiConnectedClientsSensor
from .sensor_device_status import MerakiDeviceStatusSensor
from .sensor_radio_settings import MerakiRadioSettingsSensor
from .sensor_uplink_status import MerakiUplinkStatusSensor

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
        coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
        _LOGGER.debug(f"Coordinator data: {coordinator.data}")

        sensors: List[SensorEntity] = []
        switches: List[SwitchEntity] = []  # added switch list

        _LOGGER.debug(f"Device Data in Coordinator: {coordinator.data.get('devices')}")

        relaxed_matching = entry.options.get(
            CONF_RELAXED_TAG_MATCHING, False
        )  # Get relaxed matching config

        for device in coordinator.data["devices"]:
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
        for device in coordinator.data["devices"]:
            if device.get(ATTR_SSIDS):
                for ssid in device[ATTR_SSIDS]:
                    # Match devices to ssid using tags
                    if match_device_to_ssid(
                        ssid, coordinator.data["devices"], relaxed_matching
                    ):
                        switches.append(MerakiSsidSwitch(coordinator, device, ssid))

        async with aiohttp.ClientSession() as session:
            networks = await get_network_ids_and_names(
                coordinator.config_entry.options.get("meraki_api_key"),
                coordinator.config_entry.options.get("meraki_org_id"),
                session,
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
        async with aiohttp.ClientSession() as session:
            self._attr_native_value = await get_network_clients_count(
                self._coordinator.config_entry.options.get("meraki_api_key"),
                self._network_id,
                session,  # Updated to get from config_entry
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


class MerakiSSIDAvailabilitySensor(SensorEntity):
    """Sensor to track the availability of a Meraki SSID."""

    def __init__(self, coordinator, device, ssid):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._device = device
        self._ssid = ssid
        self._attr_name = f"{device['name']} - {ssid['name']} Availability"
        self._attr_unique_id = f"{device['serial']}-{ssid['name']}-availability"
        self._attr_device_class = SENSOR_SSID_AVAILABILITY

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return "Enabled" if self._ssid.get("enabled", False) else "Disabled"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
            manufacturer="Cisco Meraki",
            model=self._device["model"],
        )


class MerakiSSIDChannelSensor(SensorEntity):
    """Sensor to track the channel of a Meraki SSID."""

    def __init__(self, coordinator, device, ssid):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._device = device
        self._ssid = ssid
        self._attr_name = f"{device['name']} - {ssid['name']} Channel"
        self._attr_unique_id = f"{device['serial']}-{ssid['name']}-channel"
        self._attr_device_class = SENSOR_SSID_CHANNEL

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._ssid.get("channel")

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
            manufacturer="Cisco Meraki",
            model=self._device["model"],
        )


class MerakiSSIDClientCountSensor(SensorEntity):
    """Sensor to track the client count of a Meraki SSID."""

    def __init__(self, coordinator, device, ssid):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._device = device
        self._ssid = ssid
        self._attr_name = f"{device['name']} - {ssid['name']} Client Count"
        self._attr_unique_id = f"{device['serial']}-{ssid['name']}-client-count"
        self._attr_device_class = SENSOR_CLIENT_COUNT

    @property
    def native_value(self):
        """Return the state of the sensor."""
        clients = self._device.get(ATTR_CONNECTED_CLIENTS, [])
        return len(
            [
                client
                for client in clients
                if client.get("ssidName") == self._ssid.get("name")
            ]
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device["serial"])},
            name=self._device["name"],
            manufacturer="Cisco Meraki",
            model=self._device["model"],
        )


class MerakiSsidSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Meraki SSID switch."""

    def __init__(
        self,
        coordinator: CoordinatorEntity,
        device: Dict[str, Any],
        ssid: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki SSID switch."""
        super().__init__(coordinator)
        self._device = device
        self._ssid = ssid
        self._attr_name = f"{device['name']} - {ssid['name']} Enabled"
        self._attr_unique_id = f"{device['serial']}_{ssid['number']}_enabled"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"{device['serial']}_{ssid['number']}")},
        }
        self._is_on = ssid.get("enabled", True)

    @property
    def is_on(self) -> bool:
        """Return the state of the switch."""
        return self._is_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._async_set_ssid_enabled(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._async_set_ssid_enabled(False)

    async def _async_set_ssid_enabled(self, enabled: bool) -> None:
        """Set the SSID enabled state."""
        network_id = self._device.get("networkId")
        ssid_number = self._ssid.get("number")
        if not network_id or ssid_number is None:
            _LOGGER.error("Network ID or SSID number not found.")
            return

        url = f"https://api.meraki.com/api/v1/networks/{network_id}/wireless/ssids/{ssid_number}"
        headers = {
            "X-Cisco-Meraki-API-Key": self.coordinator.config_entry.options.get(
                "meraki_api_key"
            ),
            "Content-Type": "application/json",
        }
        payload = {"enabled": enabled}
        try:
            async with self.coordinator.session.put(
                url, headers=headers, json=payload
            ) as response:
                response.raise_for_status()
            self._is_on = enabled
            self.async_write_ha_state()
            await self._async_validate_ssid_status()  # validate the state with GET /devices/{serial}/wireless/status
        except Exception as e:
            _LOGGER.error(f"Failed to set SSID enabled state: {e}")

    async def _async_validate_ssid_status(self):
        """Validate the SSID status using GET /devices/{serial}/wireless/status."""
        serial = self._device.get("serial")
        if not serial:
            _LOGGER.error("Device serial number not found.")
            return

        url = f"https://api.meraki.com/api/v1/devices/{serial}/wireless/status"
        headers = {
            "X-Cisco-Meraki-API-Key": self.coordinator.config_entry.options.get(
                "meraki_api_key"
            ),
        }
        try:
            async with self.coordinator.session.get(url, headers=headers) as response:
                response.raise_for_status()
                wireless_status = await response.json()
                for ssid_status in wireless_status.get("ssids", []):
                    if ssid_status.get("number") == self._ssid.get("number"):
                        self._is_on = ssid_status.get("enabled", False)
                        self.async_write_ha_state()
                        return
                _LOGGER.warning(
                    f"SSID number {self._ssid.get('number')} not found in device wireless status."
                )
        except Exception as e:
            _LOGGER.error(f"Failed to validate SSID status: {e}")
