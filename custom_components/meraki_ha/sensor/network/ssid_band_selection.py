"""Sensor entity representing the band selection of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry

<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
=======
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
from .base import MerakiSSIDBaseSensor


class MerakiSSIDBandSelectionSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Band Selection sensor."""

    entity_description = SensorEntityDescription(
        key="band_selection",
        name="Band Selection",
        icon="mdi:wifi-arrow-up-down",
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
        super().__init__(coordinator, config_entry, ssid_data, "bandSelection")
        self._attr_native_value = self._ssid_data_at_init.get("bandSelection")
