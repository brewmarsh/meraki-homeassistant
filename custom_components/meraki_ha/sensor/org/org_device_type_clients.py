"""Sensor for tracking clients by device type for the entire organization."""

import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
<<<<<<< HEAD
<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.entity_helpers import format_entity_name
=======
<<<<<<< HEAD
from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.entity_helpers import format_entity_name
=======
from ...helpers.entity_helpers import format_entity_name
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
from ...helpers.entity_helpers import format_entity_name
from ...meraki_data_coordinator import MerakiDataCoordinator
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

_LOGGER = logging.getLogger(__name__)


class MerakiOrganizationDeviceTypeClientsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Meraki organization-level client counter by device type."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
<<<<<<< HEAD
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
<<<<<<< HEAD
        coordinator: MerakiDataUpdateCoordinator,
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        coordinator: MerakiDataCoordinator,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        config_entry: ConfigEntry,
        device_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._device_type = device_type
        self._org_id = self.coordinator.api_client.organization_id
        self._attr_unique_id = f"{self._org_id}_{self._device_type}_clients"
        self._attr_name = format_entity_name(self._device_type.capitalize(), "Clients")

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
