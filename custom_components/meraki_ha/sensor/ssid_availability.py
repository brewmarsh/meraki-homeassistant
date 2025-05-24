"""Sensor entity for representing Meraki SSID availability (enabled status).

This module defines the `MerakiSSIDAvailabilitySensor`, a Home Assistant sensor
that indicates whether a specific Meraki SSID is enabled (on) or disabled (off).
"""

import logging
from typing import Any, Dict # Added for type hinting

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.core import callback # For _handle_coordinator_update

# Assuming MerakiEntity is a base class defined in the integration
# and MerakiDataUpdateCoordinator is the coordinator type.
from ..entity import MerakiEntity
from ..coordinator import MerakiDataUpdateCoordinator


_LOGGER = logging.getLogger(__name__)


class MerakiSSIDAvailabilitySensor(MerakiEntity, SensorEntity):
    """Represents a sensor for the availability (enabled state) of a Meraki SSID.

    This sensor derives its state from the 'enabled' attribute of an SSID's
    configuration data, which is obtained from the `MerakiDataUpdateCoordinator`.
    It displays "on" if the SSID is enabled and "off" otherwise.

    Inherits from `MerakiEntity` which likely handles coordinator and device/SSID
    information linking.

    Attributes:
        _attr_name (str): The friendly name of the sensor.
        _attr_unique_id (str): The unique ID for this sensor entity.
        _attr_native_value (str): The current state of the sensor (STATE_ON or STATE_OFF).
        _attr_icon (str): The icon for the sensor.
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info: Dict[str, Any],
        ssid_info: Dict[str, Any],
    ) -> None:
        """Initializes the Meraki SSID Availability sensor.

        Args:
            coordinator (MerakiDataUpdateCoordinator): The data update coordinator.
            device_info (Dict[str, Any]): Dictionary containing information about the
                parent Meraki device.
            ssid_info (Dict[str, Any]): Dictionary containing information about the
                specific SSID this sensor represents.
        """
        # Call the MerakiEntity constructor to set up common properties
        # like coordinator, device_info, and ssid_info.
        super().__init__(coordinator, device_info, ssid_info)

        # Construct the sensor's name and unique ID.
        # _device_name, _ssid_name, _device_serial, _ssid_number are expected
        # to be set by the MerakiEntity base class.
        self._attr_name = f"{self._device_name} {self._ssid_name} Availability"
        self._attr_unique_id = (
            f"{self._device_serial}_{self._ssid_number}_availability"
        )
        self._attr_icon = "mdi:wifi" # Standard Wi-Fi icon.

        # Set initial state based on current SSID info.
        self._attr_native_value = self._determine_state()
        _LOGGER.debug(
            "Meraki SSID Availability Sensor initialized: %s (Unique ID: %s)",
            self._attr_name,
            self._attr_unique_id,
        )

    def _get_current_ssid_data(self) -> Optional[Dict[str, Any]]:
        """Safely retrieves the current data for this sensor's SSID from the coordinator.

        Returns:
            Optional[Dict[str, Any]]: The SSID data dictionary if found, else None.
        """
        if self.coordinator.data and "ssids" in self.coordinator.data:
            for ssid_data in self.coordinator.data["ssids"]:
                if (isinstance(ssid_data, dict) and
                    ssid_data.get("network_id") == self._network_id and # from MerakiEntity
                    ssid_data.get("number") == self._ssid_number): # from MerakiEntity
                    return ssid_data
        _LOGGER.warning(
            "SSID data for network %s, SSID number %s not found in coordinator.",
            self._network_id, self._ssid_number
        )
        return None

    def _determine_state(self) -> str:
        """Determines the sensor's state based on the SSID's 'enabled' status."""
        # Use the _ssid attribute directly if it's guaranteed to be up-to-date by MerakiEntity.
        # Otherwise, fetch from coordinator for the most current state.
        # Current MerakiEntity seems to store the initial ssid_info in self._ssid.
        # For dynamic updates, fetching from coordinator is better.
        ssid_data = self._get_current_ssid_data()

        if ssid_data and isinstance(ssid_data.get("enabled"), bool):
            is_enabled = ssid_data.get("enabled")
            return STATE_ON if is_enabled else STATE_OFF
        else:
            _LOGGER.warning(
                "Could not determine enabled state for SSID %s on device %s. "
                "SSID data: %s. Defaulting to OFF.",
                self._ssid_name,
                self._device_name,
                ssid_data,
            )
            return STATE_OFF # Default to OFF if data is missing or 'enabled' is not boolean.

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handles data updates from the coordinator.

        This method is called by the `CoordinatorEntity` or `MerakiEntity`
        base class when new data is available. It updates the sensor's state.
        """
        new_state = self._determine_state()
        if self._attr_native_value != new_state:
            _LOGGER.debug(
                "Updating SSID availability for %s from %s to %s",
                self.name,
                self._attr_native_value,
                new_state,
            )
            self._attr_native_value = new_state
            self.async_write_ha_state()
        else:
            _LOGGER.debug("No change in SSID availability for %s. Current state: %s", self.name, new_state)


    @property
    def name(self) -> str:
        """Return the user-friendly name of the sensor."""
        return self._attr_name

    @property
    def unique_id(self) -> str:
        """Return the unique ID of this sensor entity."""
        return self._attr_unique_id

    @property
    def native_value(self) -> str:
        """Return the current state of the sensor (STATE_ON or STATE_OFF)."""
        # This relies on _attr_native_value being updated by __init__ and _handle_coordinator_update.
        return self._attr_native_value

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend for this sensor."""
        # Icon can be dynamic based on state if desired.
        # return "mdi:wifi" if self.native_value == STATE_ON else "mdi:wifi-off"
        return self._attr_icon # Returns the static icon set in __init__
