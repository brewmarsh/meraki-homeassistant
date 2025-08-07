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
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...const import DOMAIN, CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
from ...helpers.entity_helpers import format_entity_name


_LOGGER = logging.getLogger(__name__)


class MerakiSSIDAvailabilitySensor(
    CoordinatorEntity[MerakiDataCoordinator], SensorEntity
):
    """Represents a Meraki SSID Availability sensor.

    This sensor entity reflects the 'enabled' state of a specific SSID.
    It is linked to an SSID HA device.
    """

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        network_id: str,
        ssid_data: Dict[str, Any],  # Specific SSID data for this sensor
    ) -> None:
        """Initialize the Meraki SSID Availability sensor.

        Args:
          coordinator: The SSIDDeviceCoordinator.
          network_id: The ID of the network this SSID belongs to.
          ssid_data: Dictionary containing information about the SSID.
                Expected to have 'number', 'name', and 'enabled'.
        """
        super().__init__(coordinator)
        self._network_id = network_id
        self._ssid_data = (
            ssid_data  # Store the initial data for unique_id and name setup
        )

        ssid_name = self._ssid_data.get("name", "Unknown SSID")
        ssid_number = self._ssid_data.get("number")
        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            ssid_name, "Availability"
        )
        self._attr_unique_id = f"{self._network_id}_{ssid_number}_availability"

        # Link to the SSID HA Device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{self._network_id}_{ssid_number}")},
            name=ssid_name,  # Name of the parent SSID HA device
            model="Wireless SSID",  # Model of the parent SSID HA device
            manufacturer="Cisco Meraki",
        )

        # Set initial state
        self._update_sensor_state()

    def _update_sensor_state(self) -> None:
        """Update the sensor's state based on coordinator data for this SSID."""
        # Get the latest data for this specific SSID from the coordinator
        current_ssid_data = None
        if self.coordinator.data and "ssids" in self.coordinator.data:
            for ssid in self.coordinator.data["ssids"]:
                if ssid.get("networkId") == self._network_id and ssid.get("number") == self._ssid_data.get("number"):
                    current_ssid_data = ssid
                    break

        if current_ssid_data:
            self._ssid_data = current_ssid_data  # Update internal data
            is_enabled: Optional[bool] = self._ssid_data.get("enabled")
            if isinstance(is_enabled, bool):
                self._attr_native_value = STATE_ON if is_enabled else STATE_OFF
            else:
                _LOGGER.warning(
                    "SSID '%s' (ID: %s) has no 'enabled' status or it's not boolean. Setting to OFF.",
                    self._ssid_data.get("name"),
                    self._ssid_data.get("number"),
                )
                self._attr_native_value = STATE_OFF
        else:
            _LOGGER.warning(
                "SSID data for ID '%s' not found in coordinator. Setting availability to OFF.",
                self._ssid_data.get("number"),
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
