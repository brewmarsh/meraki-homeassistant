"""Connection type sensor for Meraki clients.

This sensor tracks whether a client is connected via wired or wireless,
enabling automations based on connection type changes.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ...meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiClientSensorBase


class MerakiClientConnectionTypeSensor(MerakiClientSensorBase):
    """Sensor showing the connection type (wired/wireless)."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_icon = "mdi:ethernet"
    _attr_name = "Connection Type"
    _attr_options = ["wired", "wireless"]

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the connection type sensor."""
        super().__init__(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
            sensor_key="connection_type",
        )

    @property
    def native_value(self) -> str | None:
        """Return the connection type."""
        # If client has an SSID, it's wireless
        if self._cached_client_data.get("ssid"):
            return "wireless"
        # If client has a switchport, it's wired
        if self._cached_client_data.get("switchport"):
            return "wired"
        return None

    @property
    def icon(self) -> str:
        """Return the icon based on connection type."""
        if self.native_value == "wireless":
            return "mdi:wifi"
        return "mdi:ethernet"
