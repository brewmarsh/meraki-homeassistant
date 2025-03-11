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
    coordinator = hass.data[DOMAIN][config_entry.entry_id][DATA_COORDINATOR]

    await coordinator.async_config_entry_first_refresh()

    sensors = []
    for device in coordinator.data:
        sensors.append(MerakiDeviceSensor(coordinator, device))
        if device.get("uplinks"):
            for interface, uplink_data in device["uplinks"].items():
                sensors.append(MerakiUplinkSensor(coordinator, device, interface, uplink_data))

    async_add_entities(sensors)

class MerakiDeviceSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Device Sensor."""
    # ... (Your existing MerakiDeviceSensor code)

class MerakiUplinkSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Uplink Sensor."""

    def __init__(self, coordinator, device, interface, uplink_data):
        """Initialize the uplink sensor."""
        super().__init__(coordinator)
        self._device = device
        self._interface = interface
        self._uplink_data = uplink_data
        self._attr_name = f"{device['name']} {interface} Uplink"
        self._attr_unique_id = f"{device['serial']}-{interface}-uplink"

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._uplink_data.get("enabled"):
            return "Enabled"
        else:
            return "Disabled"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attributes = {
            "vlan_enabled": self._uplink_data.get("vlanTagging", {}).get("enabled"),
            "vlan_id": self._uplink_data.get("vlanTagging", {}).get("vlanId"),
            "ipv4_assignment": self._uplink_data.get("svis", {}).get("ipv4", {}).get("assignmentMode"),
            "ipv4_address": self._uplink_data.get("svis", {}).get("ipv4", {}).get("address"),
            "ipv4_gateway": self._uplink_data.get("svis", {}).get("ipv4", {}).get("gateway"),
            "ipv4_nameservers": self._uplink_data.get("svis", {}).get("ipv4", {}).get("nameservers", {}).get("addresses"),
            "pppoe_enabled": self._uplink_data.get("pppoe", {}).get("enabled"),
            "pppoe_username": self._uplink_data.get("pppoe", {}).get("authentication", {}).get("username"),
            ATTR_ATTRIBUTION: ATTRIBUTION,
        }
        return {k: v for k, v in attributes.items() if v is not None}

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