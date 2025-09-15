"""Sensor entity representing the splash page of a Meraki SSID."""

from typing import Any, Dict
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from ...coordinator import MerakiDataUpdateCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDSplashPageSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Splash Page sensor."""

    entity_description = SensorEntityDescription(
        key="splash_page",
        name="Splash Page",
        icon="mdi:page-next",
    )

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "splashPage")
        self._attr_native_value = self._ssid_data_at_init.get("splashPage")
