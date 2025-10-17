"""Sensor entity representing the channel of a Meraki SSID."""

from typing import Any, Dict
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
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "channel")
        self._attr_native_value = self._ssid_data_at_init.get("channel")
