import logging
from typing import Any, Dict, List

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN, CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
from ...core.coordinators.network import MerakiNetworkCoordinator
from ...helpers.entity_helpers import format_entity_name

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkClientsSensor(
    CoordinatorEntity[MerakiNetworkCoordinator], SensorEntity
):
    """Representation of a Meraki Network Clients sensor."""

    _attr_icon = "mdi:account-multiple"
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: MerakiNetworkCoordinator,
        network_id: str,
        network_name: str,
    ) -> None:
        """Initialize the Meraki Network Clients sensor."""
        super().__init__(coordinator)
        self._network_id = network_id
        self._network_name = network_name
        name_format = self.coordinator.config_entry.options.get(
            CONF_DEVICE_NAME_FORMAT, DEFAULT_DEVICE_NAME_FORMAT
        )
        self._attr_name = format_entity_name(
            f"{network_name} Clients", "sensor", name_format, apply_format=False
        )
        self._attr_unique_id = f"meraki_network_clients_{network_id}"
        self._attr_native_value = 0
        self._attr_extra_state_attributes: Dict[str, Any] = {
            "network_id": self._network_id,
            "network_name": self._network_name,
            "clients_list": [],
        }
        self._update_state_from_coordinator()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_state_from_coordinator()
        self.async_write_ha_state()

    def _update_state_from_coordinator(self) -> None:
        """Update the sensor's state from coordinator data."""
        if self.coordinator.data is None or "clients" not in self.coordinator.data:
            self._attr_native_value = 0
            clients_for_network: List[Dict[str, Any]] = []
        else:
            all_clients: List[Dict[str, Any]] = self.coordinator.data.get("clients", [])
            clients_for_network = [
                client
                for client in all_clients
                if client.get("networkId") == self._network_id
            ]
            self._attr_native_value = len(clients_for_network)

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
                for client in clients_for_network
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
