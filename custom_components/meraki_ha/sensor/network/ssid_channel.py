"""Sensor entity representing the wireless channel of a Meraki SSID.

This module defines the `MerakiSSIDChannelSensor` class, a Home Assistant
sensor entity that displays the current wireless channel being used by a
specific Meraki SSID.
"""

import logging
from typing import Any, Dict, Union  # Optional removed

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


class MerakiSSIDChannelSensor(
    CoordinatorEntity[MerakiDataCoordinator], SensorEntity
):
    """Represents a Meraki SSID Channel sensor.

    This sensor entity displays the wireless channel currently utilized by
    a specific SSID. It is linked to an SSID HA device.
    """

    _attr_icon = "mdi:radio-tower"

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        network_id: str,
        ssid_data: Dict[str, Any],  # Specific SSID data for this sensor
    ) -> None:
        """Initialize the Meraki SSID Channel sensor.

        Args:
          coordinator: The SSIDDeviceCoordinator.
          network_id: The ID of the network this SSID belongs to.
          ssid_data: Dictionary containing information about the SSID.
                Expected: 'number', 'name', and potentially 'channel'.
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
            ssid_name, "Channel"
        )
        self._attr_unique_id = f"{self._network_id}_{ssid_number}_channel"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{self._network_id}_{ssid_number}")},
            name=ssid_name,
            model="Wireless SSID",
            manufacturer="Cisco Meraki",
        )

        # Set initial state
        self._update_sensor_state()

    def _update_sensor_state(self) -> None:
        """Update the sensor's state based on coordinator data for this SSID."""
        current_ssid_data = None
        if self.coordinator.data and "ssids" in self.coordinator.data:
            for ssid in self.coordinator.data["ssids"]:
                if ssid.get("networkId") == self._network_id and ssid.get("number") == self._ssid_data.get("number"):
                    current_ssid_data = ssid
                    break

        if current_ssid_data:
            self._ssid_data = current_ssid_data  # Update internal data
            # The 'channel' field is not standard in Meraki's getNetworkWirelessSsid output.
            # This field would need to be populated by SSIDDeviceCoordinator from another source
            # (e.g., AP radio settings or specific client details if this sensor means client's channel).
            # For now, we expect it might be in self._ssid_data if enriched by the coordinator.
            channel_value: Union[str, int, None] = current_ssid_data.get("channel")

            if channel_value is not None:
                self._attr_native_value = str(channel_value)
                if isinstance(channel_value, (int, float)):
                    self._attr_state_class = SensorStateClass.MEASUREMENT
                else:
                    # If channel can be "Auto" or include text like "(20MHz)"
                    self._attr_state_class = None
            else:
                self._attr_native_value = "Unknown"
                self._attr_state_class = None
        else:
            _LOGGER.warning(  # Keep warning for missing data
                "SSID data for ID '%s' not found in coordinator. Channel sensor state set to None.",
                self._ssid_data.get("number"),
            )
            self._attr_native_value = "Unknown"
            self._attr_state_class = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_state()
        self.async_write_ha_state()
