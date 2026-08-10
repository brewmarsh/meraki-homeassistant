"""Sensor for tracking clients by device type for the entire organization."""

import logging

from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from custom_components.meraki_ha.const.integration import DOMAIN

from ...coordinators import MerakiMainCoordinator
from ...core.utils.naming_utils import standardize_device_name
from ...entity import MerakiSensor

_LOGGER = logging.getLogger(__name__)


class MerakiOrganizationDeviceTypeClientsSensor(MerakiSensor):
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
        self._attr_native_value = 0
        self._update_state()

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
        self._update_state()
        self.async_write_ha_state()

    def _update_state(self) -> None:
        """Update the internal state of the sensor."""
        if not self.coordinator.data:
            self._attr_native_value = 0
            return

        clients = self.coordinator.data.get("clients")
        if not isinstance(clients, list):
            self._attr_native_value = 0
            return

        count = 0
        for client in clients:
            if not isinstance(client, dict):
                continue
            if client.get("deviceType") == self._device_type:
                count += 1
        self._attr_native_value = count
