"""Sensor entity representing the wireless channel of a Meraki SSID.

This module defines the `MerakiSSIDChannelSensor` class, a Home Assistant
sensor entity that displays the current wireless channel being used by a
specific Meraki SSID.
"""
import logging
from typing import Any, Dict, Optional, Union # Added Optional, Union

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback # For coordinator updates
# from homeassistant.helpers.update_coordinator import CoordinatorEntity # MerakiEntity already inherits

# Assuming MerakiEntity is the base class for Meraki entities
from ..entity import MerakiEntity
# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
from ..coordinators import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDChannelSensor(MerakiEntity, SensorEntity):
    """Represents a Meraki SSID Channel sensor.

    This sensor entity displays the wireless channel currently utilized by
    a specific SSID on a Meraki device (typically an access point).
    The channel information is derived from the coordinator data.

    Inherits from `MerakiEntity` which handles coordinator and basic device linkage.
    """

    _attr_icon = "mdi:radio-tower" # Static icon for this sensor type
    _attr_state_class = SensorStateClass.MEASUREMENT # If channel is numeric, otherwise it's just a generic sensor.
                                                  # Channel can be complex (e.g. "6 (20MHz)"), so not strictly measurement.
                                                  # Reverting to None if not purely numeric.
                                                  # For now, assuming it might be just the channel number.

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator, # Explicit coordinator type
        device_data: Dict[str, Any], # Parent device (e.g., AP)
        ssid_data: Dict[str, Any],   # Specific SSID data for this sensor
    ) -> None:
        """Initialize the Meraki SSID Channel sensor.

        Args:
            coordinator: The data update coordinator.
            device_data: Dictionary containing information about the parent Meraki device.
            ssid_data: Dictionary containing information about the SSID.
        """
        super().__init__(coordinator, device_data, ssid_data)

        base_name = f"{self._device_name or 'Device'} {self._ssid_name or f'SSID {self._ssid_number}'}"
        self._attr_name = f"{base_name} Channel"
        
        serial_part = self._device_serial or "unknownserial"
        ssid_num_part = self._ssid_number if self._ssid_number is not None else "unknownssid"
        self._attr_unique_id = f"{serial_part}_{ssid_num_part}_channel"
        
        # Set initial state
        self._update_sensor_state()
        _LOGGER.debug(
            "Meraki SSID Channel Sensor Initialized: %s (Unique ID: %s)",
            self._attr_name,
            self._attr_unique_id,
        )

    def _update_sensor_state(self) -> None:
        """Update the sensor's state based on coordinator data for this SSID."""
        current_ssid_data: Optional[Dict[str, Any]] = None
        if self.coordinator.data and "devices" in self.coordinator.data:
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    ssids_on_device = dev_data.get("ssids", [])
                    for ssid in ssids_on_device:
                        if ssid.get("number") == self._ssid_number:
                            current_ssid_data = ssid
                            break
                    break
        
        if current_ssid_data:
            # Assuming 'channel' is a direct attribute of the SSID data from coordinator
            # The value could be an int, string, or None.
            channel_value: Union[str, int, None] = current_ssid_data.get("channel")
            if channel_value is not None:
                self._attr_native_value = str(channel_value) # Ensure state is string, int, float or datetime
                # If channel is purely numeric and represents a measurement, SensorStateClass.MEASUREMENT is fine.
                # If it can include text like "auto" or "6 (20MHz)", then state_class=None (default) is better.
                # For now, assuming it might be numeric.
                if isinstance(channel_value, (int, float)):
                     self._attr_state_class = SensorStateClass.MEASUREMENT
                else:
                     self._attr_state_class = None # Default if not purely numeric
            else:
                _LOGGER.debug(
                    "SSID '%s' on device '%s' has no 'channel' information. Setting to None.",
                    self._ssid_name, self._device_name
                )
                self._attr_native_value = None
                self._attr_state_class = None
        else:
            _LOGGER.warning(
                "SSID data for '%s' (Num: %s) on device '%s' not found in coordinator. Channel sensor state set to None.",
                self._ssid_name, self._ssid_number, self._device_name
            )
            self._attr_native_value = None
            self._attr_state_class = None


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.
        
        This method is called by the CoordinatorEntity base class when new data
        is available from the coordinator. It updates the sensor's state.
        """
        self._update_sensor_state()
        self.async_write_ha_state()

    # `name`, `unique_id`, `native_value`, `icon` are handled by attributes set in `__init__` or `_update_sensor_state`.
    # `device_info` is inherited from `MerakiEntity`.
