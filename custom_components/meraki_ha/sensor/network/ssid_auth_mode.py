"""Sensor entity representing the auth mode of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry

<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
=======
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
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
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "authMode")
        self._attr_native_value = self._ssid_data_at_init.get("authMode")
