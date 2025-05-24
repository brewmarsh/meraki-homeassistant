"""Sensor entity for displaying the status (product type) of a Meraki device.

This module defines the `MerakiDeviceStatusSensor`, a Home Assistant sensor
entity that shows the type of a Meraki device (e.g., "Wireless", "Appliance").
The icon also changes based on the device model.
"""

import logging
from typing import Any, Dict, Optional # Added Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback # For _handle_coordinator_update

# Assuming MerakiDataUpdateCoordinator is the type of coordinator used.
# from ..coordinator import MerakiDataUpdateCoordinator # If specific coordinator type is needed

_LOGGER = logging.getLogger(__name__)


class MerakiDeviceStatusSensor(CoordinatorEntity, SensorEntity):
    """Represents a sensor for the status (product type) of a Meraki device.

    This sensor displays the `productType` of the Meraki device as its state.
    The icon is determined by the device model prefix (e.g., MR, MX, MS).
    It relies on data from the `MerakiDataUpdateCoordinator`.

    Attributes:
        _device_info (Dict[str, Any]): Raw device information from the Meraki API.
        _attr_name (str): The friendly name of the sensor.
        _attr_unique_id (str): The unique ID for this sensor entity.
        _attr_extra_state_attributes (Dict[str, Any]): Additional state attributes.
        _attr_native_value (str): The current state (product type) of the sensor.
    """

    def __init__(
        self, coordinator: CoordinatorEntity, device_info: Dict[str, Any]
    ) -> None:
        """Initializes the Meraki Device Status sensor.

        Args:
            coordinator (CoordinatorEntity): The data update coordinator instance
                from which to fetch device data.
            device_info (Dict[str, Any]): A dictionary containing the Meraki
                device's information (name, serial, model, productType, etc.).
        """
        super().__init__(coordinator)  # Initialize CoordinatorEntity.
        self._device_info = device_info  # Store the raw device data.
        device_name = device_info.get(
            "name", device_info.get("serial", "Unknown Device")
        )
        device_serial = device_info.get("serial", "unknown_serial")

        # Set Home Assistant entity attributes.
        self._attr_name = f"{device_name} Status"
        self._attr_unique_id = f"{device_serial}_status"

        # Populate extra state attributes with device details.
        self._attr_extra_state_attributes = {
            "model": device_info.get("model"),
            "serial_number": device_serial,
            "firmware_version": device_info.get("firmware"),
            "mac_address": device_info.get("mac"),
            "lan_ip": device_info.get("lanIp"),
            "network_id": device_info.get("networkId"),
        }
        # The native_value and icon are determined by properties based on current device data.
        # Initialize native_value here based on initial data.
        self._attr_native_value = self._determine_native_value()
        _LOGGER.debug(
            "Meraki Device Status Sensor initialized for %s (Serial: %s)",
            self._attr_name,
            device_serial,
        )

    def _get_current_device_data(self) -> Optional[Dict[str, Any]]:
        """Safely retrieves the current data for this sensor's device from the coordinator.

        Returns:
            Optional[Dict[str, Any]]: The device data dictionary if found, else None.
        """
        device_serial = self._device_info.get("serial")
        if self.coordinator.data and "devices" in self.coordinator.data:
            for device_data in self.coordinator.data["devices"]:
                if isinstance(device_data, dict) and device_data.get("serial") == device_serial:
                    return device_data
        _LOGGER.warning("Device data for serial %s not found in coordinator.", device_serial)
        return None

    def _determine_native_value(self) -> str:
        """Determines the sensor's state based on the device's productType."""
        current_device_data = self._get_current_device_data()
        if not current_device_data:
            return "Unknown" # Default if device data is missing

        product_type = current_device_data.get("productType", "unknown").lower()
        # More descriptive status based on productType.
        if product_type == "appliance":
            return "Appliance"
        elif product_type == "wireless":
            return "Wireless AP"
        elif product_type == "switch":
            return "Switch"
        elif product_type == "camera":
            return "Camera"
        elif product_type == "sensor":
            return "Sensor"
        else:
            _LOGGER.info(
                "Unknown productType '%s' for device %s. Defaulting status to 'Unknown'.",
                current_device_data.get("productType"),
                current_device_data.get("serial")
            )
            return "Unknown"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handles data updates from the coordinator.

        This method is called by the `CoordinatorEntity` base class when new data
        is available. It updates the sensor's `native_value` and attributes
        if the underlying device data has changed.
        """
        new_value = self._determine_native_value()
        # Also update extra attributes if they can change, e.g., firmware.
        current_device_data = self._get_current_device_data()
        if current_device_data:
            self._attr_extra_state_attributes["firmware_version"] = current_device_data.get("firmware")
            # Potentially update other attributes like LAN IP if they are dynamic.

        if self._attr_native_value != new_value:
            _LOGGER.debug("Updating status for %s from %s to %s", self.name, self._attr_native_value, new_value)
            self._attr_native_value = new_value
        self.async_write_ha_state() # Always write state to update attributes if they changed

    @property
    def native_value(self) -> str:
        """Return the current state (product type) of the Meraki device."""
        return self._attr_native_value

    @property
    def icon(self) -> str:
        """Return an icon that represents the Meraki device model.

        The icon changes dynamically based on the device model prefix.
        """
        current_device_data = self._get_current_device_data()
        model = current_device_data.get("model", "") if current_device_data else ""

        if model.startswith("MR") or model.startswith("GR"): # Wireless APs
            return "mdi:access-point"
        elif model.startswith("MX"): # Security Appliances
            return "mdi:router-wireless" # Using router-wireless for MX
        elif model.startswith("MS"): # Switches
            return "mdi:switch"
        elif model.startswith("MV"): # Cameras
            return "mdi:camera-outline" # Using camera-outline
        elif model.startswith("MT"): # Sensors
            return "mdi:leak" # Example for sensors, could be more specific
        else:
            return "mdi:help-rhombus-outline"  # A more generic 'unknown' or default Meraki icon

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity-specific state attributes for more details."""
        return self._attr_extra_state_attributes.copy()
