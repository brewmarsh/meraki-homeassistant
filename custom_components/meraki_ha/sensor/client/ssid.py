"""SSID sensor for Meraki clients.

This sensor tracks which wireless network (SSID) a client is connected to,
enabling automations based on network changes.
"""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ...meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiClientSensorBase


class MerakiClientSSIDSensor(MerakiClientSensorBase):
    """Sensor showing which SSID the client is connected to."""

    _attr_icon = "mdi:wifi"
    _attr_name = "SSID"

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the SSID sensor."""
        super().__init__(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
            sensor_key="ssid",
        )

    @property
    def native_value(self) -> str | None:
        """Return the SSID name."""
        return self._cached_client_data.get("ssid")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional SSID-related attributes."""
        attrs: dict[str, Any] = {}

        if ssid := self._cached_client_data.get("ssid"):
            attrs["ssid_name"] = ssid
        if band := self._cached_client_data.get("wirelessCapabilities"):
            attrs["wireless_capabilities"] = band

        return attrs
