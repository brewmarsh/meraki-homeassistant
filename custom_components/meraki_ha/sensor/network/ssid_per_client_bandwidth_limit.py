"""Sensor entity representing the per-client bandwidth limit of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry

<<<<<<< HEAD
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_entity_name
>>>>>>> origin/beta
from .base import MerakiSSIDBaseSensor


class MerakiSSIDPerClientBandwidthLimitSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Per-Client Bandwidth Limit sensor."""

    entity_description = SensorEntityDescription(
        key="per_client_bandwidth_limit",
        icon="mdi:upload-network",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="Kbps",
    )

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> origin/beta
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        direction: str,
    ) -> None:
        """Initialize the sensor."""
        attribute = f"perClientBandwidthLimit{direction.capitalize()}"
        super().__init__(coordinator, config_entry, ssid_data, attribute)
        self._attr_name = f"Per-Client Bandwidth Limit {direction.capitalize()}"
        self._attr_native_value = self._ssid_data_at_init.get(attribute)
        self._attr_unique_id = (
            f"ssid-{self._network_id}-{self._ssid_number}-"
            f"per-client-bandwidth-limit-{direction}"
        )
