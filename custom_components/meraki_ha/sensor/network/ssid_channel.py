"""Sensor entity representing the channel of a Meraki SSID."""

from __future__ import annotations

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


class MerakiSSIDChannelSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Channel sensor."""

<<<<<<< HEAD
=======
    _attr_entity_category = EntityCategory.DIAGNOSTIC
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    entity_description = SensorEntityDescription(
        key="channel",
        name="Channel",
        icon="mdi:radio-tower",
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
        """
        Initialize the sensor.

        Args:
        ----
            coordinator: The data update coordinator.
            config_entry: The config entry.
            ssid_data: The SSID data.

        """
        super().__init__(coordinator, config_entry, ssid_data, "channel")
        self._attr_native_value = self._ssid_data_at_init.get("channel")
