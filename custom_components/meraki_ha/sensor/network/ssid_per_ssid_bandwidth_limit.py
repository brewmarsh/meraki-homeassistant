"""Sensor entity representing the per-SSID bandwidth limit of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfDataRate

from ...coordinator import MerakiDataUpdateCoordinator
from .base import MerakiSSIDBaseSensor

BANDWIDTH_LIMIT_UP = SensorEntityDescription(
    key="bandwidth_limit_up",
    name=None,
    icon="mdi:upload-network-outline",
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND,
)

BANDWIDTH_LIMIT_DOWN = SensorEntityDescription(
    key="bandwidth_limit_down",
    name=None,
    icon="mdi:download-network-outline",
    state_class=SensorStateClass.MEASUREMENT,
    native_unit_of_measurement=UnitOfDataRate.KILOBITS_PER_SECOND,
)


class MerakiSSIDPerSsidBandwidthLimitSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Per-SSID Bandwidth Limit sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
        direction: str,
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = (
            BANDWIDTH_LIMIT_UP if direction.lower() == "up" else BANDWIDTH_LIMIT_DOWN
        )
        attribute = f"perSsidBandwidthLimit{direction.capitalize()}"
        super().__init__(coordinator, config_entry, ssid_data, attribute)
        self._attr_native_value = self._ssid_data_at_init.get(attribute)

        # Robust unique_id format: serial_classname_key
        serial = ssid_data.get("serial") or getattr(coordinator, "serial", "unknown")
        self._attr_unique_id = f"{serial}_{self.__class__.__name__}_{attribute}"
