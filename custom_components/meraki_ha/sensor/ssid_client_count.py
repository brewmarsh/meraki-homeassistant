"""Sensor entity representing the client count for a Meraki SSID.

This module defines the `MerakiSSIDClientCountSensor` class, a Home Assistant
sensor entity that displays the number of clients currently connected to a
specific Meraki SSID.
"""

import logging
from typing import Any, Dict, Optional  # Added Optional, Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback  # For coordinator updates

# from homeassistant.helpers.update_coordinator import CoordinatorEntity #
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

# Use SSIDDeviceCoordinator for these sensors
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDClientCountSensor(CoordinatorEntity[SSIDDeviceCoordinator], SensorEntity):
    """Represents a Meraki SSID Client Count sensor.

    This sensor entity displays the number of clients connected to a specific SSID.
    It is linked to an SSID HA device.
    """

    _attr_icon = "mdi:account-multiple"
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: SSIDDeviceCoordinator,
        ssid_data: Dict[str, Any],  # Specific SSID data for this sensor
    ) -> None:
        """Initialize the Meraki SSID Client Count sensor.

        Args:
            coordinator: The SSIDDeviceCoordinator.
            ssid_data: Dictionary containing information about the SSID.
                       Expected: 'unique_id', 'name', and potentially 'client_count'.
        """
        super().__init__(coordinator)
        self._ssid_data = ssid_data

        ssid_name = self._ssid_data.get("name", "Unknown SSID")
        self._attr_name = f"{ssid_name} Client Count"
        self._attr_unique_id = f"{self._ssid_data['unique_id']}_client_count"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._ssid_data["unique_id"])},
            name=ssid_name,
            model="Wireless SSID",
            manufacturer="Cisco Meraki",
        )
        
        # Set initial state
        self._update_sensor_state()
        _LOGGER.debug(
            "MerakiSSIDClientCountSensor Initialized: Name: %s, Unique ID: %s, SSID Data: %s",
            self._attr_name,
            self._attr_unique_id,
            {key: ssid_data.get(key) for key in ['name', 'unique_id', 'client_count']} # Log subset
        )

    def _update_sensor_state(self) -> None:
        """Update the sensor's state based on coordinator data for this SSID."""
        current_ssid_data = self.coordinator.data.get(self._ssid_data["unique_id"])

        if current_ssid_data:
            self._ssid_data = current_ssid_data # Update internal data
            # The 'client_count' field is not standard in Meraki's getNetworkWirelessSsid output.
            # This field would need to be populated by SSIDDeviceCoordinator.
            client_count: Optional[int] = self._ssid_data.get("client_count")
            
            if isinstance(client_count, int):
                self._attr_native_value = client_count
            else:
                _LOGGER.debug(
                    "SSID '%s' (ID: %s) has no 'client_count' information or it's not an int. Setting to 0.",
                    self._ssid_data.get("name"),
                    self._ssid_data.get("unique_id"),
                )
                self._attr_native_value = 0 
        else:
            _LOGGER.warning(
                "SSID data for ID '%s' not found in coordinator. Client count set to 0.",
                self._ssid_data.get("unique_id"),
            )
            self._attr_native_value = 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_state()
        self.async_write_ha_state()
