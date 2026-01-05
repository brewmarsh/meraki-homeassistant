"""Sensor entity representing the PSK of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory

from ...meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDPSKSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID PSK sensor."""

    entity_description = SensorEntityDescription(
        key="psk",
        name="PSK",
        icon="mdi:key-wireless",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    )

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "psk")
        # Initialize the native value
        self._attr_native_value = self._ssid_data_at_init.get("psk")
