"""VLAN sensor for Meraki clients.

This sensor tracks which VLAN a client is connected to,
enabling automations based on VLAN changes.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from ...meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiClientSensorBase


class MerakiClientVLANSensor(MerakiClientSensorBase):
    """Sensor showing which VLAN the client is connected to."""

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_icon = "mdi:lan"
    _attr_name = "VLAN"

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the VLAN sensor."""
        super().__init__(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
            sensor_key="vlan",
        )

    @property
    def native_value(self) -> int | None:
        """Return the VLAN ID."""
        return self._cached_client_data.get("vlan")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional VLAN-related attributes."""
        attrs: dict[str, Any] = {}

        if vlan := self._cached_client_data.get("vlan"):
            attrs["vlan_id"] = vlan

        return attrs
