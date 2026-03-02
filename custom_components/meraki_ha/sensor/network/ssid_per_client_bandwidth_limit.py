"""Sensor entity representing the per-client bandwidth limit of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfDataRate

from ...coordinators import MerakiMainCoordinator
from .base import MerakiSSIDBaseSensor

PER_CLIENT_BANDWIDTH_LIMIT_UP = SensorEntityDescription(
    key="per_client_bandwidth_limit_up",
    name="per-client bandwidth limit up",
    icon="mdi:upload-network",
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND,
)

PER_CLIENT_BANDWIDTH_LIMIT_DOWN = SensorEntityDescription(
    key="per_client_bandwidth_limit_down",
    name="per-client bandwidth limit down",
    icon="mdi:download-network",
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND,
)


class MerakiSSIDPerClientBandwidthLimitSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Per-Client Bandwidth Limit sensor."""

    _attr_has_entity_name = True
    _attr_name: str | None = None

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        direction: str,
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = (
            PER_CLIENT_BANDWIDTH_LIMIT_UP
            if direction.lower() == "up"
            else PER_CLIENT_BANDWIDTH_LIMIT_DOWN
        )
        attribute = f"perClientBandwidthLimit{direction.capitalize()}"
        super().__init__(coordinator, config_entry, ssid_data, attribute)
        self._attr_native_value = self._ssid_data_at_init.get(attribute)

        # Apply robust unique_id format: serial_classname_key
        # For SSID entities, we use a combination of networkId and SSID number
        # as the unique prefix
        serial = ssid_data.get(
            "networkId", coordinator.data.get("networkId", "unknown")
        )
        number = ssid_data.get("number", "unknown")
        self._attr_unique_id = (
            f"{serial}_{number}_{self.__class__.__name__}_{self.entity_description.key}"
        )
