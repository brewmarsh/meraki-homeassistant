"""Sensor entity for displaying Meraki device wireless radio settings.

This module defines the `MerakiRadioSettingsSensor`, a Home Assistant sensor
entity that primarily displays the current wireless channel of a Meraki device.
Additional radio settings are exposed as state attributes.
"""

import logging
from typing import Any, Dict

from typing import Any, Dict, Optional # Added Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback # For _handle_coordinator_update

# Assuming MerakiDataUpdateCoordinator is the type of coordinator used.
from ..coordinator import MerakiDataUpdateCoordinator
from ..meraki_api.wireless import get_meraki_device_wireless_radio_settings

_LOGGER = logging.getLogger(__name__)

# Constants for sensor state if data is unavailable or an error occurs.
STATE_UNAVAILABLE_VALUE = "Unavailable"
STATE_ERROR_VALUE = "Error"


class MerakiRadioSettingsSensor(CoordinatorEntity, SensorEntity):
    """Represents a sensor for Meraki device wireless radio settings.

    This sensor displays the primary radio channel (e.g., from 2.4GHz or 5GHz band,
    often the first one reported or a specific band's channel) as its main state.
    Other detailed radio settings fetched from the API are exposed as extra
    state attributes.

    The sensor uses its own `async_update` method to fetch data directly,
    rather than relying on pre-fetched data from the main coordinator that
    might be aggregated. This is suitable for endpoint-specific data that isn't
    part of a bulk update.

    Attributes:
        _device_info (Dict[str, Any]): Raw device information from the Meraki API.
        _attr_name (str): The friendly name of the sensor.
        _attr_unique_id (str): The unique ID for this sensor entity.
        _attr_icon (str): The icon for the sensor.
        _attr_extra_state_attributes (Dict[str, Any]): Stores additional radio
            settings and device details.
        _attr_native_value (Optional[str]): The current value of the sensor,
            typically the radio channel or a status string.
    """

    def __init__(
        self, coordinator: MerakiDataUpdateCoordinator, device_info: Dict[str, Any]
    ) -> None:
        """Initializes the Meraki Radio Settings sensor.

        Args:
            coordinator (MerakiDataUpdateCoordinator): The main data update coordinator,
                used here to access shared information like API key and org ID.
            device_info (Dict[str, Any]): A dictionary containing the Meraki
                device's information (name, serial, model, etc.).
        """
        # Pass the main coordinator, though this sensor updates independently.
        super().__init__(coordinator)
        self._device_info = device_info
        device_name = device_info.get(
            "name", device_info.get("serial", "Unknown Device")
        )
        device_serial = device_info.get("serial", "unknown_serial")

        # Set Home Assistant entity attributes
        self._attr_name = f"{device_name} Radio Settings"
        self._attr_unique_id = f"{device_serial}_radio_settings"
        self._attr_icon = "mdi:wifi-settings" # Icon representing Wi-Fi settings

        # Initialize extra state attributes with basic device info.
        # These will be updated with radio-specific settings in async_update.
        self._attr_extra_state_attributes: Dict[str, Any] = {
            "model": device_info.get("model"),
            "serial_number": device_serial,
            "firmware_version": device_info.get("firmware"),
            "mac_address": device_info.get("mac"),
        }
        self._attr_native_value: Optional[str] = None # Initialize native_value

        _LOGGER.debug(
            "Meraki Radio Settings Sensor initialized for %s (Serial: %s)",
            self._attr_name,
            device_serial,
        )

    # This sensor fetches its own data directly rather than using _handle_coordinator_update
    # because radio settings are specific to a device and might not be part of the main coordinator's bulk data.
    # If radio settings were part of the main coordinator.data, _handle_coordinator_update would be preferred.
    async def async_update(self) -> None:
        """Fetches the latest radio settings for the device and updates sensor state.

        This method is called periodically by Home Assistant. It makes a direct
        API call to get the wireless radio settings for this specific device.
        The primary channel is set as the sensor's state, and all other fetched
        radio settings are added to the extra state attributes.
        """
        _LOGGER.debug("Updating radio settings sensor state for %s", self._attr_name)
        device_serial = self._device_info.get("serial")
        if not device_serial:
            _LOGGER.error("Device serial is missing for radio settings sensor %s. Cannot update.", self._attr_name)
            self._attr_native_value = STATE_ERROR_VALUE
            return

        try:
            # Fetch radio settings directly using the API function.
            # self.coordinator is the MerakiDataUpdateCoordinator instance.
            radio_settings = await get_meraki_device_wireless_radio_settings(
                self.coordinator.api_key,  # API key from the main coordinator
                device_serial, # Changed from self.coordinator.org_id
                               # The API endpoint for device radio settings only needs serial.
                               # Original code had self.coordinator.org_id as second param, which is incorrect for this function.
            )

            if radio_settings:
                # Determine the primary state value.
                # The API returns settings for different bands (e.g., twoFourGhzSettings, fiveGhzSettings).
                # We need to pick a representative value, e.g., the channel of the first active band or a specific band.
                # For simplicity, let's try to get a channel from common band keys.
                # This logic might need adjustment based on the exact structure and desired primary state.
                primary_channel = None
                if isinstance(radio_settings.get("twoFourGhzSettings"), dict) and radio_settings["twoFourGhzSettings"].get("channel"):
                    primary_channel = radio_settings["twoFourGhzSettings"]["channel"]
                elif isinstance(radio_settings.get("fiveGhzSettings"), dict) and radio_settings["fiveGhzSettings"].get("channel"):
                    primary_channel = radio_settings["fiveGhzSettings"]["channel"]
                elif radio_settings.get("channel"): # Fallback if a top-level 'channel' exists (less common for detailed radio settings)
                    primary_channel = radio_settings["channel"]

                if primary_channel is not None:
                    self._attr_native_value = str(primary_channel) # Ensure it's a string
                else:
                    self._attr_native_value = STATE_UNAVAILABLE_VALUE
                    _LOGGER.warning("No primary channel found in radio settings for %s: %s", device_serial, radio_settings)

                # Update extra state attributes with all fetched radio settings.
                # Start with base device info and then update/add radio specifics.
                current_attributes = {
                    "model": self._device_info.get("model"),
                    "serial_number": device_serial,
                    "firmware_version": self._device_info.get("firmware"), # This might also come from coordinator if fresher
                    "mac_address": self._device_info.get("mac"),
                }
                current_attributes.update(radio_settings) # Add all fetched radio settings
                self._attr_extra_state_attributes = current_attributes
            else:
                # API returned no data or empty data.
                _LOGGER.warning("No radio settings data returned for device %s.", device_serial)
                self._attr_native_value = STATE_UNAVAILABLE_VALUE
                # Keep basic attributes, remove radio-specific ones if they were there.
                self._attr_extra_state_attributes = {
                    "model": self._device_info.get("model"),
                    "serial_number": device_serial,
                    "firmware_version": self._device_info.get("firmware"),
                    "mac_address": self._device_info.get("mac"),
                    "status_reason": "No data from API",
                }

        except Exception as e:
            _LOGGER.error(
                "Error fetching radio settings for device %s: %s", device_serial, e
            )
            self._attr_native_value = STATE_ERROR_VALUE
            self._attr_extra_state_attributes["error_message"] = str(e)
        # async_write_ha_state() is called by SensorEntity base class after async_update.

    @property
    def native_value(self) -> Optional[str]:
        """Return the current state of the sensor (e.g., radio channel or status)."""
        return self._attr_native_value

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity-specific state attributes, including detailed radio settings."""
        return self._attr_extra_state_attributes.copy()
