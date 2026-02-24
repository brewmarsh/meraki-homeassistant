"""Sensor entity representing the availability of a Meraki SSID."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry

from ...coordinator import MerakiDataUpdateCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDAvailabilitySensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Availability sensor."""

    _attr_has_entity_name = True
    _attr_name: str | None = None

    entity_description = SensorEntityDescription(
        key="availability",
        name="availability",
        icon="mdi:check-circle-outline",
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
        super().__init__(coordinator, config_entry, ssid_data, "enabled")
        self._attr_unique_id = (
            f"{ssid_data['serial']}_MerakiSSIDAvailabilitySensor_"
            f"{self.entity_description.key}"
        )
        self._attr_native_value = self._ssid_data_at_init.get("enabled")
