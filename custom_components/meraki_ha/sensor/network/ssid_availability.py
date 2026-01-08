"""Sensor entity representing the availability of a Meraki SSID."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry

from ...meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDAvailabilitySensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Availability sensor."""

    entity_description = SensorEntityDescription(
        key="availability",
        translation_key="availability",
        icon="mdi:check-circle-outline",
    )

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
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
        super().__init__(coordinator, config_entry, ssid_data, "enabled")
        self._attr_native_value = self._ssid_data_at_init.get("enabled")
