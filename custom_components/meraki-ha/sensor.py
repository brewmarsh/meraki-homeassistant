"""Sensor platform for the meraki_ha integration."""
import logging
from typing import Any, Dict

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
    """Set up the sensor platform for the Meraki integration."""
    _LOGGER.debug("Meraki: sensor.py async_setup_entry called")
    try:
        coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]

        sensors: list[SensorEntity] = []
        for device in coordinator.data:
            _LOGGER.debug(f"Meraki: Processing device: {device['name']}") # Added logging
            if device["model"].startswith("MR") or device["model"].startswith("GR"):
                _LOGGER.debug(f"Meraki: Adding sensors for {device['name']}") # Added logging
                sensors.append(MerakiConnectedClientsSensor(coordinator, device))
                sensors.append(MerakiRadioSettingsSensor(coordinator, device))
        async_add_entities(sensors)
        _LOGGER.debug(f"Meraki: Meraki Sensors added: {sensors}")
    except Exception as e:
        _LOGGER.error(f"Meraki: Error setting up meraki_ha sensors: {e}")

class MerakiConnectedClientsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Connected Clients sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Connected Clients sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{device['name']} Connected Clients"
        self._attr_unique_id = f"{device['serial']}_connected_clients"
        self._attr_icon = "mdi:account-network"
        _LOGGER.debug(f"Meraki: Connected Clients Sensor Initialized: {self._attr_name}") # Added logging

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        _LOGGER.debug(f"Meraki: Getting native value for {self._attr_name}") # Added logging
        if isinstance(self._device.get("connected_clients"), list):
            return len(self._device["connected_clients"])
        else:
            return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes of the sensor."""
        _LOGGER.debug(f"Meraki: Getting extra state attributes for {self._attr_name}") # Added logging
        return {"clients": self._device.get("connected_clients")}

class MerakiRadioSettingsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Radio Settings sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Radio Settings sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{device['name']} Radio Settings"
        self._attr_unique_id = f"{device['serial']}_radio_settings"
        self._attr_icon = "mdi:wifi"
        _LOGGER.debug(f"Meraki: Radio Sensor Initialized: {self._attr_name}") # Added logging

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        _LOGGER.debug(f"Meraki: Getting native value for {self._attr_name}") # Added logging
        if self._device.get("radio_settings"):
            return self._device["radio_settings"].get("channel")
        else:
            return "Unavailable"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes of the sensor."""
        _LOGGER.debug(f"Meraki: Getting extra state attributes for {self._attr_name}") # Added logging
        return {"radio_settings": self._device.get("radio_settings")}