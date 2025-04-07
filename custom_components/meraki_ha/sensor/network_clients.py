from homeassistant.components.sensor import SensorEntity
from ..meraki_api.networks import get_network_clients_count


class MerakiNetworkClientCountSensor(SensorEntity):
    def __init__(self, coordinator, network_id, network_name):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._network_id = network_id
        self._network_name = network_name
        self._attr_name = f"Meraki Network Clients {network_name}"
        self._attr_unique_id = f"meraki_network_clients_{network_id}"

    async def async_update(self):
        self._attr_native_value = await get_network_clients_count(
            self._coordinator.api_key,  # Get API key from coordinator
            self._network_id,
        )
        self.async_write_ha_state()
