"""Sensor entity for displaying Meraki device radio settings.

This module defines the `MerakiRadioSettingsSensor` class, which represents
a sensor in Home Assistant displaying information about the radio settings
of a specific Meraki wireless device (e.g., channel, band).
"""

import logging
from typing import Any, Dict, Optional  # Union removed F401

from homeassistant.components.sensor import (
    SensorEntity,
)  # SensorStateClass removed F401
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
from ...coordinators import MerakiDataUpdateCoordinator
from ...const import DOMAIN

# Assuming this function is correctly defined in the meraki_api package
# from .meraki_api.wireless import get_meraki_device_wireless_radio_settings
_LOGGER = logging.getLogger(__name__)

# Constants for sensor state if data is unavailable or an error occurs
# More descriptive than just UNAVAILABLE
STATE_UNAVAILABLE_VALUE = "Unavailable"
STATE_ERROR_VALUE = "Error"


class MerakiRadioSettingsSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Radio Settings sensor.

    This sensor displays a key piece of radio information (e.g., channel)
    as its main state and other radio settings as state attributes.
    The data is sourced from the `MerakiDataUpdateCoordinator` or fetched
    directly if this entity manages its own updates.

    Note: The original implementation had its own `async_update` method,
    suggesting it might fetch data independently. If it's intended to use
    the coordinator's data, `async_update` should be removed and data
    retrieved from `self.coordinator.data` in `_handle_coordinator_update`.
    This revision assumes it will become a true CoordinatorEntity.

    Attributes:
        _attr_name: The name of the sensor.
        _attr_unique_id: The unique ID of the sensor.
        _attr_icon: The icon for the sensor.
        _device_info_data: Raw dictionary data for the associated Meraki device.
    """

    _attr_icon = "mdi:wifi-settings"  # Icon representing WiFi settings
    _attr_entity_registry_enabled_default = False

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        # Data for the Meraki device this sensor is for
        device_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Radio Settings sensor.

        Args:
            coordinator: The data update coordinator.
            device_data: A dictionary containing information about the Meraki device
                         (e.g., name, serial, model).
        """
        super().__init__(coordinator)
        self._device_info_data: Dict[str, Any] = device_data
        device_name = self._device_info_data.get(
            "name", self._device_info_data.get("serial", "Unknown Device")
        )
        device_serial = self._device_info_data.get("serial", "")

        self._attr_name = f"{device_name} Radio Settings"
        self._attr_unique_id = f"{device_serial}_radio_settings"

        # Initialize state attributes, these will be updated from coordinator
        self._attr_extra_state_attributes: Dict[str, Any] = {
            "model": self._device_info_data.get("model"),
            "serial_number": device_serial,
            "firmware_version": self._device_info_data.get("firmware"),
        }
        # Set initial state
        self._update_sensor_state()
        # _LOGGER.debug("Meraki Radio Settings Sensor Initialized: %s", self._attr_name) # Removed

    def _update_sensor_state(self) -> None:
        """Update sensor state and attributes from coordinator data.

        This method assumes the coordinator's data (`self.coordinator.data`)
        contains a structure where radio settings for each device can be found.
        Example structure: `coordinator.data['devices_radio_settings']['SERIAL'] = {'channel': X, ...}`
        """
        device_serial = self._device_info_data.get("serial")
        radio_settings: Optional[Dict[str, Any]] = None

        current_device_dict: Optional[Dict[str, Any]] = None
        if self.coordinator.data and "devices" in self.coordinator.data:
            for dev in self.coordinator.data["devices"]:
                if dev.get("serial") == device_serial:
                    current_device_dict = dev
                    break

        if current_device_dict:
            radio_settings = current_device_dict.get("radio_settings")
        else:
            radio_settings = None  # Device not found

        if radio_settings and isinstance(radio_settings, dict):
            # Determine primary state (e.g., channel, or a summary string)
            # The original code used 'channel' as the primary state.
            primary_value = radio_settings.get("channel")
            if primary_value is not None:
                # Sensor state must be string, int, float, or datetime
                self._attr_native_value = str(primary_value)
            else:
                self._attr_native_value = STATE_UNAVAILABLE_VALUE

            # Update all radio settings as extra state attributes
            # Start with base attributes and add/override with radio_settings
            current_attributes = {
                "model": self._device_info_data.get("model"),
                "serial_number": device_serial,
                "firmware_version": self._device_info_data.get("firmware"),
            }
            current_attributes.update(radio_settings)
            self._attr_extra_state_attributes = {
                k: v for k, v in current_attributes.items() if v is not None
            }
        else:
            _LOGGER.warning(
                "Radio settings for device '%s' (Serial: %s) not found in coordinator data. Setting state to unavailable.",
                self._device_info_data.get("name", "N/A"),
                device_serial,
            )
            self._attr_native_value = STATE_UNAVAILABLE_VALUE
            # Keep basic attributes if radio settings are missing
            self._attr_extra_state_attributes = {
                "model": self._device_info_data.get("model"),
                "serial_number": device_serial,
                "firmware_version": self._device_info_data.get("firmware"),
            }
            self._attr_extra_state_attributes = {
                k: v
                for k, v in self._attr_extra_state_attributes.items()
                if v is not None
            }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        This method is called by the CoordinatorEntity base class when new data
        is available from the coordinator. It updates the sensor's state.
        """
        self._update_sensor_state()
        self.async_write_ha_state()

    # native_value property is now managed by _attr_native_value
    # extra_state_attributes property is now managed by
    # _attr_extra_state_attributes

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for linking this entity to the device registry.

        This links the sensor to the physical Meraki device it represents.
        """
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_info_data["serial"])},
            name=str(
                self._device_info_data.get("name", self._device_info_data["serial"])
            ),
            manufacturer="Cisco Meraki",
            model=str(self._device_info_data.get("model", "Unknown")),
            sw_version=str(self._device_info_data.get("firmware", "")),
        )
