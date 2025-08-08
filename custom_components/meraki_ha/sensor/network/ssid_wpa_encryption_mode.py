"""Sensor entity representing the WPA encryption mode of a Meraki SSID."""

from typing import Any, Dict
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from .base import MerakiSSIDBaseSensor


class MerakiSSIDWPAEncryptionModeSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID WPA Encryption Mode sensor."""

    entity_description = SensorEntityDescription(
        key="wpa_encryption_mode",
        name="WPA Encryption Mode",
        icon="mdi:shield-key-outline",
    )

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        ssid_data: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "wpaEncryptionMode")
        self._attr_native_value = self._ssid_data_at_init.get("wpaEncryptionMode")
