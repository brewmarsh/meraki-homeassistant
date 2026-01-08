"""Sensor entity representing the visibility of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry

from ...meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDVisibleSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Visibility sensor."""

    entity_description = SensorEntityDescription(
        key="visible",
        translation_key="visible",
        icon="mdi:eye",
    )

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "visible")
        self._attr_native_value = self._ssid_data_at_init.get("visible")
