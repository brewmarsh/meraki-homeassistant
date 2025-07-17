import logging
from typing import Any, Dict, List, Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinators import MerakiDataUpdateCoordinator
from ..const import DOMAIN
from ..api.meraki_api._api_client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkClientsSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Network Clients sensor.

    This sensor displays the number of clients connected to a specific
    Meraki network using data from the MerakiDataUpdateCoordinator.
    It lists client details as attributes.
    """

    _attr_icon = "mdi:account-multiple"
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = False  # Data is updated by the coordinator

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        network_id: str,
        network_name: str,
    ) -> None:
        """Initialize the Meraki Network Clients sensor.

        Args:
            coordinator: The data update coordinator.
            network_id: The ID of the Meraki network this sensor is for.
            network_name: The name of the Meraki network.
        """
        super().__init__(coordinator)
        self._network_id = network_id
        self._network_name = network_name
        self._attr_name = f"{network_name} Clients"
        self._attr_unique_id = f"meraki_network_clients_{network_id}"
        # Initialize with empty state, coordinator will update it
        self._attr_native_value = 0
        self._attr_extra_state_attributes: Dict[str, Any] = {
            "network_id": self._network_id,
            "network_name": self._network_name,
            "clients_list": [],
        }
        # Set initial state
        self._update_state_from_coordinator()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state_from_coordinator()
        self.async_write_ha_state()

    def _update_state_from_coordinator(self) -> None:
        """Update the sensor's state from coordinator data.

        Filters clients for the current network and updates native value
        and attributes.
        """
        _LOGGER.debug(
            "Updating Meraki Network Clients sensor for network %s (ID: %s) from coordinator data.",
            self._network_name,
            self._network_id,
        )
        if self.coordinator.data is None or "clients" not in self.coordinator.data:
            _LOGGER.debug(
                "Coordinator data or 'clients' key is missing for network %s (ID: %s). Setting to 0 clients.",
                self._network_name,
                self._network_id,
            )
            self._attr_native_value = 0
            clients_for_network: List[Dict[str, Any]] = []
        else:
            all_clients: List[Dict[str, Any]] = self.coordinator.data.get("clients", [])
            clients_for_network = [
                client
                for client in all_clients
                if client.get("networkId") == self._network_id # Assuming client data has 'networkId'
            ]
            self._attr_native_value = len(clients_for_network)
            _LOGGER.debug(
                "Found %d clients for network %s (ID: %s) after filtering.",
                len(clients_for_network),
                self._network_name,
                self._network_id,
            )

        self._attr_extra_state_attributes = {
            "network_id": self._network_id,
            "network_name": self._network_name,
            "clients_list": [
                {
                    "mac": client.get("mac"),
                    "description": client.get("description"),
                    "ip": client.get("ip"),
                    "status": client.get("status"),
                }
                for client in clients_for_network # Use the filtered list
            ],
        }

    @property
    def available(self) -> bool:
        """Return True if coordinator has data and the 'clients' key is present."""
        return (
            super().available
            and self.coordinator.data is not None
            and "clients" in self.coordinator.data
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for linking this entity to the network "device"."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._network_id)},
            name=self._network_name,
            manufacturer="Cisco Meraki",
            model="Network",
        )

# Remove or comment out the old MerakiNetworkClientCountSensor
# class MerakiNetworkClientCountSensor(
#     CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
# ):
#     ... (rest of the old class)
#
# async def get_network_clients_count(
#     api_key: str, network_id: str, timespan: int = 86400
# ) -> int:
#     ... (old placeholder function)
