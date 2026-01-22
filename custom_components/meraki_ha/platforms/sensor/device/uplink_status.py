"""
Sensor entity for representing the uplink status of a Meraki MX appliance.

This module defines the `MerakiUplinkStatusSensor` class, a Home Assistant
sensor entity that displays the status of the primary uplink for a Meraki
MX security appliance.
"""

import logging
from typing import Any

from ....core.entities.device import MerakiDeviceEntity

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
        device_serial: str,
    ) -> None:
        """Initialize the Meraki MX Appliance Uplink Status sensor."""
        super().__init__(
            coordinator=coordinator,
            device_serial=device_serial,
            name="Uplink Status",
            unique_id_suffix="uplink_status",
        )

    @property
    def native_value(self) -> str:
        """Return the uplink status."""
        if isinstance(self.device_data, dict):
            status = self.device_data.get("status", STATE_UNKNOWN_UPLINK)
        else:
            status = getattr(self.device_data, "status", STATE_UNKNOWN_UPLINK)

        status = (status or STATE_UNKNOWN_UPLINK).lower()
        if status == "online":
            return "Online"
        if status in ["offline", "dormant"]:
            return "Offline"
        return status.capitalize()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if isinstance(self.device_data, dict):
            return {
                "wan1_ip": self.device_data.get("wan1Ip"),
                "wan2_ip": self.device_data.get("wan2Ip"),
                "public_ip": self.device_data.get("publicIp"),
                "lan_ip": self.device_data.get("lanIp"),
                "tags": self.device_data.get("tags", []),
                "network_id": self.device_data.get("networkId"),
            }

        return {
            "wan1_ip": getattr(self.device_data, "wan1_ip", None),
            "wan2_ip": getattr(self.device_data, "wan2_ip", None),
            "public_ip": getattr(self.device_data, "public_ip", None),
            "lan_ip": getattr(self.device_data, "lan_ip", None),
            "tags": getattr(self.device_data, "tags", []),
            "network_id": getattr(self.device_data, "network_id", None),
        }
