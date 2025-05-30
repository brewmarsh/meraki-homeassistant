"""Sensor platform for monitoring Meraki network status, specifically client counts.

This module defines sensor entities related to Meraki network status, focusing
on the number of clients connected to each network. It includes setup logic
for discovering networks and creating corresponding client count sensors.

Note: This file appears to define a `MerakiNetworkClientCountSensor` similar to
the one in `network_clients.py`. This might indicate redundancy or an alternative
setup path. The improvements will be applied assuming this file is in use.
"""
import logging
from typing import Any, Dict, List, Optional  # Added Any

# Added SensorStateClass
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
# For type hinting coordinator
# from homeassistant.helpers.update_coordinator import CoordinatorEntity # Unused F401
from homeassistant.helpers.entity import DeviceInfo # Added for F821

from ..const import DOMAIN
from ..meraki_api.exceptions import MerakiApiException # Added for F821
# Assuming MerakiDataUpdateCoordinator is the correct type for the coordinator
from ..coordinators import MerakiDataUpdateCoordinator

# Assuming these are async functions from the meraki_api package
# from ..meraki_api.networks import get_meraki_networks, get_network_clients_count
# Placeholders for the functions if not available for type checking


async def get_meraki_networks(
        api_key: str, org_id: str) -> Optional[List[Dict[str, Any]]]:
    """Placeholder: Fetches all networks for an organization."""
    _LOGGER.warning(
        "Using placeholder for get_meraki_networks for org_id %s.",
        org_id)
    return [{"id": "N_placeholder_net1",
             "name": "Placeholder Network 1",
             "productTypes": ["wireless"]}]


async def get_network_clients_count(
        api_key: str,
        network_id: str,
        timespan: int = 86400) -> Optional[int]:
    """Placeholder: Fetches network client count."""
    _LOGGER.warning(
        "Using placeholder for get_network_clients_count for network_id %s.",
        network_id)
    return 0

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki network client count sensors from a config entry.

    This function discovers Meraki networks associated with the given organization
    and creates a `MerakiNetworkClientCountSensor` for each network found.

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry for this Meraki integration instance.
        async_add_entities: Callback function to add entities to Home Assistant.
    """
    _LOGGER.debug("Setting up Meraki network status (client count) sensors.")

    # It's assumed the coordinator is already initialized and stored in hass.data
    # The type hint for coordinator should be the specific coordinator class.
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Helper function defined inside async_setup_entry
    async def _get_network_ids_and_names(
        api_key: str, org_id: str
    ) -> Optional[List[Dict[str, str]]]:
        """Retrieve network IDs and names from Meraki API.

        Args:
            api_key: The Meraki API key.
            org_id: The Meraki Organization ID.

        Returns:
            A list of dictionaries, each containing 'id' and 'name' of a network,
            or None if fetching fails.
        """
        _LOGGER.debug(
            "Fetching network list for org_id: %s (for sensor setup)",
            org_id)
        networks_data: Optional[
            List[Dict[str, Any]]
        ] = await get_meraki_networks(api_key, org_id)
        if networks_data is None:
            _LOGGER.error("Failed to retrieve networks for org_id: %s", org_id)
            return None

        processed_networks: List[Dict[str, str]] = []
        for network in networks_data:
            network_id = network.get("id")
            network_name = network.get("name")
            if network_id and network_name:
                processed_networks.append(
                    {"id": str(network_id), "name": str(network_name)})
            else:
                _LOGGER.warning(
                    "Network found with missing ID or name: %s", network)
        return processed_networks

    networks: Optional[List[Dict[str, str]]] = await _get_network_ids_and_names(
        coordinator.api_key, coordinator.org_id
    )

    if networks:
        entities: List[MerakiNetworkClientCountSensor] = [
            MerakiNetworkClientCountSensor(coordinator, network["id"], network["name"])
            for network in networks
        ]
        if entities:
            async_add_entities(entities)
            _LOGGER.info(
                "Added %d Meraki network client count sensors.",
                len(entities))
        else:
            _LOGGER.info(
                "No network client count sensors were created (networks list might be empty or filtered).")
    else:
        _LOGGER.warning(
            "Failed to retrieve Meraki networks for org_id %s; no network client count sensors will be created.",
            coordinator.org_id)


class MerakiNetworkClientCountSensor(SensorEntity):
    """Representation of a Meraki network client count sensor.

    This sensor entity displays the number of clients connected to a specific
    Meraki network over the last 24 hours. It fetches this data periodically.

    Note: This class defines its own `async_update` method, meaning it fetches
    data independently rather than relying solely on a central coordinator for
    this specific data point. If it were to use a central coordinator for its
    value, it would typically inherit from `CoordinatorEntity`.

    Attributes:
        _coordinator: Reference to the main data coordinator (primarily for API key).
        _network_id: The ID of the Meraki network this sensor monitors.
        _network_name: The name of the Meraki network.
        _attr_name: The name of the sensor entity.
        _attr_unique_id: The unique ID of the sensor entity.
        _attr_native_value: The current value (client count) of the sensor.
        _attr_icon: The icon for the sensor.
        _attr_native_unit_of_measurement: The unit of measurement.
        _attr_state_class: The state class of the sensor.
    """
    _attr_icon = "mdi:account-multiple"  # Changed from mdi:account-network for multiple clients
    _attr_native_unit_of_measurement = "clients"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,  # Used for API key access
        network_id: str,
        network_name: str,
    ) -> None:
        """Initialize the Meraki Network Client Count sensor.

        Args:
            coordinator: The main Meraki data update coordinator, used here to
                         access shared configuration like the API key.
            network_id: The ID of the Meraki network.
            network_name: The name of the Meraki network.
        """
        self._coordinator: MerakiDataUpdateCoordinator = coordinator
        self._network_id: str = network_id
        self._network_name: str = network_name
        # User-friendly name, including the network name for clarity
        self._attr_name = f"{self._network_name} Client Count (24h)"
        self._attr_unique_id = f"{DOMAIN}_{self._network_id}_clients_24h"
        # Initialize native_value
        self._attr_native_value: Optional[int] = None

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This method is called periodically by Home Assistant to update the
        sensor's state. It calls the Meraki API to get the current client count.
        """
        _LOGGER.debug(
            "Updating Meraki Network Client Count sensor for network: %s (ID: %s)",
            self._network_name,
            self._network_id,
        )
        try:
            # Assuming get_network_clients_count is an async function that
            # returns Optional[int]
            client_count: Optional[int] = await get_network_clients_count(
                self._coordinator.api_key, self._network_id
            )
            if client_count is not None:
                self._attr_native_value = client_count
            else:
                _LOGGER.warning(
                    "Received no client count for network %s (ID: %s), setting to None.",
                    self._network_name,
                    self._network_id)
                self._attr_native_value = None  # Explicitly set to None if API returns None
        except MerakiApiException as e:  # Catch specific API errors
            _LOGGER.error(
                "API error updating client count for network '%s' (ID: %s): %s",
                self._network_name,
                self._network_id,
                e)
            self._attr_native_value = None  # Set to None or an error state on API failure
        except Exception as e:  # Catch any other unexpected errors
            _LOGGER.exception(
                "Unexpected error updating client count for network '%s' (ID: %s): %s",
                self._network_name,
                self._network_id,
                e)
            self._attr_native_value = None  # Set to None or an error state

        # self.async_write_ha_state() # Not needed if using _attr_native_value
        # with SensorEntity

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for linking this entity to the network "device".

        This sensor is associated with a Meraki Network, which itself is
        represented as a device in Home Assistant.
        """
        return DeviceInfo(
            # Link to the network "device"
            identifiers={(DOMAIN, self._network_id)},
            name=str(self._network_name),
            manufacturer="Cisco Meraki",
            model="Network",  # Generic model for network-level entities
        )

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return additional state attributes for the sensor."""
        attrs: Dict[str, Any] = {
            "network_id": self._network_id,
            "network_name": self._network_name,
            # Could add last_updated time here if managed manually
        }
        return attrs

    # The icon property was present in the original code.
    # It can be kept if dynamic icons are needed, or set as _attr_icon if static.
    # For this sensor, a static icon is likely sufficient.
    # @property
    # def icon(self) -> str:
    #     """Return the icon of the sensor."""
    #     return "mdi:account-multiple"
