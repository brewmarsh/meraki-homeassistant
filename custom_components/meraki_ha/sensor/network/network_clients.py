"""Sensor for tracking clients on a specific network."""

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info
from ...helpers.entity_helpers import format_entity_name

if TYPE_CHECKING:
    from ...services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class MerakiNetworkClientsSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki network-level client counter."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_data: dict,
        network_control_service: "NetworkControlService",
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._network_data = network_data
        self._network_id = network_data["id"]
        self._network_control_service = network_control_service
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
        return self._network_control_service.get_network_client_count(self._network_id)
