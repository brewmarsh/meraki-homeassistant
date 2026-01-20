"""Sensor for tracking clients by device type for the entire organization."""

import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiOrganizationDeviceTypeClientsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki organization-level client counter by device type."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        device_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._device_type = device_type
        self._org_id = self.coordinator.api_client.organization_id
        self._attr_unique_id = f"{self._org_id}_{self._device_type}_clients"
        self._attr_name = f"{self._device_type.capitalize()} Clients"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._org_id)},
            name=self.coordinator.data.get("organization", {}).get(
                "name", "Meraki Organization"
            ),
            manufacturer="Cisco Meraki",
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
