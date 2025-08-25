"""Sensor for tracking clients on a specific network."""

import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from ...helpers.device_info_helpers import resolve_device_info
from ...helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkClientsSensor(
    CoordinatorEntity[MerakiDataCoordinator], SensorEntity
):
    """Representation of a Meraki network-level client counter."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network_data: dict,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._network_data = network_data
        self._network_id = network_data["id"]
        self._attr_unique_id = f"meraki_network_clients_{self._network_id}"
        self._attr_name = format_entity_name(network_data["name"], "Clients")
        self._attr_device_info = resolve_device_info(
            self._network_data, self._config_entry
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
            if client.get("networkId") == self._network_id:
                count += 1
        return count
