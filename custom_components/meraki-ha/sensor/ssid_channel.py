"""Sensor entity representing the wireless channel of a Meraki SSID.

This module defines the `MerakiSSIDChannelSensor` class, a Home Assistant
sensor entity that displays the current wireless channel being used by a
specific Meraki SSID.
"""

import logging
from typing import Any, Dict, Union # Optional removed

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback  # For coordinator updates

# from homeassistant.helpers.update_coordinator import CoordinatorEntity #
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

# Use SSIDDeviceCoordinator for these sensors
from ..coordinators.ssid_device_coordinator import SSIDDeviceCoordinator
from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDChannelSensor(CoordinatorEntity[SSIDDeviceCoordinator], SensorEntity):
    """Represents a Meraki SSID Channel sensor.

    This sensor entity displays the wireless channel currently utilized by
    a specific SSID. It is linked to an SSID HA device.
    """

    _attr_icon = "mdi:radio-tower"

    def __init__(
        self,
        coordinator: SSIDDeviceCoordinator,
        ssid_data: Dict[str, Any],  # Specific SSID data for this sensor
    ) -> None:
        """Initialize the Meraki SSID Channel sensor.

        Args:
            coordinator: The SSIDDeviceCoordinator.
            ssid_data: Dictionary containing information about the SSID.
                       Expected: 'unique_id', 'name', and potentially 'channel'.
        """
        super().__init__(coordinator)
        self._ssid_data = ssid_data

        ssid_name = self._ssid_data.get("name", "Unknown SSID")
        self._attr_name = f"{ssid_name} Channel"
        self._attr_unique_id = f"{self._ssid_data['unique_id']}_channel"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._ssid_data["unique_id"])},
            name=ssid_name,
            model="Wireless SSID",
            manufacturer="Cisco Meraki",
        )

        # Set initial state
        self._update_sensor_state()
        _LOGGER.debug(
            "MerakiSSIDChannelSensor Initialized: Name: %s, Unique ID: %s, SSID Data: %s",
            self._attr_name,
            self._attr_unique_id,
            {
                key: ssid_data.get(key) for key in ["name", "unique_id", "channel"]
            },  # Log subset
        )

    def _update_sensor_state(self) -> None:
        """Update the sensor's state based on coordinator data for this SSID."""
        current_ssid_data = self.coordinator.data.get(self._ssid_data["unique_id"])

        if current_ssid_data:
            self._ssid_data = current_ssid_data  # Update internal data
            # The 'channel' field is not standard in Meraki's getNetworkWirelessSsid output.
            # This field would need to be populated by SSIDDeviceCoordinator from another source
            # (e.g., AP radio settings or specific client details if this sensor means client's channel).
            # For now, we expect it might be in self._ssid_data if enriched by the coordinator.
            channel_value: Union[str, int, None] = self._ssid_data.get("channel")

            if channel_value is not None:
                self._attr_native_value = str(channel_value)
                if isinstance(channel_value, (int, float)):
                    self._attr_state_class = SensorStateClass.MEASUREMENT
                else:
                    # If channel can be "Auto" or include text like "(20MHz)"
                    self._attr_state_class = None
            else:
                _LOGGER.debug(
                    "SSID '%s' (ID: %s) has no 'channel' information. Setting to None.",
                    self._ssid_data.get("name"),
                    self._ssid_data.get("unique_id"),
                )
                self._attr_native_value = None
                self._attr_state_class = None
        else:
            _LOGGER.warning(
                "SSID data for ID '%s' not found in coordinator. Channel sensor state set to None.",
                self._ssid_data.get("unique_id"),
            )
            self._attr_native_value = None
            self._attr_state_class = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_sensor_state()
        self.async_write_ha_state()
