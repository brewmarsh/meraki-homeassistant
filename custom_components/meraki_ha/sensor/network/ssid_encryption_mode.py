"""Sensor entity representing the encryption mode of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry

<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
=======
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
from .base import MerakiSSIDBaseSensor


class MerakiSSIDEncryptionModeSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Encryption Mode sensor."""

    entity_description = SensorEntityDescription(
        key="encryption_mode",
        name="Encryption Mode",
        icon="mdi:shield-key",
    )

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "encryptionMode")
        self._attr_native_value = self._ssid_data_at_init.get("encryptionMode")
