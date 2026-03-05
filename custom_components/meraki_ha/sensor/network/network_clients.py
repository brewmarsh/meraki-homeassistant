"""Sensor for tracking clients on a specific network."""

import logging
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ...coordinators import MerakiMainCoordinator
from ...core.entities.meraki_network_entity import MerakiNetworkEntity
from ...core.models.network import MerakiNetwork

if TYPE_CHECKING:
    from ...services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


class MerakiNetworkClientsSensor(MerakiNetworkEntity, SensorEntity):
    """Representation of a Meraki network-level client counter."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True
    _attr_name = "Clients"
    _attr_translation_key = "network_clients"

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        config_entry: ConfigEntry,
        network_data: MerakiNetwork,
        network_control_service: "NetworkControlService",
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_data)
        self._network_control_service = network_control_service
        self._attr_unique_id = f"meraki_network_clients_{self._network_id}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if not self._network_id:
            return 0
        return self._network_control_service.get_network_client_count(
            str(self._network_id)
        )
