"""Sensor entity representing the encryption mode of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
<<<<<<< HEAD

from ...coordinator import MerakiDataUpdateCoordinator
=======
from homeassistant.const import EntityCategory

from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
from .base import MerakiSSIDBaseSensor


class MerakiSSIDEncryptionModeSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID Encryption Mode sensor."""

<<<<<<< HEAD
=======
    _attr_entity_category = EntityCategory.DIAGNOSTIC
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
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
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "encryptionMode")
        self._attr_native_value = self._ssid_data_at_init.get("encryptionMode")
