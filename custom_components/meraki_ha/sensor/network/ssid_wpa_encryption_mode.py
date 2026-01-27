"""Sensor entity representing the WPA encryption mode of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory

from ...coordinator import MerakiDataUpdateCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDWPAEncryptionModeSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID WPA Encryption Mode sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    entity_description = SensorEntityDescription(
        key="wpa_encryption_mode",
        name="WPA Encryption Mode",
        icon="mdi:shield-key-outline",
    )

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "wpaEncryptionMode")
        self._attr_native_value = self._ssid_data_at_init.get("wpaEncryptionMode")
