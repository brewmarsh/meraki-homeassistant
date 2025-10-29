"""Sensor entity representing the client count of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry

from ...coordinator import MerakiDataUpdateCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDClientCountSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Client Count sensor."""

    entity_description = SensorEntityDescription(
        key="client_count",
        name="Client Count",
        icon="mdi:account-multiple",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="clients",
    )

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "clientCount")
        self._attr_native_value = self._ssid_data_at_init.get("clientCount")
