"""Sensor entity representing the encryption mode of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory

from ...coordinator import MerakiDataUpdateCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDEncryptionModeSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Encryption Mode sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    entity_description = SensorEntityDescription(
        key="encryption_mode",
        name="Encryption Mode",
        icon="mdi:shield-key",
    )

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "encryptionMode")
        self._attr_native_value = self._ssid_data_at_init.get("encryptionMode")
