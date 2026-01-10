"""Connected device sensor for Meraki clients.

This sensor tracks which Meraki device (AP, switch) a client is connected to,
enabling automations based on device roaming or location changes.
"""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ...meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiClientSensorBase


class MerakiClientConnectedDeviceSensor(MerakiClientSensorBase):
    """Sensor showing which Meraki device the client is connected to."""

    _attr_icon = "mdi:access-point-network"
    _attr_name = "Connected Device"

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the connected device sensor."""
        super().__init__(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
            sensor_key="connected_device",
        )

    @property
    def native_value(self) -> str | None:
        """Return the name of the device the client is connected to."""
        return self._cached_client_data.get("recentDeviceName")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional connected device attributes."""
        attrs: dict[str, Any] = {}

        if device_name := self._cached_client_data.get("recentDeviceName"):
            attrs["device_name"] = device_name
        if device_serial := self._cached_client_data.get("recentDeviceSerial"):
            attrs["device_serial"] = device_serial
        if device_mac := self._cached_client_data.get("recentDeviceMac"):
            attrs["device_mac"] = device_mac
        if switchport := self._cached_client_data.get("switchport"):
            attrs["switchport"] = switchport

        return attrs
