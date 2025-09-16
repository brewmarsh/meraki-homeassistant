"""Base class for Meraki Network sensors."""

import logging
from typing import Any, Dict, Optional
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from ...coordinator import MerakiDataUpdateCoordinator
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkBaseSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Base class for Meraki Network sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_data: Dict[str, Any],
        attribute: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._network_data_at_init = network_data
        self._attribute = attribute
        self._network_id = network_data.get("id")
        self._attr_unique_id = f"network-{self._network_id}-{self._attribute}"
        # Set device_info directly in init
        self._attr_device_info = resolve_device_info(
            entity_data=self._network_data_at_init,
            config_entry=self._config_entry,
        )

    def _get_current_network_data(self) -> Optional[Dict[str, Any]]:
        """Retrieve the latest data for this Network from the coordinator."""
        if not self.coordinator.data or "networks" not in self.coordinator.data:
            return None
        for network in self.coordinator.data["networks"]:
            if network.get("id") == self._network_id:
                return network
        return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not super().available or not self.coordinator.data:
            return False
        network_data = self._get_current_network_data()
        return network_data is not None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        network_data = self._get_current_network_data()
        if network_data:
            self._attr_native_value = network_data.get(self._attribute)
        self.async_write_ha_state()
