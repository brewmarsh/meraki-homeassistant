# custom_components/meraki_ha/sensor/network_identity.py
"""Sensor entity representing the identity of a Meraki network."""

import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinators.base_coordinator import MerakiDataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkIdentitySensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Network Identity sensor.

    This sensor displays the network name as its state and provides
    network ID and type as attributes for diagnostic purposes.
    """

    _attr_icon = "mdi:information-outline"  # Or "mdi:lan", "mdi:network"

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        network_data: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki Network Identity sensor.

        Args:
            coordinator: The data update coordinator.
            network_data: A dictionary containing the network's data,
                          expected to have 'id', 'name', and 'type'.
        """
        super().__init__(coordinator)
        self._network_id: str = network_data.get("id", "Unknown ID")
        self._network_name: str = network_data.get("name", "Unknown Network")
        self._network_type: str = network_data.get("type", "Unknown Type")

        self._attr_name = f"{self._network_name} Network Identity"
        self._attr_unique_id = f"meraki_network_identity_{self._network_id}"

        # Set initial state and attributes
        self._update_sensor_state()

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._network_id)},
            name=self._network_name, # So it's grouped with other entities for this network device
            manufacturer="Cisco Meraki",
            model="Network Information",
        )
        # _LOGGER.debug(
        #     "MerakiNetworkIdentitySensor Initialized: Name: %s, Unique ID: %s, Network ID: %s, Type: %s",
        #     self._attr_name,
        #     self._attr_unique_id,
        #     self._network_id,
        #     self._network_type,
        # ) # Removed

    def _update_sensor_state(self) -> None:
        """Update the native value and attributes of the sensor."""
        # The network identity (ID, name, type) is generally static.
        # However, if the name could change in Meraki dashboard and we want to reflect it:
        # We need to find this specific network's data in the coordinator.
        # Assuming main_coordinator.data["networks"] is a list of dicts like network_data.

        current_network_data = None
        if self.coordinator.data and "networks" in self.coordinator.data:
            for net_data in self.coordinator.data["networks"]:
                if net_data.get("id") == self._network_id:
                    current_network_data = net_data
                    break

        if current_network_data:
            self._network_name = current_network_data.get("name", self._network_name) # Keep old if new is missing
            self._network_type = current_network_data.get("type", self._network_type) # Keep old if new is missing
            # Update name attribute if network name changes
            self._attr_name = f"{self._network_name} Network Identity"


        self._attr_native_value = self._network_name # State is the network name
        self._attr_extra_state_attributes = {
            "network_id": self._network_id,
            "network_name": self._network_name, # Display name in attributes as well
            "network_type": self._network_type,
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # This method is called when the coordinator has new data.
        # We update our sensor's state if relevant data has changed.
        self._update_sensor_state()
        self.async_write_ha_state()

    # If this sensor's data is not expected to change after initial setup,
    # _handle_coordinator_update and _update_sensor_state could be simplified,
    # or _attr_should_poll could be set to False if it never changes.
    # However, network name *can* change.
