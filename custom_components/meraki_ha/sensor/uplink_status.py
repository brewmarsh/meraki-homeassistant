"""Sensor entity for representing the uplink status of a Meraki MX appliance.

This module defines the `MerakiUplinkStatusSensor` class, a Home Assistant
sensor entity that displays the status of the primary uplink for a Meraki
MX security appliance.
"""
import logging
from typing import Any, Dict, Optional, List  # Added Optional, List

# SensorStateClass not needed if state is string
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback  # For coordinator updates
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
from ..coordinators import MerakiDataUpdateCoordinator
from ..const import DOMAIN  # For device_info identifiers
# Assuming this function is correctly defined in the meraki_api package
# from ..meraki_api.appliance import get_meraki_device_appliance_uplinks
# Placeholder for the function if not available for type checking


async def get_meraki_device_appliance_uplinks(  # Function name was different in appliance.py
    # org_id seems unused by actual API endpoint for device uplinks
    api_key: str, org_id: str, serial: str
) -> Optional[List[Dict[str, Any]]]:  # API returns a list of uplinks
    """Placeholder: Fetches Meraki device appliance uplink settings/status."""
    _LOGGER.warning(
        "Using placeholder for get_meraki_device_appliance_uplinks for serial %s.",
        serial)
    # Example successful response structure (simplified list of uplinks)
    # return [{"interface": "wan1", "status": "active", "ip": "1.2.3.4", ...}, {"interface": "wan2", ...}]
    # Example error or no data:
    return None

_LOGGER = logging.getLogger(__name__)

# Constants for sensor state if data is unavailable or an error occurs
STATE_UNAVAILABLE_UPLINK = "Unavailable"
STATE_ERROR_UPLINK = "Error"
STATE_UNKNOWN_UPLINK = "Unknown"


class MerakiUplinkStatusSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki MX Appliance Uplink Status sensor.

    This sensor displays the status of the primary uplink of a Meraki MX device.
    Additional uplink details are exposed as state attributes.

    Note: The original implementation had its own `async_update` method.
    This revision assumes it will become a true `CoordinatorEntity`, relying on
    the coordinator to provide uplink data for the specific device.

    Attributes:
        _attr_name: The name of the sensor.
        _attr_unique_id: The unique ID of the sensor.
        _attr_icon: The icon for the sensor.
        _device_info_data: Raw dictionary data for the associated Meraki MX appliance.
    """

    _attr_icon = "mdi:upload-network-outline"  # Static icon

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any],  # Data for the Meraki MX appliance
    ) -> None:
        """Initialize the Meraki MX Appliance Uplink Status sensor.

        Args:
            coordinator: The data update coordinator.
            device_data: A dictionary containing information about the Meraki MX
                         appliance (e.g., name, serial, model).
        """
        super().__init__(coordinator)
        self._device_info_data: Dict[str, Any] = device_data
        device_name = self._device_info_data.get(
            "name", self._device_info_data.get(
                "serial", "Unknown Device"))
        device_serial = self._device_info_data.get("serial", "")

        self._attr_name = f"{device_name} Uplink Status"
        self._attr_unique_id = f"{device_serial}_uplink_status"

        # Initialize base attributes that won't change per update
        self._base_attributes: Dict[str, Any] = {
            "model": self._device_info_data.get("model"),
            "serial_number": device_serial,
            "firmware_version": self._device_info_data.get("firmware"),
        }
        self._attr_extra_state_attributes = self._base_attributes.copy()  # Initial attributes

        # Set initial state
        self._update_sensor_state()
        _LOGGER.debug(
            "Meraki Uplink Status Sensor Initialized: %s", self._attr_name
        )

    def _update_sensor_state(self) -> None:
        """Update sensor state and attributes from coordinator data.

        Assumes coordinator data structure:
        `coordinator.data['devices_uplinks']['SERIAL'] = List[Dict[str, Any]]` (list of uplink details)
        The state of this sensor will be the status of the first uplink in the list.
        All uplink details will be in `extra_state_attributes`.
        """
        device_serial = self._device_info_data.get("serial")
        uplinks_data: Optional[List[Dict[str, Any]]] = None

        if self.coordinator.data and "devices_uplinks" in self.coordinator.data:
            device_uplinks_all = self.coordinator.data["devices_uplinks"]
            if isinstance(device_uplinks_all, dict):
                uplinks_data = device_uplinks_all.get(device_serial)

        # Reset attributes to base and then update with new data
        current_attributes = self._base_attributes.copy()

        if uplinks_data and isinstance(uplinks_data, list) and uplinks_data:
            # Assuming the first uplink in the list is the primary or most
            # relevant one for the main state
            primary_uplink_status = uplinks_data[0].get(
                "status", STATE_UNKNOWN_UPLINK)
            self._attr_native_value = str(primary_uplink_status).capitalize()
            # Add all uplink details to extra_state_attributes
            # To avoid overly large state objects, decide what's most relevant from uplinks_data.
            # For example, just the list of uplinks, or specific fields from
            # each.
            # Store the full list
            current_attributes["uplinks_details"] = uplinks_data
            # Or, to be more selective:
            # current_attributes["active_uplink_interface"] = uplinks_data[0].get("interface")
            # current_attributes["active_uplink_ip"] = uplinks_data[0].get("ip")
        elif uplinks_data == []:  # Explicitly empty list means no uplinks reported
            _LOGGER.info(
                "No uplink data reported for device '%s'.", device_serial
            )
            # Or "No Uplinks"
            self._attr_native_value = STATE_UNAVAILABLE_UPLINK
            current_attributes["uplinks_details"] = []
        else:
            _LOGGER.warning(
                (
                    "Uplink data for device '%s' (Serial: %s) not found or in "
                    "unexpected format in coordinator data. Setting state to unavailable."
                ),
                self._device_info_data.get("name", "N/A"),
                device_serial,
            )
            self._attr_native_value = STATE_UNAVAILABLE_UPLINK
            # Indicate data was not available
            current_attributes["uplinks_details"] = None

        self._attr_extra_state_attributes = {
            k: v for k, v in current_attributes.items() if v is not None
        }

    # Original async_update logic if this sensor were to fetch its own data:
    # async def async_update(self) -> None:
    #     """Update the sensor state by fetching data from the API."""
    #     _LOGGER.debug("Updating uplink status sensor for %s", self._attr_name)
    #     device_serial = self._device_info_data.get("serial")
    #     if not device_serial:
    #         _LOGGER.error("Cannot update uplink status sensor for %s: missing serial.", self.name)
    #         self._attr_native_value = STATE_ERROR_UPLINK
    #         self._attr_extra_state_attributes.update({"uplinks_details": None})
    #         return
    #
    #     current_attributes = self._base_attributes.copy()
    #     try:
    #         # The API function get_meraki_device_appliance_uplinks was used.
    #         # In appliance.py, it was renamed to async_get_device_appliance_uplinks_settings
    #         # and it returns a Dict, not List. The API endpoint /devices/{serial}/appliance/uplinks
    #         # (without /settings) returns a list of current uplink statuses. Let's assume that's intended.
    #         # Placeholder needs to reflect this:
    #         # async def get_device_appliance_uplinks(api_key: str, serial: str) -> Optional[List[Dict[str, Any]]]:
    #
    #         uplinks_status_list: Optional[List[Dict[str, Any]]] = await get_meraki_device_appliance_uplinks(
    #             self.coordinator.api_key, # Assuming api_key is an attribute of coordinator
    #             # self.coordinator.org_id, # org_id might not be needed for device specific uplink status
    #             device_serial,
    #         )
    #
    #         if uplinks_status_list: # API returns a list of uplink interface statuses
    #             # For simplicity, using the status of the first uplink as the sensor's main state.
    #             # More complex logic could be to find the "active" one.
    #             self._attr_native_value = str(uplinks_status_list[0].get("status", STATE_UNKNOWN_UPLINK)).capitalize()
    #             current_attributes["uplinks_details"] = uplinks_status_list
    #         elif uplinks_status_list == []:
    #             self._attr_native_value = "No Uplinks" # Or STATE_UNAVAILABLE_UPLINK
    #             current_attributes["uplinks_details"] = []
    #         else: # None was returned by API call
    #             self._attr_native_value = STATE_UNAVAILABLE_UPLINK
    #             current_attributes["uplinks_details"] = None
    #
    #     except MerakiApiException as e: # Catch specific API errors
    #         _LOGGER.error("API error fetching uplink status for %s: %s", self.name, e)
    #         self._attr_native_value = STATE_ERROR_UPLINK
    #         current_attributes["uplinks_details"] = "API Error"
    #     except Exception as e: # Catch any other unexpected errors
    #         _LOGGER.exception("Unexpected error fetching uplink status for %s: %s", self.name, e)
    #         self._attr_native_value = STATE_ERROR_UPLINK
    #         current_attributes["uplinks_details"] = "Unexpected Error"
    #
    #     self._attr_extra_state_attributes = {k:v for k,v in current_attributes.items() if v is not None}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        This method is called by the CoordinatorEntity base class when new data
        is available from the coordinator. It updates the sensor's state.
        """
        self._update_sensor_state()
        self.async_write_ha_state()

    # native_value and extra_state_attributes are now managed by _attr_ fields

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for linking this entity to the device registry.

        This links the sensor to the physical Meraki MX appliance it represents.
        """
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_info_data["serial"])},
            name=str(self._device_info_data.get("name", self._device_info_data["serial"])),
            manufacturer="Cisco Meraki",
            model=str(self._device_info_data.get("model", "Unknown")),
            sw_version=str(self._device_info_data.get("firmware", "")),
        )
