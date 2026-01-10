"""Switchport sensor for Meraki clients.

This sensor tracks which switch port a wired client is connected to,
enabling automations based on port changes.
"""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ...meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiClientSensorBase


class MerakiClientSwitchportSensor(MerakiClientSensorBase):
    """Sensor showing which switchport the client is connected to."""

    _attr_icon = "mdi:ethernet"
    _attr_name = "Switchport"

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the switchport sensor."""
        super().__init__(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
            sensor_key="switchport",
        )

    @property
    def native_value(self) -> str | None:
        """Return the switchport number/ID."""
        return self._cached_client_data.get("switchport")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional switchport-related attributes."""
        attrs: dict[str, Any] = {}

        if switchport := self._cached_client_data.get("switchport"):
            attrs["port"] = switchport
        if vlan := self._cached_client_data.get("vlan"):
            attrs["vlan"] = vlan

        return attrs
