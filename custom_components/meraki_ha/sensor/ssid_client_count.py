"""Sensor entity for representing Meraki SSID client count.

This module defines the `MerakiSSIDClientCountSensor`, a Home Assistant sensor
that displays the number of clients connected to a specific SSID on a particular
Meraki device.
"""

import logging
from typing import Any, Dict, Optional # Added for type hinting

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback # For _handle_coordinator_update

# Assuming MerakiEntity is a base class defined in the integration
# and MerakiDataUpdateCoordinator is the coordinator type.
from ..entity import MerakiEntity
from ..coordinator import MerakiDataUpdateCoordinator


_LOGGER = logging.getLogger(__name__)


class MerakiSSIDClientCountSensor(MerakiEntity, SensorEntity):
    """Represents a sensor for the client count of a Meraki SSID on a device.

    This sensor displays the `client_count` attribute associated with an SSID,
    which should represent the number of clients connected to this specific SSID
    on the parent Meraki device. The data is sourced from the
    `MerakiDataUpdateCoordinator`.

    Inherits from `MerakiEntity` which likely handles coordinator and device/SSID
    information linking.

    Attributes:
        _attr_name (str): The friendly name of the sensor.
        _attr_unique_id (str): The unique ID for this sensor entity.
        _attr_native_value (Optional[int]): The current number of clients, or None.
        _attr_icon (str): The icon for the sensor.
        _attr_state_class (SensorStateClass): The state class of the sensor.
        _attr_native_unit_of_measurement (str): The unit of measurement.
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info: Dict[str, Any],
        ssid_info: Dict[str, Any],
    ) -> None:
        """Initializes the Meraki SSID Client Count sensor.

        Args:
            coordinator (MerakiDataUpdateCoordinator): The data update coordinator.
            device_info (Dict[str, Any]): Dictionary containing information about the
                parent Meraki device.
            ssid_info (Dict[str, Any]): Dictionary containing information about the
                specific SSID this sensor represents. It's expected to have a
                'client_count' key.
        """
        super().__init__(coordinator, device_info, ssid_info)

        # Construct the sensor's name and unique ID.
        # _device_name, _ssid_name, _device_serial, _ssid_number are expected
        # to be set by the MerakiEntity base class.
        self._attr_name = f"{self._device_name} {self._ssid_name} Client Count"
        self._attr_unique_id = (
            f"{self._device_serial}_{self._ssid_number}_client_count"
        )
        self._attr_icon = "mdi:account-multiple" # Icon for multiple users/clients.
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "clients"

        # Set initial state based on current SSID info.
        self._attr_native_value = self._determine_state()
        _LOGGER.debug(
            "Meraki SSID Client Count Sensor initialized: %s (Unique ID: %s)",
            self._attr_name,
            self._attr_unique_id,
        )

    def _get_current_ssid_specific_data_on_device(self) -> Optional[Dict[str, Any]]:
        """Safely retrieves the current, device-specific data for this sensor's SSID.

        This method searches for the SSID's data specific to *this* device within
        the coordinator's data. Client count for an SSID is often per-AP.

        Returns:
            Optional[Dict[str, Any]]: The SSID's device-specific data dictionary
                if found, else None.
        """
        if self.coordinator.data and "devices" in self.coordinator.data:
            for device_data in self.coordinator.data["devices"]:
                if isinstance(device_data, dict) and device_data.get("serial") == self._device_serial:
                    # Found the parent device, now look for this specific SSID within it.
                    device_ssids = device_data.get("ssids", [])
                    if isinstance(device_ssids, list):
                        for ssid_on_device in device_ssids:
                            if (isinstance(ssid_on_device, dict) and
                                ssid_on_device.get("number") == self._ssid_number):
                                return ssid_on_device # This dict should contain device-specific client_count
        _LOGGER.warning(
            "Device-specific SSID data for device %s, SSID number %s not found in coordinator for client count.",
            self._device_serial, self._ssid_number
        )
        return None

    def _determine_state(self) -> Optional[int]:
        """Determines the sensor's state from the SSID's 'client_count' attribute."""
        # `self._ssid` from MerakiEntity holds the general SSID configuration.
        # `client_count` for an SSID is specific to the AP broadcasting it.
        ssid_device_data = self._get_current_ssid_specific_data_on_device()

        if ssid_device_data:
            client_count = ssid_device_data.get("client_count")
            if isinstance(client_count, int):
                return client_count
            elif client_count is not None: # Could be a string '0' etc.
                try:
                    return int(client_count)
                except ValueError:
                    _LOGGER.warning(
                        "Client count for SSID %s on device %s is not a valid integer: %s. Defaulting to None.",
                        self._ssid_name, self._device_name, client_count
                    )
                    return None
            else:
                _LOGGER.debug(
                    "Client count not available for SSID %s on device %s. Defaulting to None.",
                    self._ssid_name, self._device_name
                )
                return None # Or 0 if preferred for unavailable count
        else:
            # Fallback if specific data isn't found; this might use a general count if available,
            # but that's less accurate for per-AP client counts.
            client_count = self._ssid.get("client_count") # self._ssid from MerakiEntity
            if isinstance(client_count, int):
                _LOGGER.debug("Using general client_count for SSID %s (may not be device-specific): %s", self._ssid_name, client_count)
                return client_count
            _LOGGER.warning(
                "Could not determine client count for SSID %s on device %s.",
                self._ssid_name, self._device_name
            )
            return None # Or 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handles data updates from the coordinator."""
        new_state = self._determine_state()
        if self._attr_native_value != new_state:
            _LOGGER.debug(
                "Updating SSID client count for %s from %s to %s",
                self.name,
                self._attr_native_value,
                new_state,
            )
            self._attr_native_value = new_state
            self.async_write_ha_state()
        else:
            _LOGGER.debug("No change in SSID client count for %s. Current value: %s", self.name, new_state)


    @property
    def name(self) -> str:
        """Return the user-friendly name of the sensor."""
        return self._attr_name

    @property
    def unique_id(self) -> str:
        """Return the unique ID of this sensor entity."""
        return self._attr_unique_id

    @property
    def native_value(self) -> Optional[int]:
        """Return the current number of clients connected to this SSID on this device."""
        return self._attr_native_value

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend for this sensor."""
        return self._attr_icon
