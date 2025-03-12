"""Sensor platform for the meraki_ha integration."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_COORDINATOR, DOMAIN
from .meraki_api.appliance import get_meraki_device_appliance_uplinks
from .meraki_api.exceptions import MerakiApiError

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
        _LOGGER.debug(f"Meraki: Device data: {device}")  # Added for debugging.
        self._attr_name = f"{device['name']} Connected Clients"
        self._attr_unique_id = f"{device['serial']}_connected_clients"
        self._attr_icon = "mdi:account-network"
        self._attr_extra_state_attributes = {
            "model": device.get("model"),
            "serial_number": device.get("serial"),
            "firmware_version": device.get("firmware"),
        }
        self._attr_extra_state_attributes["serial_number"] = device.get(
            "serial"
        )  # Added to make extra sure.
        _LOGGER.debug(
            f"Meraki: Connected Clients Sensor Initialized: {self._attr_name}"
        )

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        _LOGGER.debug(f"Meraki: Getting native value for {self._attr_name}")
        if isinstance(self._device.get("connected_clients"), list):
            return len(self._device["connected_clients"])
        else:
            return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes of the sensor."""
        _LOGGER.debug(f"Meraki: Getting extra state attributes for {self._attr_name}")
        return self._attr_extra_state_attributes.copy()


class MerakiRadioSettingsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Radio Settings sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Radio Settings sensor."""
        super().__init__(coordinator)
        self._device = device
        _LOGGER.debug(f"Meraki: Device data: {device}")  # Added for debugging.
        self._attr_name = f"{device['name']} Radio Settings"
        self._attr_unique_id = f"{device['serial']}_radio_settings"
        self._attr_icon = "mdi:wifi"
        self._attr_extra_state_attributes = {
            "model": device.get("model"),
            "serial_number": device.get("serial"),
            "firmware_version": device.get("firmware"),
        }
        self._attr_extra_state_attributes["serial_number"] = device.get(
            "serial"
        )  # Added to make extra sure.
        _LOGGER.debug(f"Meraki: Radio Sensor Initialized: {self._attr_name}")

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        _LOGGER.debug(f"Meraki: Getting native value for {self._attr_name}")
        if self._device.get("radio_settings"):
            return self._device["radio_settings"].get("channel")
        else:
            return "Unavailable"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes of the sensor."""
        _LOGGER.debug(f"Meraki: Getting extra state attributes for {self._attr_name}")
        return self._attr_extra_state_attributes.copy()


class MerakiUplinkStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki MX Appliance Uplink Status sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki MX Appliance Uplink Status sensor."""
        super().__init__(coordinator)
        self._device = device
        _LOGGER.debug(f"Meraki: Device data: {device}")  # Added for debugging.
        self._attr_name = f"{device['name']} Uplink Status"
        self._attr_unique_id = f"{device['serial']}_uplink_status"
        self._attr_icon = "mdi:upload-network-outline"
        self._attr_extra_state_attributes = {
            "model": device.get("model"),
            "serial_number": device.get("serial"),
            "firmware_version": device.get("firmware"),
        }
        self._attr_extra_state_attributes["serial_number"] = device.get(
            "serial"
        )  # Added to make extra sure.
        _LOGGER.debug(f"Meraki: Uplink Sensor Initialized: {self._attr_name}")

    async def async_update(self) -> None:
        """Update the sensor state."""
        _LOGGER.debug(f"Meraki: Updating sensor state for {self._attr_name}")
        try:
            uplinks = await get_meraki_device_appliance_uplinks(
                self.coordinator.api_key,
                self.coordinator.org_id,
                self._device["serial"],
            )
            if uplinks and uplinks.get("uplinks"):
                self._attr_native_value = uplinks["uplinks"][0].get("status", "Unknown")
                self._attr_extra_state_attributes.update(
                    {"uplinks": uplinks.get("uplinks")}
                )
            else:
                self._attr_native_value = "Unavailable"
                self._attr_extra_state_attributes.update({"uplinks": None})
        except MerakiApiError as e:
            _LOGGER.error(f"Meraki: Error fetching uplink status: {e}")
            self._attr_native_value = "Error"
        except Exception as e:
            _LOGGER.error(f"Meraki: Unexpected error fetching uplink status: {e}")
            self._attr_native_value = "Error"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self._attr_native_value

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes of the sensor."""
        return self._attr_extra_state_attributes.copy()


class MerakiDeviceStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki Device Status sensor."""

    def __init__(self, coordinator, device: Dict[str, Any]) -> None:
        """Initialize the Meraki Device Status sensor."""
        super().__init__(coordinator)
        self._device = device
        self._attr_name = f"{device['name']} Status"
        self._attr_unique_id = f"{device['serial']}_status"
        self._attr_icon = "mdi:information-outline"
        self._attr_extra_state_attributes = {
            "model": device.get("model"),
            "serial_number": device.get("serial"),
            "firmware_version": device.get("firmware"),
        }

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        if self._device.get("productType") == "appliance":
            return "Appliance"
        elif self._device.get("productType") == "wireless":
            return "Wireless"
        elif self._device.get("productType") == "switch":
            return "Switch"
        elif self._device.get("productType") == "camera":
            return "Camera"
        elif self._device.get("productType") == "sensor":
            return "Sensor"
        else:
            return "Unknown"
