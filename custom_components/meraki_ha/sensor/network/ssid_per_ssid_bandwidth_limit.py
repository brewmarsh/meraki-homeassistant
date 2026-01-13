"""Sensor entity representing the per-SSID bandwidth limit of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
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


class MerakiSSIDPerSsidBandwidthLimitSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Per-SSID Bandwidth Limit sensor."""

    entity_description = SensorEntityDescription(
        key="per_ssid_bandwidth_limit",
        icon="mdi:upload-network-outline",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="Kbps",
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
        direction: str,
    ) -> None:
        """Initialize the sensor."""
        attribute = f"perSsidBandwidthLimit{direction.capitalize()}"
        super().__init__(coordinator, config_entry, ssid_data, attribute)
        self._attr_name = f"Per-SSID Bandwidth Limit {direction.capitalize()}"
        self._attr_native_value = self._ssid_data_at_init.get(attribute)
        self._attr_unique_id = (
            f"ssid-{self._network_id}-{self._ssid_number}-"
            f"per-ssid-bandwidth-limit-{direction}"
        )
