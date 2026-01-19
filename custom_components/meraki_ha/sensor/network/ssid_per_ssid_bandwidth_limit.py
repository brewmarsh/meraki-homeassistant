"""Sensor entity representing the per-SSID bandwidth limit of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry

<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_entity_name
=======
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
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
        coordinator: MerakiDataCoordinator,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
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
