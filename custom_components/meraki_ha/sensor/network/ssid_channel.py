"""Sensor entity representing the channel of a Meraki SSID."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry

from ...coordinator import MerakiDataUpdateCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDChannelSensor(MerakiSSIDBaseSensor):

    """Representation of a Meraki SSID Channel sensor."""

    entity_description = SensorEntityDescription(
        key="channel",
        name="Channel",
        icon="mdi:radio-tower",
    )

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """
        Initialize the sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            config_entry: The config entry.
            ssid_data: The SSID data.

        """
        super().__init__(coordinator, config_entry, ssid_data, "channel")
        self._attr_native_value = self._ssid_data_at_init.get("channel")
