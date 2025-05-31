# custom_components/meraki_ha/sensor/meraki_ssid_psk.py
"""Sensor entity for displaying Meraki SSID PSK."""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator

_LOGGER = logging.getLogger(__name__)

# Define common PSK-based auth modes. This might need to be expanded based on Meraki's API.
PSK_AUTH_MODES = [
    "psk",
    "wpa-psk",
    "wpa2-psk",
    "wpa3-psk", # Assuming WPA3 PSK modes if Meraki supports them via similar naming
    "wpa-eap-psk", # Example, if such mixed modes exist and expose a PSK
]

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki SSID PSK sensors from a config entry."""
    ssid_coordinator: SSIDDeviceCoordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinators"]["ssid_devices"]

    if not ssid_coordinator.data:
        _LOGGER.warning("SSID Coordinator has no data, skipping PSK sensor setup")
        return

    sensors_to_add = []
    for ssid_unique_id, ssid_data in ssid_coordinator.data.items():
        auth_mode = ssid_data.get("authMode", "").lower()
        # Only add a PSK sensor if the auth mode is PSK-based and a PSK might exist
        if any(psk_mode in auth_mode for psk_mode in PSK_AUTH_MODES):
            # Further check if psk field is actually present, though it might be None/empty
            if "psk" in ssid_data:
                 sensors_to_add.append(MerakiSSIDPskSensor(ssid_coordinator, config_entry, ssid_unique_id, ssid_data))
            else:
                _LOGGER.debug(f"SSID {ssid_data.get('name')} uses PSK auth mode '{auth_mode}' but 'psk' field not found in data. Skipping PSK sensor.")
        else:
            _LOGGER.debug(f"SSID {ssid_data.get('name')} auth mode '{auth_mode}' is not PSK-based. Skipping PSK sensor.")

    async_add_entities(sensors_to_add, update_before_add=True)


class MerakiSSIDPskSensor(CoordinatorEntity[SSIDDeviceCoordinator], SensorEntity):
    """Representation of a Meraki SSID's PSK as a sensor entity."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:key-variant"

    def __init__(
        self,
        coordinator: SSIDDeviceCoordinator,
        config_entry: ConfigEntry,
        ssid_unique_id: str, # HA device unique_id for the SSID
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki SSID PSK sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._ssid_unique_id = ssid_unique_id

        self._network_id = ssid_data.get("networkId")
        self._ssid_number = ssid_data.get("number")
        ssid_name = ssid_data.get("name", f"SSID {self._ssid_number}")

        self._attr_unique_id = f"{self._ssid_unique_id}_psk_sensor"
        self._attr_name = f"{ssid_name} PSK" # e.g., "Guest WiFi PSK"

        self._update_internal_state(ssid_data) # Set initial state

    def _is_psk_auth_mode(self, ssid_data: Optional[Dict[str, Any]]) -> bool:
        """Check if the SSID's authMode is PSK-based."""
        if not ssid_data:
            return False
        auth_mode = ssid_data.get("authMode", "").lower()
        return any(psk_mode in auth_mode for psk_mode in PSK_AUTH_MODES)

    def _update_internal_state(self, current_ssid_data: Optional[Dict[str, Any]]) -> None:
        """Update the internal state of the sensor based on coordinator data."""
        if current_ssid_data and self._is_psk_auth_mode(current_ssid_data):
            self._attr_native_value = current_ssid_data.get("psk") # Will be None if PSK is not set but authMode is PSK
            # Update name if SSID name changed
            ssid_name = current_ssid_data.get("name", f"SSID {self._ssid_number}")
            self._attr_name = f"{ssid_name} PSK"
        else:
            # Not a PSK auth mode, or data not found
            self._attr_native_value = None # Or "Not Applicable"
            if current_ssid_data: # Keep name updated if data exists but not PSK mode
                ssid_name = current_ssid_data.get("name", f"SSID {self._ssid_number}")
                self._attr_name = f"{ssid_name} PSK"

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information to link this entity to the SSID device."""
        return {
            "identifiers": {(DOMAIN, self._ssid_unique_id)},
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        current_ssid_data = self.coordinator.data.get(self._ssid_unique_id)
        self._update_internal_state(current_ssid_data)
        self.async_write_ha_state()
