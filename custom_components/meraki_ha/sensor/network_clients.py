import logging
from typing import Any, Dict, List, Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..coordinators import MerakiDataUpdateCoordinator
from ..const import DOMAIN
from ..meraki_api._api_client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkClientsSensor(
    CoordinatorEntity[MerakiDataUpdateCoordinator], SensorEntity
):
    """Representation of a Meraki Network Clients sensor.

    This sensor displays the number of clients connected to a specific
    Meraki network and lists their details as attributes.
    """

    _attr_icon = "mdi:account-multiple"
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = True # Add this line

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        network_id: str,
        network_name: str,
        meraki_api_client: MerakiAPIClient,
    ) -> None:
        """Initialize the Meraki Network Clients sensor.

        Args:
            coordinator: The data update coordinator.
            network_id: The ID of the Meraki network this sensor is for.
            network_name: The name of the Meraki network.
            meraki_api_client: The Meraki API client.
        """
        super().__init__(coordinator)
        self._network_id = network_id
        self._network_name = network_name
        self._meraki_api_client = meraki_api_client
        self._attr_name = f"{network_name} Clients"
        self._attr_unique_id = f"meraki_network_clients_{network_id}"
        self._clients_data: List[Dict[str, Any]] = []

        self._update_sensor_state()

    async def _fetch_clients_data(self) -> List[Dict[str, Any]]:
        """Fetch clients data from the Meraki API."""
        try:
            clients = await self._meraki_api_client.networks.getNetworkClients(
                networkId=self._network_id,
                timespan=86400,
                perPage=1000,
            )
            if clients is None:
                _LOGGER.debug(
                    "API call for network clients for network %s (ID: %s) returned None. Treating as zero clients.", self._network_name, self._network_id
                )
                return []
            if not clients:  # Empty list
                _LOGGER.debug(
                    "API call for network clients for network %s (ID: %s) returned an empty list. Zero clients.", self._network_name, self._network_id
                )
                return []
            # If clients is not None and not empty, it's a non-empty list
            _LOGGER.debug(
                "Successfully fetched %d clients for network %s (ID: %s).", len(clients), self._network_name, self._network_id
            )
            return clients
        except Exception as e:
            _LOGGER.error(
                "Error fetching clients for network %s (ID: %s): %s", self._network_name, self._network_id, e
            )
            return []

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # By calling async_schedule_update_ha_state with force_refresh=True,
        # we ensure that our own async_update method (which calls _fetch_clients_data)
        # is run when the coordinator signals an update.
        self.async_schedule_update_ha_state(force_refresh=True)


    def _update_sensor_state(self) -> None:
        """Update the native value and attributes of the sensor based on fetched client data."""
        # This method now relies on self._clients_data being up-to-date.
        # `async_update` will be responsible for updating `self._clients_data`.
        self._attr_native_value = len(self._clients_data)
        self._attr_extra_state_attributes = {
            "network_id": self._network_id,
            "network_name": self._network_name,
            "clients_list": [
                {
                    "mac": client.get("mac"),
                    "description": client.get("description"),
                    "ip": client.get("ip"), # Primary IP
                    # "ip6": client.get("ip6"), # Typically less critical for quick ID
                    "status": client.get("status"), # Important to know if online/offline
                    # "last_seen": client.get("lastSeen"), # Can be verbose if timestamp is long
                    # "manufacturer": client.get("manufacturer"), # Can be long
                    # "os": client.get("os"), # Can be long
                    # "user": client.get("user"), # Often None, but can be useful
                    # "ssid": client.get("ssid"), # Useful for wireless, but adds another field
                    # "vlan": client.get("vlan"), # Might be useful in complex setups
                }
                for client in self._clients_data
            ],
            # Optionally, add aggregated counts if useful and client_list is further reduced
            # "online_clients_count": sum(1 for c in self._clients_data if c.get("status") == "Online"),
        }

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This method is responsible for fetching the latest client data.
        """
        _LOGGER.debug(
            "Fetching Meraki Network Clients sensor data for network: %s",
            self._network_name,
        )
        self._clients_data = await self._fetch_clients_data()
        self._update_sensor_state() # Update internal state based on new data

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
