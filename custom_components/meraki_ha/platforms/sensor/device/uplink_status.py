"""Sensor entity for representing the uplink status of a Meraki MX appliance.

This module defines the `MerakiUplinkStatusSensor` class, a Home Assistant
sensor entity that displays the status of the primary uplink for a Meraki
MX security appliance.
"""

import logging
from typing import Any, Dict

from ....entities import MerakiDeviceEntity

_LOGGER = logging.getLogger(__name__)

# Constants for sensor state if data is unavailable or an error occurs
STATE_UNAVAILABLE_UPLINK = "Unavailable"
STATE_UNKNOWN_UPLINK = "Unknown"


class MerakiUplinkStatusSensor(MerakiDeviceEntity):
    """Representation of a Meraki MX Appliance Uplink Status sensor."""

    _attr_icon = "mdi:upload-network-outline"

    def __init__(
        self,
        coordinator,
        device_data: Dict[str, Any],  # Data for the Meraki MX appliance
    ) -> None:
        """Initialize the Meraki MX Appliance Uplink Status sensor."""
        super().__init__(
            coordinator=coordinator,
            device_data=device_data,
            name="Uplink Status",
            unique_id_suffix="uplink_status",
        )

        # Set initial state by calling the update method
        self._update_sensor_state()

    def _update_sensor_state(self) -> None:
        """Update sensor state and attributes from coordinator data."""
        current_device_data = self._get_device_data()

        if not current_device_data:
            self._attr_native_value = STATE_UNAVAILABLE_UPLINK
            self._attr_extra_state_attributes.update(
                {"wan1_ip": None, "wan2_ip": None, "public_ip": None}
            )
            return

        # Update state based on the device's overall status
        device_status = current_device_data.get("status")
        if device_status is None:
            self._attr_native_value = STATE_UNKNOWN_UPLINK
        else:
            device_status = device_status.lower()
            if device_status == "online":
                self._attr_native_value = "Online"
            elif device_status in ["offline", "dormant"]:
                self._attr_native_value = "Offline"
            else:  # e.g., "alerting", "connecting"
                self._attr_native_value = device_status.capitalize()

        # Update attributes
        # Start with base attributes that might have been in initial_device_data but need refresh
        current_attributes = {
            "wan1_ip": current_device_data.get("wan1Ip"),
            "wan2_ip": current_device_data.get("wan2Ip"),
            "public_ip": current_device_data.get("publicIp"),
            "lan_ip": current_device_data.get("lanIp"),
            "tags": current_device_data.get("tags", []),
            "network_id": current_device_data.get("networkId"),
        }

        self._attr_extra_state_attributes.update(
            {k: v for k, v in current_attributes.items() if v is not None}
        )

    def _get_uplink_status(self, device_data: Dict[str, Any]) -> str:
        """Get the status of the primary uplink for this device.

        Args:
            device_data: Device data dictionary from the coordinator

        Returns:
            String representing the uplink status
        """
        if not device_data:
            return STATE_UNAVAILABLE_UPLINK

        uplink_info = device_data.get("uplinks", [{}])[0]
        if not isinstance(uplink_info, dict):
            return STATE_UNKNOWN_UPLINK

        status = uplink_info.get("status")
        if not status:
            return STATE_UNKNOWN_UPLINK

        try:
            return str(status).lower()
        except (AttributeError, TypeError):
            _LOGGER.warning(
                "Invalid uplink status value for device %s: %s",
                device_data.get("name", "Unknown device"),
                status,
            )
            return STATE_UNKNOWN_UPLINK
