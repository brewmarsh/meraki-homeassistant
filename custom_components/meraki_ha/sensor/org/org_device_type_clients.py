"""Sensor for tracking clients by device type for the entire organization."""

import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...helpers.entity_helpers import format_entity_name
from ...meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiOrganizationDeviceTypeClientsSensor(
    CoordinatorEntity[MerakiDataCoordinator], SensorEntity
):
    """Representation of a Meraki organization-level client counter by device type."""

    coordinator: MerakiDataCoordinator
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        device_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._device_type = device_type
        self._org_id = self.coordinator.api.organization_id
        self._attr_unique_id = f"{self._org_id}_{self._device_type}_clients"
        self._attr_name = format_entity_name(self._device_type.capitalize(), "Clients")

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        if self.coordinator.config_entry is None:
            return None
        org_name = self.coordinator.data.get("organization", {}).get(
            "name", "Meraki Organization"
        )
        org_device_data = {"name": org_name, "productType": "organization"}
        formatted_name = format_device_name(
            device=org_device_data,
            config=self.coordinator.config_entry.options,
        )
        return DeviceInfo(
            # Use org_ prefix to prevent collisions with other entity types
            identifiers={(DOMAIN, f"org_{self._org_id}")},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Organization",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if not self.coordinator.data or not self.coordinator.data.get("clients"):
            return 0

        count = 0
        for client in self.coordinator.data["clients"]:
            if client.get("deviceType") == self._device_type:
                count += 1
        return count
