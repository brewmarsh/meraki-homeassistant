"""Sensor for tracking clients by device type for the entire organization."""

import logging

from custom_components.meraki_ha.const.integration import DOMAIN
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinators import MerakiMainCoordinator
from ...core.utils.naming_utils import standardize_device_name

_LOGGER = logging.getLogger(__name__)


class MerakiOrganizationDeviceTypeClientsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki organization-level client counter by device type."""

    coordinator: MerakiMainCoordinator

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        config_entry: ConfigEntry,
        device_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._device_type = device_type
        self._org_id = self.coordinator.api.organization_id
        self._attr_unique_id = f"{self._org_id}_{self._device_type}_clients"
        self._attr_name = f"{self._device_type.capitalize()} Clients"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        org_name = "Organization"
        if self.coordinator.data:
            org_data = self.coordinator.data.get("organization")
            if isinstance(org_data, dict):
                org_name = org_data.get("name", "Organization")

        return DeviceInfo(
            identifiers={(DOMAIN, self._org_id)},
            name=standardize_device_name(org_name),
            manufacturer="Cisco Meraki",
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return 0

        clients = self.coordinator.data.get("clients")
        if not isinstance(clients, list):
            return 0

        count = 0
        for client in clients:
            if not isinstance(client, dict):
                continue
            if client.get("deviceType") == self._device_type:
                count += 1
        return count
