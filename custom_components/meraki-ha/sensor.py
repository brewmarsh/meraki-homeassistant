"""Sensor platform for the meraki_ha integration."""
import logging
from typing import Any, Dict, List

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DATA_COORDINATOR

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform for the Meraki integration.

    Args:
        hass: Home Assistant instance.
        entry: Config entry for the integration.
        async_add_entities: Callback to add entities.
    """
    _LOGGER.debug("sensor.py async_setup_entry called")
    try:
        coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

        sensors: List[SensorEntity] =
        for device in coordinator.data:
            if device["model"].startswith("MR") or device["model"].startswith("GR"):
                sensors.append(MerakiConnectedClientsSensor(coordinator, device))
                sensors.append(MerakiRadioSettingsSensor(coordinator, device))
        async_add_entities(sensors)
        _LOGGER.debug(f"Meraki Sensors added: {sensors}")
    except Exception as e:
        _LOGGER.error(f"Error setting up meraki_ha sensors: {e}")

class MerakiConnectedClientsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Connected Clients sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Connected Clients sensor.

        Args:
            coordinator: DataUpdateCoordinator instance.
            device: Device data from the Meraki API.
        """
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{device['name']} Connected Clients"
        self._attr_unique_id = f"{device['serial']}_connected_clients"
        self._attr_icon = "mdi:account-network"
        _LOGGER.debug(f"Meraki Sensor Initialized: {self._attr_name}")

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        if isinstance(self._device.get("connected_clients"), list):
            return len(self._device["connected_clients"])
        else:
            return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes of the sensor."""
        return {"clients": self._device.get("connected_clients")}

class MerakiRadioSettingsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Radio Settings sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Radio Settings sensor.

        Args:
            coordinator: DataUpdateCoordinator instance.
            device: Device data from the Meraki API.
        """
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{device['name']} Radio Settings"
        self._attr_unique_id = f"{device['serial']}_radio_settings"
        self._attr_icon = "mdi:wifi"
        _LOGGER.debug(f"Meraki Radio Sensor Initialized: {self._attr_name}")

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        if self._device.get("radio_settings"):
            return self._device["radio_settings"].get("channel")
        else:
            return "Unavailable"

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

class MerakiWirelessRadioSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Wireless Radio Sensor."""

    def __init__(self, coordinator, device, band, radio_data):
        """Initialize the wireless radio sensor."""
        super().__init__(coordinator)
        self._device = device
        self._band = band
        self._radio_data = radio_data
        self._attr_name = f"{device['name']} {band} Radio"
        self._attr_unique_id = f"{device['serial']}-{band}-radio"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._radio_data.get("channel", "unknown")

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attributes = {
            "target_power": self._radio_data.get("targetPower"),
            "channel_width": self._radio_data.get("channelWidth"),
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
