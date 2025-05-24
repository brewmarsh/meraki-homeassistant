"""Sensor entity for representing Meraki SSID wireless channel.

This module defines the `MerakiSSIDChannelSensor`, a Home Assistant sensor
that displays the wireless channel an SSID is currently operating on for a
specific device.
"""

import logging
from typing import Any, Dict, Optional # Added for type hinting

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback # For _handle_coordinator_update

# Assuming MerakiEntity is a base class defined in the integration
# and MerakiDataUpdateCoordinator is the coordinator type.
from ..entity import MerakiEntity
from ..coordinator import MerakiDataUpdateCoordinator


_LOGGER = logging.getLogger(__name__)


class MerakiSSIDChannelSensor(MerakiEntity, SensorEntity):
    """Represents a sensor for the wireless channel of a Meraki SSID on a device.

    This sensor displays the `channel` attribute associated with an SSID,
    as provided by the `MerakiDataUpdateCoordinator`. The channel information
    is typically specific to the device broadcasting the SSID, especially in
    multi-AP environments.

    Inherits from `MerakiEntity` which handles coordinator and device/SSID
    information linking.

    Attributes:
        _attr_name (str): The friendly name of the sensor.
        _attr_unique_id (str): The unique ID for this sensor entity.
        _attr_native_value (Optional[str]): The current wireless channel as a string,
            or None if not available.
        _attr_icon (str): The icon for the sensor.
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info: Dict[str, Any],
        ssid_info: Dict[str, Any],
    ) -> None:
        """Initializes the Meraki SSID Channel sensor.

        Args:
            coordinator (MerakiDataUpdateCoordinator): The data update coordinator.
            device_info (Dict[str, Any]): Dictionary containing information about the
                parent Meraki device.
            ssid_info (Dict[str, Any]): Dictionary containing information about the
                specific SSID this sensor represents.
        """
        super().__init__(coordinator, device_info, ssid_info)

        # Construct the sensor's name and unique ID.
        # _device_name, _ssid_name, _device_serial, _ssid_number are expected
        # to be set by the MerakiEntity base class.
        self._attr_name = f"{self._device_name} {self._ssid_name} Channel"
        self._attr_unique_id = f"{self._device_serial}_{self._ssid_number}_channel"
        self._attr_icon = "mdi:radio-tower" # Icon suggesting radio transmission/channel.

        # Set initial state based on current SSID info.
        self._attr_native_value = self._determine_state()
        _LOGGER.debug(
            "Meraki SSID Channel Sensor initialized: %s (Unique ID: %s)",
            self._attr_name,
            self._attr_unique_id,
        )

    def _get_current_ssid_specific_data_on_device(self) -> Optional[Dict[str, Any]]:
        """Safely retrieves the current, device-specific data for this sensor's SSID.

        This method needs to find the SSID's data that is specific to *this* device,
        as channel information can vary per AP. The structure of coordinator data
        will determine how this is best achieved.

        Assuming `coordinator.data['devices']` contains devices, and each device
        might have an `ssids` list with device-specific SSID details.

        Returns:
            Optional[Dict[str, Any]]: The SSID's device-specific data dictionary
                if found, else None.
        """
        if self.coordinator.data and "devices" in self.coordinator.data:
            for device_data in self.coordinator.data["devices"]:
                if isinstance(device_data, dict) and device_data.get("serial") == self._device_serial:
                    # Found the parent device, now look for this specific SSID within it.
                    # This assumes the coordinator populates device_data with a list of its SSIDs,
                    # including their device-specific attributes like channel.
                    device_ssids = device_data.get("ssids", []) # Or the actual key for SSIDs on a device
                    if isinstance(device_ssids, list):
                        for ssid_on_device in device_ssids:
                            if (isinstance(ssid_on_device, dict) and
                                ssid_on_device.get("number") == self._ssid_number):
                                return ssid_on_device
        _LOGGER.warning(
            "Device-specific SSID data for device %s, SSID number %s not found in coordinator.",
            self._device_serial, self._ssid_number
        )
        return None

    def _determine_state(self) -> Optional[str]:
        """Determines the sensor's state based on the SSID's 'channel' attribute."""
        # The `self._ssid` from `MerakiEntity` likely holds the general SSID configuration.
        # Channel can be device-specific, so we might need to look up this SSID's
        # current operational details on *this* specific device from the coordinator.
        ssid_device_data = self._get_current_ssid_specific_data_on_device()

        if ssid_device_data:
            channel = ssid_device_data.get("channel")
            if channel is not None:
                return str(channel) # Ensure channel is a string for state.
            else:
                _LOGGER.debug(
                    "Channel not available for SSID %s on device %s.",
                    self._ssid_name, self._device_name
                )
                return None # Or "Unknown" / "Unavailable"
        else:
            # Fallback to general SSID info if device-specific isn't found,
            # though 'channel' is usually very device-specific.
            # This part might be less reliable for channel.
            channel = self._ssid.get("channel") # self._ssid is from MerakiEntity
            if channel is not None:
                _LOGGER.debug("Using general channel info for SSID %s (may not be device-specific): %s", self._ssid_name, channel)
                return str(channel)
            _LOGGER.warning(
                "Could not determine channel for SSID %s on device %s.",
                self._ssid_name, self._device_name
            )
            return None # Or "Unknown" / "Unavailable"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handles data updates from the coordinator."""
        new_state = self._determine_state()
        if self._attr_native_value != new_state:
            _LOGGER.debug(
                "Updating SSID channel for %s from %s to %s",
                self.name,
                self._attr_native_value,
                new_state,
            )
            self._attr_native_value = new_state
            self.async_write_ha_state()
        else:
            _LOGGER.debug("No change in SSID channel for %s. Current value: %s", self.name, new_state)

    @property
    def name(self) -> str:
        """Return the user-friendly name of the sensor."""
        return self._attr_name

    @property
    def unique_id(self) -> str:
        """Return the unique ID of this sensor entity."""
        return self._attr_unique_id

    @property
    def native_value(self) -> Optional[str]:
        """Return the current wireless channel of the SSID on this device."""
        return self._attr_native_value

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend for this sensor."""
        return self._attr_icon
