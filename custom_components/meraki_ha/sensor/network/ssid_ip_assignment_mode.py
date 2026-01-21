"""Sensor entity representing the IP assignment mode of a Meraki SSID."""

from typing import Any

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory

<<<<<<< HEAD
from ...meraki_data_coordinator import MerakiDataCoordinator
=======
from ...coordinator import MerakiDataUpdateCoordinator
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
from .base import MerakiSSIDBaseSensor


class MerakiSSIDIPAssignmentModeSensor(MerakiSSIDBaseSensor):
    """Representation of a Meraki SSID IP Assignment Mode sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    entity_description = SensorEntityDescription(
        key="ip_assignment_mode",
        name="IP Assignment Mode",
        icon="mdi:ip-network",
    )

    def __init__(
        self,
<<<<<<< HEAD
        coordinator: MerakiDataCoordinator,
=======
        coordinator: MerakiDataUpdateCoordinator,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        config_entry: ConfigEntry,
        ssid_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, ssid_data, "ipAssignmentMode")
        self._attr_native_value = self._ssid_data_at_init.get("ipAssignmentMode")
