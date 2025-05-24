"""Sensor entity for monitoring connected clients on a Meraki wireless device.

This module defines the `MerakiConnectedClientsSensor`, a Home Assistant sensor
entity that displays the number of clients currently connected to a specific
Meraki wireless access point (MR or GR series).
"""

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import callback


_LOGGER = logging.getLogger(__name__)


class MerakiConnectedClientsSensor(CoordinatorEntity, SensorEntity):
    """Represents a sensor for the number of clients connected to a Meraki device.

    This sensor entity pulls data from the `MerakiDataUpdateCoordinator` to display
    the count of clients connected to a specific Meraki wireless device (e.g., an MR
    or GR access point).

    Attributes:
        _device (Dict[str, Any]): The raw device information dictionary from the
            Meraki API, used to identify and characterize this sensor's device.
        _attr_name (str): The friendly name of the sensor in Home Assistant.
        _attr_unique_id (str): The unique ID for this sensor entity.
        _attr_icon (str): The icon to display for this sensor in the frontend.
        _attr_extra_state_attributes (Dict[str, Any]): Additional state attributes
            for the sensor, providing more context about the device.
        _attr_native_value (Optional[int]): The current value of the sensor (client count).
        _attr_native_unit_of_measurement (str): The unit of measurement ("clients").
        _attr_state_class (str): The state class of the sensor ("measurement").
    """

    def __init__(
        self, coordinator: CoordinatorEntity, device: Dict[str, Any]
    ) -> None:
        """Initializes the Meraki Connected Clients sensor.

        Args:
            coordinator (CoordinatorEntity): The data update coordinator instance
                from which to fetch device data. This is typically an instance of
                `MerakiDataUpdateCoordinator`.
            device (Dict[str, Any]): A dictionary containing the Meraki device's
                information, such as its name, serial number, model, etc. This
                data is used to configure the sensor's identity and attributes.
        """
        super().__init__(coordinator)  # Initialize the CoordinatorEntity base class.
        self._device = device  # Store the raw device data.
        device_name = device.get("name", device.get("serial", "Unknown Device"))
        device_serial = device.get("serial", "unknown_serial")

        # Set Home Assistant entity attributes.
        self._attr_name = f"{device_name} Connected Clients"
        self._attr_unique_id = f"{device_serial}_connected_clients"
        self._attr_icon = "mdi:account-network"  # Icon representing network clients.

        # Populate extra state attributes with device details.
        self._attr_extra_state_attributes = {
            "model": device.get("model"),
            "serial_number": device_serial,
            "firmware_version": device.get("firmware"),
            # Potentially add LAN IP, MAC address, etc., if available and useful.
            "lan_ip": device.get("lanIp"),
            "mac_address": device.get("mac"),
        }
        _LOGGER.debug(
            "Meraki Connected Clients Sensor initialized for %s (Serial: %s)",
            self._attr_name,
            device_serial,
        )

        # Set sensor-specific properties.
        # The initial value is fetched via _get_client_count.
        self._attr_native_value = self._get_client_count()
        self._attr_native_unit_of_measurement = "clients"
        self._attr_state_class = "measurement"  # Indicates the sensor value is a numeric measurement.

    def _get_client_count(self) -> Optional[int]:
        """Retrieves the connected client count for this sensor's device from coordinator data.

        This method searches the coordinator's data for the device associated with
        this sensor (by serial number) and extracts the 'connected_clients' value,
        which is expected to be populated by the `MerakiDeviceCoordinator`.

        Returns:
            Optional[int]: The number of connected clients. Returns 0 if the device
                data is not found, if 'connected_clients' is missing, or if its
                value is None. Returns None if the coordinator data itself is missing.
        """
        device_serial = self._device.get("serial")
        _LOGGER.debug(
            "Getting client count for device serial: %s", device_serial
        )

        if self.coordinator.data is None or "devices" not in self.coordinator.data:
            _LOGGER.warning(
                "Coordinator data or 'devices' list is not available for %s.",
                device_serial,
            )
            return None # Or 0, depending on desired behavior for unavailable data source

        # Find the specific device's data within the coordinator's list of devices.
        device_data_from_coordinator = next(
            (
                d
                for d in self.coordinator.data.get("devices", [])
                if isinstance(d, dict) and d.get("serial") == device_serial
            ),
            None,  # Default to None if the device is not found.
        )

        if device_data_from_coordinator:
            _LOGGER.debug(
                "Found device data in coordinator for %s: %s",
                device_serial,
                device_data_from_coordinator,
            )
            # The 'connected_clients' key is expected to be populated by MerakiDeviceCoordinator.
            connected_clients_count = device_data_from_coordinator.get(
                "connected_clients"
            )
            if connected_clients_count is not None and isinstance(connected_clients_count, int):
                _LOGGER.debug(
                    "Connected clients for %s: %d",
                    device_serial,
                    connected_clients_count,
                )
                return connected_clients_count
            else:
                _LOGGER.warning(
                    "'connected_clients' count is missing, None, or not an integer for %s. Data: %s. Defaulting to 0.",
                    device_serial,
                    connected_clients_count,
                )
                return 0  # Default to 0 if data is missing or not an int.
        else:
            _LOGGER.warning(
                "Device data not found in coordinator for serial %s. Cannot determine client count. Defaulting to 0.",
                device_serial,
            )
            return 0 # Default to 0 if device data is missing.

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handles data updates from the coordinator.

        This method is called by the `CoordinatorEntity` base class when the
        coordinator signals that new data is available. It updates the sensor's
        `native_value` and schedules a state write.
        """
        new_value = self._get_client_count()
        if self._attr_native_value != new_value:
            _LOGGER.debug(
                "Updating connected clients for %s from %s to %s",
                self.name, # Use self.name for logging consistency
                self._attr_native_value,
                new_value,
            )
            self._attr_native_value = new_value
            self.async_write_ha_state() # Inform Home Assistant of the state change.
        else:
            _LOGGER.debug("No change in connected clients for %s. Current value: %s", self.name, new_value)


    @property
    def native_value(self) -> Optional[int]:
        """Return the current state (number of connected clients) of the sensor."""
        # This property relies on _attr_native_value being kept up-to-date
        # by __init__ and _handle_coordinator_update.
        return self._attr_native_value

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity-specific state attributes.

        Provides additional information about the Meraki device associated with
        this sensor, such as its model, serial number, and firmware version.
        """
        # Returns a copy to prevent modification of the internal attribute dictionary.
        return self._attr_extra_state_attributes.copy()
