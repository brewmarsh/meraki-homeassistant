"""Sensor entity representing the band selection of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory

from ...coordinators import MerakiMainCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDBandSelectionSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Band Selection sensor."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    entity_description = SensorEntityDescription(
        key="band_selection",
        name=None,
        icon="mdi:wifi-arrow-up-down",
    )

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "bandSelection")
        self._attr_native_value = self._ssid_data_at_init.get("bandSelection")
        self._attr_unique_id = (
            f"{ssid_data.get('networkId')}_{ssid_data.get('number')}_"
            f"{self.entity_description.key}"
        )
