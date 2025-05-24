"""Sensor entity for Meraki MX appliance uplink status.

This module defines the `MerakiUplinkStatusSensor`, a Home Assistant sensor
entity that displays the status of the primary uplink for a Meraki MX security
appliance.
"""

import logging
from typing import Any, Dict

from typing import Any, Dict, Optional # Added Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Assuming MerakiDataUpdateCoordinator is the type of coordinator used.
from ..coordinator import MerakiDataUpdateCoordinator
from ..meraki_api.appliance import get_meraki_device_appliance_uplinks
from ..meraki_api.exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)

# Constants for sensor state if data is unavailable or an error occurs.
STATE_UNAVAILABLE_VALUE = "Unavailable"
STATE_ERROR_VALUE = "Error"
STATE_UNKNOWN_VALUE = "Unknown"


class MerakiUplinkStatusSensor(CoordinatorEntity, SensorEntity):
    """Represents a sensor for the uplink status of a Meraki MX appliance.

    This sensor displays the status of the primary uplink interface (typically WAN 1)
    of a Meraki MX security appliance. Detailed information about all uplinks
    is usually provided in the `extra_state_attributes`.

    The sensor uses its own `async_update` method to fetch data directly via
    `get_meraki_device_appliance_uplinks`, as uplink status is specific to an
    MX device and might not be part of a bulk data update from the main coordinator.

    Attributes:
        _device_info (Dict[str, Any]): Raw device information from the Meraki API.
        _attr_name (str): The friendly name of the sensor.
        _attr_unique_id (str): The unique ID for this sensor entity.
        _attr_icon (str): The icon for the sensor.
        _attr_extra_state_attributes (Dict[str, Any]): Stores additional uplink
            details and device information.
        _attr_native_value (Optional[str]): The current status of the primary uplink.
    """

    def __init__(
        self, coordinator: MerakiDataUpdateCoordinator, device_info: Dict[str, Any]
    ) -> None:
        """Initializes the Meraki MX Appliance Uplink Status sensor.

        Args:
            coordinator (MerakiDataUpdateCoordinator): The main data update coordinator,
                used here to access shared information like API key.
            device_info (Dict[str, Any]): A dictionary containing the Meraki
                device's information (name, serial, model, etc.).
        """
        # Pass the main coordinator, though this sensor updates independently for its specific data.
        super().__init__(coordinator)
        self._device_info = device_info
        device_name = device_info.get(
            "name", device_info.get("serial", "Unknown Device")
        )
        device_serial = device_info.get("serial", "unknown_serial")

        # Set Home Assistant entity attributes
        self._attr_name = f"{device_name} Uplink Status"
        self._attr_unique_id = f"{device_serial}_uplink_status"
        self._attr_icon = "mdi:wan" # WAN / Uplink icon

        # Initialize extra state attributes with basic device info.
        # These will be updated with uplink-specific details in async_update.
        self._attr_extra_state_attributes: Dict[str, Any] = {
            "model": device_info.get("model"),
            "serial_number": device_serial,
            "firmware_version": device_info.get("firmware"),
            "mac_address": device_info.get("mac"),
            "lan_ip": device_info.get("lanIp"),
        }
        self._attr_native_value: Optional[str] = None # Initialize native_value

        _LOGGER.debug(
            "Meraki Uplink Status Sensor initialized for %s (Serial: %s)",
            self._attr_name,
            device_serial,
        )

    # This sensor fetches its own data directly via async_update.
    async def async_update(self) -> None:
        """Fetches the latest uplink status for the MX appliance and updates sensor state.

        This method is called periodically by Home Assistant. It makes a direct
        API call to get the uplink status for this specific MX device.
        The status of the first uplink interface is set as the sensor's state,
        and all fetched uplink data is added to `extra_state_attributes`.
        """
        _LOGGER.debug("Updating uplink status sensor for %s", self._attr_name)
        device_serial = self._device_info.get("serial")
        if not device_serial:
            _LOGGER.error("Device serial is missing for uplink sensor %s. Cannot update.", self._attr_name)
            self._attr_native_value = STATE_ERROR_VALUE
            return

        try:
            # Fetch uplink status directly using the API function.
            # `self.coordinator.org_id` might not be strictly necessary if the API call
            # `get_meraki_device_appliance_uplinks` only needs api_key and serial.
            # Adjusting the call based on the actual signature of get_meraki_device_appliance_uplinks.
            # The original code passed org_id, but the function in meraki_api/appliance.py
            # was updated to only require api_key and serial.
            uplink_data = await get_meraki_device_appliance_uplinks(
                self.coordinator.api_key,  # API key from the main coordinator
                device_serial,
            )

            # Reset/update extra attributes with latest full uplink data or clear if unavailable.
            # Start with base device info.
            current_attributes = {
                "model": self._device_info.get("model"),
                "serial_number": device_serial,
                "firmware_version": self._device_info.get("firmware"),
                "mac_address": self._device_info.get("mac"),
                "lan_ip": self._device_info.get("lanIp"),
            }

            if uplink_data and isinstance(uplink_data, list) and uplink_data: # API returns a list of interfaces
                # The API returns a list of uplink interface statuses.
                # We'll use the status of the first interface as the primary state.
                primary_uplink = uplink_data[0] # First interface in the list
                self._attr_native_value = primary_uplink.get("status", STATE_UNKNOWN_VALUE)
                # Store all uplink interface details in attributes.
                current_attributes["uplinks"] = uplink_data
                _LOGGER.debug("Uplink data for %s: Primary status: %s, All uplinks: %s",
                              device_serial, self._attr_native_value, uplink_data)
            elif isinstance(uplink_data, dict) and "interfaces" in uplink_data: # Older format check
                 # Handle potential older format if API changes or for backward compatibility
                interfaces = uplink_data.get("interfaces", [])
                if interfaces and isinstance(interfaces, list) and interfaces:
                    self._attr_native_value = interfaces[0].get("status", STATE_UNKNOWN_VALUE)
                    current_attributes["uplinks"] = interfaces
                else:
                    self._attr_native_value = STATE_UNAVAILABLE_VALUE
                    current_attributes["uplinks"] = None
            else:
                _LOGGER.warning("No uplink data or unexpected format returned for device %s: %s", device_serial, uplink_data)
                self._attr_native_value = STATE_UNAVAILABLE_VALUE
                current_attributes["uplinks"] = None

            self._attr_extra_state_attributes = current_attributes

        except MerakiApiError as e:
            _LOGGER.error("API error fetching uplink status for %s: %s", device_serial, e)
            self._attr_native_value = STATE_ERROR_VALUE
            self._attr_extra_state_attributes["error_message"] = str(e)
        except Exception as e:
            # Catch any other unexpected errors.
            _LOGGER.exception(
                "Unexpected error fetching uplink status for %s: %s", device_serial, e
            )
            self._attr_native_value = STATE_ERROR_VALUE
            self._attr_extra_state_attributes["error_message"] = str(e)
            # Re-raising the original exception might be too disruptive if it's transient.
            # For a sensor, often better to report an error state.
            # However, if this indicates a persistent issue like auth, it might need specific handling.
            # Original code re-raised `e` for "Exception as e", but not for MerakiApiError.
            # For consistency, let's not re-raise here to allow HA to manage sensor availability.

    @property
    def native_value(self) -> Optional[str]:
        """Return the current status of the primary uplink interface."""
        return self._attr_native_value

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity-specific state attributes, including all uplink details."""
        return self._attr_extra_state_attributes.copy()
