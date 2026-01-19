"""Sensor entity representing the auth mode of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
<<<<<<< HEAD

from ...coordinator import MerakiDataUpdateCoordinator
=======
from homeassistant.const import EntityCategory

from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
from .base import MerakiSSIDBaseSensor


class MerakiSSIDAuthModeSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Auth Mode sensor."""

<<<<<<< HEAD
=======
    _attr_entity_category = EntityCategory.DIAGNOSTIC
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
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
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "authMode")
        self._attr_native_value = self._ssid_data_at_init.get("authMode")
