"""Sensor entity representing the auth mode of a Meraki SSID."""

from typing import Any, Dict
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDAuthModeSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Auth Mode sensor."""

    entity_description = SensorEntityDescription(
        key="auth_mode",
        name="Auth Mode",
        icon="mdi:lock",
    )

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "authMode")
        self._attr_native_value = self._ssid_data_at_init.get("authMode")
