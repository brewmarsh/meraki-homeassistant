"""Sensor entity for representing the uplink status of a Meraki MX appliance.

This module defines the `MerakiUplinkStatusSensor` class, a Home Assistant
sensor entity that displays the status of the primary uplink for a Meraki
MX security appliance.
"""

import logging
from typing import Any, Dict, Optional, List  # Added Optional, List

# SensorStateClass not needed if state is string
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback  # For coordinator updates
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
from ..coordinators import MerakiDataUpdateCoordinator
from ..const import DOMAIN  # For device_info identifiers

# Assuming this function is correctly defined in the meraki_api package
# from ..meraki_api.appliance import get_meraki_device_appliance_uplinks
_LOGGER = logging.getLogger(__name__)

# Constants for sensor state if data is unavailable or an error occurs
STATE_UNAVAILABLE_UPLINK = "Unavailable"
# STATE_ERROR_UPLINK = "Error" # Can be removed if not used
STATE_UNKNOWN_UPLINK = "Unknown"


class MerakiUplinkStatusSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki MX Appliance Uplink Status sensor.

    This sensor displays the overall status of the Meraki MX device,
    which implies uplink health. Specific WAN IP details are exposed as state attributes.
    """

    _attr_icon = "mdi:upload-network-outline"  # Static icon

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_data: Dict[str, Any],  # Data for the Meraki MX appliance
    ) -> None:
        """Initialize the Meraki MX Appliance Uplink Status sensor.

        Args:
            coordinator: The data update coordinator.
            device_data: A dictionary containing information about the Meraki MX
                         appliance (e.g., name, serial, model, status, wan1Ip, publicIp).
        """
        super().__init__(coordinator)
        # Store the initial device_data to set up unique_id, name, etc.
        # This data might be stale for the first state update, but _handle_coordinator_update
        # will refresh it from the coordinator.
        self._initial_device_data: Dict[str, Any] = device_data 
        
        device_name = self._initial_device_data.get(
            "name", self._initial_device_data.get("serial", "Unknown Device")
        )
        self._device_serial = self._initial_device_data.get("serial", "") # Store serial for updates

        self._attr_name = f"{device_name} Uplink Status"
        self._attr_unique_id = f"{self._device_serial}_uplink_status"
        
        # Initial attributes, will be expanded in _update_sensor_state
        self._attr_extra_state_attributes: Dict[str, Any] = {
            "model": self._initial_device_data.get("model"),
            "serial_number": self._device_serial,
            "firmware_version": self._initial_device_data.get("firmware"),
        }

        # Set initial state by calling the update method
        self._update_sensor_state() 
        _LOGGER.debug(
            "MerakiUplinkStatusSensor Initialized: Name: %s, Unique ID: %s, Initial Device Data (subset): %s",
            self._attr_name, self._attr_unique_id,
            {k: self._initial_device_data.get(k) for k in ['name', 'serial', 'status', 'publicIp', 'wan1Ip', 'wan2Ip']}
        )

    def _update_sensor_state(self) -> None:
        """Update sensor state and attributes from coordinator data."""
        
        current_device_info: Optional[Dict[str, Any]] = None
        # Find this device's current data in the coordinator's device list
        if self.coordinator.data and self.coordinator.data.get("devices"):
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_serial:
                    current_device_info = dev_data
                    break
        
        if not current_device_info:
            _LOGGER.warning(
                "Uplink data for device '%s' (Serial: %s) not found in coordinator. Setting state to unavailable.",
                self._attr_name, self._device_serial
            )
            self._attr_native_value = STATE_UNAVAILABLE_UPLINK
            self._attr_extra_state_attributes.update({
                "wan1_ip": None, "wan2_ip": None, "public_ip": None
            })
            return

        # Update state based on the device's overall status
        device_status = current_device_info.get("status", STATE_UNKNOWN_UPLINK).lower()
        if device_status == "online":
            self._attr_native_value = "Online"
        elif device_status in ["offline", "dormant"]:
            self._attr_native_value = "Offline"
        else: # e.g., "alerting", "connecting"
            self._attr_native_value = device_status.capitalize()

        # Update attributes
        # Start with base attributes that might have been in initial_device_data but need refresh
        current_attributes = {
            "model": current_device_info.get("model"),
            "serial_number": self._device_serial, # Serial doesn't change
            "firmware_version": current_device_info.get("firmware"),
            "wan1_ip": current_device_info.get("wan1Ip"),
            "wan2_ip": current_device_info.get("wan2Ip"),
            "public_ip": current_device_info.get("publicIp"),
            "lan_ip": current_device_info.get("lanIp"), # Merged from status
            "tags": current_device_info.get("tags", []),
            "network_id": current_device_info.get("networkId"),
        }
        
        self._attr_extra_state_attributes = {
            k: v for k, v in current_attributes.items() if v is not None
        }
        _LOGGER.debug(
            "Uplink Sensor Updated: %s, State: %s, WAN1: %s, WAN2: %s, PublicIP: %s",
            self._attr_name, self._attr_native_value, 
            current_attributes.get("wan1_ip"), current_attributes.get("wan2_ip"), current_attributes.get("public_ip")
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        This method is called by the CoordinatorEntity base class when new data
        is available from the coordinator. It updates the sensor's state.
        """
        self._update_sensor_state()
        self.async_write_ha_state()

    # native_value and extra_state_attributes are now managed by _attr_ fields

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for linking this entity to the device registry.

        This links the sensor to the physical Meraki MX appliance it represents.
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
