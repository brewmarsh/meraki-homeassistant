# In sensor_network_status.py
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .meraki_api.networks import get_meraki_networks, get_network_clients_count
from typing import Optional, List, Dict
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up the Meraki network client count sensors."""

    async def get_network_ids_and_names(
        api_key: str, org_id: str
    ) -> Optional[List[Dict[str, str]]]:
        """Retrieve network IDs and names from Meraki API."""
        networks = await get_meraki_networks(api_key, org_id)
        if networks is None:
            return None
        return [{"id": network["id"], "name": network["name"]} for network in networks]

    _LOGGER.debug("sensor_network_status.py: async_setup_entry called")

    coordinator = hass.data[DOMAIN][config_entry.entry_id]  # Get the coordinator

    networks = await get_network_ids_and_names(
        coordinator.api_key, coordinator.org_id
    )  # Fetch networks using coordinator's API key and org ID

    if networks:  # Only proceed if networks were successfully fetched
        entities = [
            MerakiNetworkClientCountSensor(coordinator, network["id"], network["name"])
            for network in networks
        ]
        async_add_entities(entities)
    else:
        _LOGGER.warning("Failed to retrieve Meraki networks, no sensors created.")


class MerakiNetworkClientCountSensor(SensorEntity):
    """Representation of a Meraki network client count sensor."""

    def __init__(self, coordinator, network_id, network_name):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._network_id = network_id
        self._network_name = network_name
        self._attr_name = f"{network_name} Clients (24h)"
        self._attr_unique_id = f"{DOMAIN}_{network_id}_clients_24h"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._attr_native_value = await get_network_clients_count(
            self._coordinator.api_key, self._network_id
        )
        self.async_write_ha_state()

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._network_id)},
            "name": self._network_name,
            "manufacturer": "Cisco Meraki",
            "model": "Network",
        }

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:account-network"  # Or any other suitable icon
