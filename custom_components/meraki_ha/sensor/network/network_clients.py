"""Sensor for tracking clients on a specific network."""

import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
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
        network_id: str,
        network_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._network_id = network_id
        self._network_name = network_name
        self._attr_unique_id = f"meraki_network_clients_{self._network_id}"
        self._attr_name = format_entity_name(self._network_name, "Clients")

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"network_{self._network_id}")},
            name=self._network_name,
            manufacturer="Cisco Meraki",
            model="Network",
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
