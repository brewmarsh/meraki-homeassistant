"""Sensor entity representing the client count for a Meraki SSID.

This module defines the `MerakiSSIDClientCountSensor` class, a Home Assistant
sensor entity that displays the number of clients currently connected to a
specific Meraki SSID.
"""
import logging
from typing import Any, Dict, Optional # Added Optional, Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback # For coordinator updates
# from homeassistant.helpers.update_coordinator import CoordinatorEntity # MerakiEntity already inherits

# Assuming MerakiEntity is the base class for Meraki entities
from ..entity import MerakiEntity
# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
from ..coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiSSIDClientCountSensor(MerakiEntity, SensorEntity):
    """Represents a Meraki SSID Client Count sensor.

    This sensor entity displays the number of clients connected to a specific
    SSID on a Meraki device (typically a wireless access point).
    The client count is derived from the coordinator data.

    Inherits from `MerakiEntity` which handles coordinator and basic device linkage.
    """

    _attr_icon = "mdi:account-multiple" # Static icon for this sensor type
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator, # Explicit coordinator type
        device_data: Dict[str, Any], # Parent device (e.g., AP)
        ssid_data: Dict[str, Any],   # Specific SSID data for this sensor
    ) -> None:
        """Initialize the Meraki SSID Client Count sensor.

        Args:
            coordinator: The data update coordinator.
            device_data: Dictionary containing information about the parent Meraki device.
            ssid_data: Dictionary containing information about the SSID.
        """
        super().__init__(coordinator, device_data, ssid_data)

        base_name = f"{self._device_name or 'Device'} {self._ssid_name or f'SSID {self._ssid_number}'}"
        self._attr_name = f"{base_name} Client Count"
        
        serial_part = self._device_serial or "unknownserial"
        ssid_num_part = self._ssid_number if self._ssid_number is not None else "unknownssid"
        self._attr_unique_id = f"{serial_part}_{ssid_num_part}_client_count"
        
        # Set initial state
        self._update_sensor_state()
        _LOGGER.debug(
            "Meraki SSID Client Count Sensor Initialized: %s (Unique ID: %s)",
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
            # Assuming 'client_count' is a direct attribute of the SSID data from coordinator
            client_count: Optional[int] = current_ssid_data.get("client_count")
            if isinstance(client_count, int):
                self._attr_native_value = client_count
            else:
                _LOGGER.debug(
                    "SSID '%s' on device '%s' has no 'client_count' information or it's not an int (%s). Setting to 0.",
                    self._ssid_name, self._device_name, type(client_count).__name__
                )
                self._attr_native_value = 0 # Default to 0 if missing or not an int
        else:
            _LOGGER.warning(
                "SSID data for '%s' (Num: %s) on device '%s' not found in coordinator. Client count set to 0.",
                self._ssid_name, self._ssid_number, self._device_name
            )
            self._attr_native_value = 0 # Default to 0 if SSID data not found

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.
        
        This method is called by the CoordinatorEntity base class when new data
        is available from the coordinator. It updates the sensor's state.
        """
        self._update_sensor_state()
        self.async_write_ha_state()

    # `name`, `unique_id`, `native_value`, `icon`, `native_unit_of_measurement`, `state_class`
    # are handled by attributes set in `__init__` or `_update_sensor_state`.
    # `device_info` is inherited from `MerakiEntity`.
