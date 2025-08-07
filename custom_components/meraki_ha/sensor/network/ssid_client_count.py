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
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...const import DOMAIN, CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
from ...helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDClientCountSensor(
    CoordinatorEntity[MerakiDataCoordinator], SensorEntity
):
    """Represents a Meraki SSID Client Count sensor.

    This sensor entity displays the number of clients connected to a specific SSID.
    The client count is provided by the `SSIDDeviceCoordinator`, which calculates
    it based on network-wide client data filtered by SSID name.
    This sensor is linked to an HA device representing the specific SSID.
    """

    _attr_icon = "mdi:account-multiple"
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        network_id: str,
        ssid_data: Dict[str, Any],  # Specific SSID data for this sensor
    ) -> None:
        """Initialize the Meraki SSID Client Count sensor.

        Args:
          coordinator: The `SSIDDeviceCoordinator` instance that provides updates
                 for this SSID's data, including the client count.
          network_id: The ID of the network this SSID belongs to.
          ssid_data: A dictionary containing initial information about the SSID,
                including 'number' (for identifying the SSID in coordinator data),
                'name' (for display purposes), and potentially 'client_count'
                as calculated by the coordinator.
        """
        super().__init__(coordinator)
        self._network_id = network_id
        self._ssid_data = ssid_data

        ssid_name = self._ssid_data.get("name", "Unknown SSID")
        ssid_number = self._ssid_data.get("number")
        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            ssid_name, "Client Count"
        )
        self._attr_unique_id = f"{self._network_id}_{ssid_number}_client_count"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{self._network_id}_{ssid_number}")},
            name=ssid_name,
            model="Wireless SSID",
            manufacturer="Cisco Meraki",
        )

        # Set initial state
        self._update_sensor_state()

    def _update_sensor_state(self) -> None:
        """Update the sensor's state using the latest data from the coordinator.

        This method retrieves the most recent data for this specific SSID from the
        `SSIDDeviceCoordinator`. It then updates the sensor's native value with
        the `client_count` found in that data. If `client_count` is missing or
        not an integer, the sensor's value defaults to 0.
        """
        current_ssid_data = None
        if self.coordinator.data and "ssids" in self.coordinator.data:
            for ssid in self.coordinator.data["ssids"]:
                if ssid.get("networkId") == self._network_id and ssid.get("number") == self._ssid_data.get("number"):
                    current_ssid_data = ssid
                    break

        if current_ssid_data:
            self._ssid_data = current_ssid_data  # Update internal data
            # The 'client_count' field is populated by the SSIDDeviceCoordinator.
            client_count: Optional[int] = current_ssid_data.get("client_count")

            if isinstance(client_count, int):
                self._attr_native_value = client_count
            else:
                self._attr_native_value = 0
        else:
            _LOGGER.warning(  # Keep warning for missing data
                "SSID data for ID '%s' not found in coordinator. Client count set to 0.",
                self._ssid_data.get("number"),
            )
            self._attr_native_value = 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_state()
        self.async_write_ha_state()
