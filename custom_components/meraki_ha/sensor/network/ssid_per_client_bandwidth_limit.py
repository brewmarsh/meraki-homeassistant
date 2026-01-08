"""Sensor entity representing the per-client bandwidth limit of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry

from ...meraki_data_coordinator import MerakiDataCoordinator
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
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        direction: str,
    ) -> None:
        """Initialize the sensor."""
        self._direction = direction
        attribute = f"perClientBandwidthLimit{direction.capitalize()}"
        super().__init__(coordinator, config_entry, ssid_data, attribute)
        self.translation_key = "per_client_bandwidth_limit"
        self._attr_native_value = self._ssid_data_at_init.get(attribute)
        self._attr_unique_id = (
            f"ssid-{self._network_id}-{self._ssid_number}-"
            f"per-client-bandwidth-limit-{direction}"
        )

    @property
    def translation_placeholders(self) -> dict[str, str]:
        """Return the placeholders for translation."""
        return {"direction": self._direction.capitalize()}
