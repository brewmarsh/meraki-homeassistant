"""Sensor entity representing the availability (enabled/disabled) of a Meraki SSID.

This module defines the `MerakiSSIDAvailabilitySensor` class, a Home Assistant
sensor entity that indicates whether a specific Meraki SSID is currently enabled
or disabled.
"""
import logging
from typing import Any, Dict, Optional # Added Optional, Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_OFF, STATE_ON # Standard HA states
from homeassistant.core import callback # For coordinator updates
# from homeassistant.helpers.update_coordinator import CoordinatorEntity # MerakiEntity already inherits this

# Assuming MerakiEntity is the base class for Meraki entities and handles coordinator logic.
from ..entity import MerakiEntity
# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
from ..coordinators import MerakiDataUpdateCoordinator


_LOGGER = logging.getLogger(__name__)


class MerakiSSIDAvailabilitySensor(MerakiEntity, SensorEntity):
    """Represents a Meraki SSID Availability sensor.

    This sensor entity reflects the 'enabled' state of a specific SSID
    on a Meraki device (typically a wireless access point).

    Inherits from `MerakiEntity` which is assumed to handle coordinator
    and basic device information.
    """

    # Define attributes for HA sensor properties if they are static.
    # Dynamic properties like name, unique_id, native_value, icon will be methods.
    # _attr_device_class = SensorDeviceClass.ENUM # If we had specific enum values
    # _attr_options = [STATE_ON, STATE_OFF] # If using SensorDeviceClass.ENUM

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator, # Explicit coordinator type
        device_data: Dict[str, Any], # Parent device (e.g., AP)
        ssid_data: Dict[str, Any],   # Specific SSID data for this sensor
    ) -> None:
        """Initialize the Meraki SSID Availability sensor.

        Args:
            coordinator: The data update coordinator.
            device_data: Dictionary containing information about the parent Meraki device.
                         Expected to have 'name' and 'serial'.
            ssid_data: Dictionary containing information about the SSID.
                       Expected to have 'name' (SSID name) and 'number' (SSID number).
        """
        super().__init__(coordinator, device_data, ssid_data) # Pass ssid_data to MerakiEntity

        # Construct name and unique ID using info from both device and SSID
        # _device_name and _ssid_name are assumed to be set by MerakiEntity's __init__
        base_name = f"{self._device_name or 'Device'} {self._ssid_name or f'SSID {self._ssid_number}'}"
        self._attr_name = f"{base_name} Availability"
        
        # Ensure unique_id is robust even if some parts are None
        serial_part = self._device_serial or "unknownserial"
        ssid_num_part = self._ssid_number if self._ssid_number is not None else "unknownssid"
        self._attr_unique_id = f"{serial_part}_{ssid_num_part}_availability"

        # Set initial state
        self._update_sensor_state()
        _LOGGER.debug(
            "Meraki SSID Availability Sensor Initialized: %s (Unique ID: %s)",
            self._attr_name,
            self._attr_unique_id,
        )

    def _update_sensor_state(self) -> None:
        """Update the sensor's state based on coordinator data for this SSID."""
        # Find the specific SSID data from the coordinator for the current device and SSID number
        current_ssid_data: Optional[Dict[str, Any]] = None
        if self.coordinator.data and "devices" in self.coordinator.data:
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial: # Match parent device
                    ssids_on_device = dev_data.get("ssids", []) # Assuming ssids are nested under device
                    for ssid in ssids_on_device:
                        if ssid.get("number") == self._ssid_number:
                            current_ssid_data = ssid
                            break
                    break # Found parent device
        
        if current_ssid_data:
            is_enabled: Optional[bool] = current_ssid_data.get("enabled")
            if isinstance(is_enabled, bool):
                self._attr_native_value = STATE_ON if is_enabled else STATE_OFF
            else:
                _LOGGER.warning(
                    "SSID '%s' on device '%s' has no 'enabled' status or it's not boolean. Setting to OFF.",
                    self._ssid_name, self._device_name
                )
                self._attr_native_value = STATE_OFF # Default if 'enabled' is missing or not bool
        else:
            _LOGGER.warning(
                "SSID data for '%s' (Num: %s) on device '%s' not found in coordinator. Setting availability to OFF.",
                self._ssid_name, self._ssid_number, self._device_name
            )
            self._attr_native_value = STATE_OFF # Default if SSID data not found

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.
        
        This method is called by the CoordinatorEntity base class when new data
        is available from the coordinator. It updates the sensor's state.
        """
        self._update_sensor_state()
        self.async_write_ha_state()

    # The `name` and `unique_id` properties are now handled by `_attr_name` and `_attr_unique_id`
    # set in `__init__`, so explicit @property methods are not strictly needed unless
    # there's more dynamic logic involved (which is not the case here).

    # The `native_value` property is now handled by `_attr_native_value`,
    # set by `_update_sensor_state`.

    @property
    def icon(self) -> str:
        """Return the icon of the sensor based on its state.
        
        Returns:
            A string representing the icon (e.g., "mdi:wifi" or "mdi:wifi-off").
        """
        # Icon changes based on whether the SSID is considered ON (enabled) or OFF.
        return "mdi:wifi" if self.native_value == STATE_ON else "mdi:wifi-off"

    # device_info is inherited from MerakiEntity, which should correctly link
    # this sensor to the SSID "device" if _ssid_info_data was passed to MerakiEntity's init.
    # If MerakiEntity needs adjustment for SSID-specific entities, that was handled there.
