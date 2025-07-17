"""Sensor entity representing the availability (enabled/disabled) of a Meraki SSID.

This module defines the `MerakiSSIDAvailabilitySensor` class, a Home Assistant
sensor entity that indicates whether a specific Meraki SSID is currently enabled
or disabled.
"""

import logging
from typing import Any, Dict, Optional  # Added Optional, Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_OFF, STATE_ON  # Standard HA states
from homeassistant.core import callback  # For coordinator updates

# from homeassistant.helpers.update_coordinator import CoordinatorEntity #
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

# Use SSIDDeviceCoordinator for these sensors
from custom_components.meraki_hacoordinators.ssid_device_coordinator import SSIDDeviceCoordinator
from custom_components.meraki_haconst import DOMAIN


_LOGGER = logging.getLogger(__name__)


class MerakiSSIDAvailabilitySensor(
    CoordinatorEntity[SSIDDeviceCoordinator], SensorEntity
):
    """Represents a Meraki SSID Availability sensor.

    This sensor entity reflects the 'enabled' state of a specific SSID.
    It is linked to an SSID HA device.
    """

    def __init__(
        self,
        coordinator: SSIDDeviceCoordinator,
        ssid_data: Dict[str, Any],  # Specific SSID data for this sensor
    ) -> None:
        """Initialize the Meraki SSID Availability sensor.

        Args:
            coordinator: The SSIDDeviceCoordinator.
            ssid_data: Dictionary containing information about the SSID.
                       Expected to have 'unique_id', 'name', and 'enabled'.
        """
        super().__init__(coordinator)
        self._ssid_data = (
            ssid_data  # Store the initial data for unique_id and name setup
        )

        ssid_name = self._ssid_data.get("name", "Unknown SSID")
        self._attr_name = f"{ssid_name} Availability"
        self._attr_unique_id = f"{self._ssid_data['unique_id']}_availability"  # Use unique_id from ssid_data

        # Link to the SSID HA Device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._ssid_data["unique_id"])},
            name=ssid_name,  # Name of the parent SSID HA device
            model="Wireless SSID",  # Model of the parent SSID HA device
            manufacturer="Cisco Meraki",
            # via_device can link to the integration config entry if desired,
            # but identifiers link is primary for entity-to-device.
            # The SSID HA device itself is linked to config_entry.
        )

        # Set initial state
        self._update_sensor_state()
        # _LOGGER.debug(
        #     "MerakiSSIDAvailabilitySensor Initialized: Name: %s, Unique ID: %s, SSID Data: %s",
        #     self._attr_name,
        #     self._attr_unique_id,
        #     {
        #         key: ssid_data.get(key) for key in ["name", "unique_id", "enabled"]
        #     },
        # ) # Removed

    def _update_sensor_state(self) -> None:
        """Update the sensor's state based on coordinator data for this SSID."""
        # Get the latest data for this specific SSID from the coordinator
        # self.coordinator.data is a dict: {unique_ssid_id: ssid_data_dict}
        current_ssid_data = self.coordinator.data.get(self._ssid_data["unique_id"])

        if current_ssid_data:
            self._ssid_data = current_ssid_data  # Update internal data
            is_enabled: Optional[bool] = self._ssid_data.get("enabled")
            if isinstance(is_enabled, bool):
                self._attr_native_value = STATE_ON if is_enabled else STATE_OFF
            else:
                _LOGGER.warning(
                    "SSID '%s' (ID: %s) has no 'enabled' status or it's not boolean. Setting to OFF.",
                    self._ssid_data.get("name"),
                    self._ssid_data.get("unique_id"),
                )
                self._attr_native_value = STATE_OFF
        else:
            _LOGGER.warning(
                "SSID data for ID '%s' not found in coordinator. Setting availability to OFF.",
                self._ssid_data.get("unique_id"),
            )
            self._attr_native_value = STATE_OFF

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_state()
        self.async_write_ha_state()

    @property
    def icon(self) -> str:
        """Return the icon of the sensor based on its state."""
        return "mdi:wifi" if self.native_value == STATE_ON else "mdi:wifi-off"
