"""Sensor entity representing the availability of a Meraki SSID."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry

<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
=======
<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
=======
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
from .base import MerakiSSIDBaseSensor


class MerakiSSIDAvailabilitySensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Availability sensor."""

    entity_description = SensorEntityDescription(
        key="availability",
        name="Availability",
        icon="mdi:check-circle-outline",
    )

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
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
        super().__init__(coordinator, config_entry, ssid_data, "enabled")
        self._attr_native_value = self._ssid_data_at_init.get("enabled")
