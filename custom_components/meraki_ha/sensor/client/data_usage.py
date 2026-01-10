"""Data usage sensors for Meraki clients.

These sensors track sent and received bytes for each client,
enabling monitoring of bandwidth usage per device.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfInformation
from homeassistant.core import HomeAssistant

from ...meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiClientSensorBase


class MerakiClientSentBytesSensor(MerakiClientSensorBase):
    """Sensor showing bytes sent by the client."""

    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfInformation.BYTES
    _attr_icon = "mdi:upload"
    _attr_name = "Sent"
    _attr_suggested_display_precision = 0

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the sent bytes sensor."""
        super().__init__(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
            sensor_key="sent_bytes",
        )

    @property
    def native_value(self) -> int | None:
        """Return the bytes sent."""
        usage = self._cached_client_data.get("usage")
        if isinstance(usage, dict):
            return usage.get("sent")
        return None


class MerakiClientReceivedBytesSensor(MerakiClientSensorBase):
    """Sensor showing bytes received by the client."""

    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfInformation.BYTES
    _attr_icon = "mdi:download"
    _attr_name = "Received"
    _attr_suggested_display_precision = 0

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        client_data: dict[str, Any],
    ) -> None:
        """Initialize the received bytes sensor."""
        super().__init__(
            hass=hass,
            coordinator=coordinator,
            config_entry=config_entry,
            client_data=client_data,
            sensor_key="received_bytes",
        )

    @property
    def native_value(self) -> int | None:
        """Return the bytes received."""
        usage = self._cached_client_data.get("usage")
        if isinstance(usage, dict):
            return usage.get("recv")
        return None
