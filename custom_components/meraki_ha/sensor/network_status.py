"""Sensor platform for Meraki network status, specifically client counts.

Note: This module appears to duplicate functionality found in
`network_clients.py` regarding `MerakiNetworkClientCountSensor`.
Consider refactoring or removing this module if it's redundant.

This module defines a sensor to display the number of clients connected
to a Meraki network over the last 24 hours.
"""
import logging
from typing import Any, Dict, List, Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from ..const import DOMAIN
# Assuming MerakiDataUpdateCoordinator is the type of coordinator used.
from ..coordinator import MerakiDataUpdateCoordinator
from ..meraki_api.networks import get_meraki_networks, get_network_clients_count

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki network client count sensors from a config entry.

    This function retrieves network information using the main data coordinator
    and then creates a `MerakiNetworkClientCountSensor` for each discovered network.

    Note: This setup logic is very similar to what might be expected in
    `sensor/__init__.py` for network-wide sensors or in `network_clients.py`.
    If `network_clients.py`'s sensor is added via `sensor/__init__.py`,
    this `async_setup_entry` might lead to duplicate sensors or conflicts.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        config_entry (ConfigEntry): The configuration entry for this Meraki
            integration instance.
        async_add_entities (AddEntitiesCallback): Callback function to add
            entities to Home Assistant.
    """

    async def _get_network_ids_and_names(
        api_key: str, org_id: str
    ) -> Optional[List[Dict[str, str]]]:
        """Helper to retrieve network IDs and names from Meraki API.

        This makes a direct API call. In a coordinator-based pattern, this data
        might already be available via the coordinator.

        Args:
            api_key (str): The Meraki API key.
            org_id (str): The Meraki organization ID.

        Returns:
            Optional[List[Dict[str, str]]]: A list of network dicts (id, name)
                or None if fetching fails.
        """
        try:
            networks_raw = await get_meraki_networks(api_key, org_id)
            if networks_raw is None:
                _LOGGER.warning("get_meraki_networks returned None, cannot extract IDs and names.")
                return None
            # Ensure each item is a dictionary and has 'id' and 'name'
            return [
                {"id": net["id"], "name": net["name"]}
                for net in networks_raw
                if isinstance(net, dict) and "id" in net and "name" in net
            ]
        except Exception as e:
            _LOGGER.error("Error fetching networks for IDs and names: %s", e)
            return None

    _LOGGER.debug(
        "async_setup_entry in sensor_network_status.py called. "
        "Note potential redundancy with network_clients.py."
    )

    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    # Fetch network information.
    networks = await _get_network_ids_and_names(
        coordinator.api_key, coordinator.org_id
    )

    if networks:
        entities = [
            MerakiNetworkClientCountSensor(coordinator, network["id"], network["name"])
            for network in networks # Relies on _get_network_ids_and_names filtering malformed entries
        ]
        if entities:
            async_add_entities(entities)
            _LOGGER.info("Added %d Meraki network client count sensors (from network_status.py).", len(entities))
        else:
            _LOGGER.info("No network client count sensors created (from network_status.py), networks list might have been empty or malformed after processing.")
    else:
        _LOGGER.warning(
            "Failed to retrieve Meraki networks for client count sensor setup (from network_status.py)."
        )


class MerakiNetworkClientCountSensor(SensorEntity):
    """Represents a sensor for Meraki network client count (24h).

    This sensor displays the number of unique clients seen on a specific
    Meraki network in the last 24 hours.

    Note: This class is very similar, if not identical, to the one defined in
    `network_clients.py`. This could lead to issues if both are registered.

    Attributes:
        _coordinator (MerakiDataUpdateCoordinator): The main data coordinator, used
            here to access the API key for direct API calls.
        _network_id (str): The ID of the Meraki network.
        _network_name (str): The name of the Meraki network.
        _attr_name (str): Friendly name of the sensor.
        _attr_unique_id (str): Unique ID of the sensor.
        _attr_native_value (Optional[int]): The current client count.
        _attr_state_class (SensorStateClass): State class of the sensor.
        _attr_native_unit_of_measurement (str): Unit of measurement.
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        network_id: str,
        network_name: str,
    ) -> None:
        """Initializes the Meraki Network Client Count sensor.

        Args:
            coordinator (MerakiDataUpdateCoordinator): The data coordinator.
            network_id (str): The ID of the Meraki network.
            network_name (str): The name of the Meraki network.
        """
        self._coordinator = coordinator
        self._network_id = network_id
        self._network_name = network_name
        # Setting entity attributes
        self._attr_name = f"{network_name} Clients (24h)"
        self._attr_unique_id = f"{DOMAIN}_{network_id}_clients_24h" # Ensure DOMAIN is part of unique_id for clarity
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "clients"
        self._attr_native_value: Optional[int] = None # Initialize

        _LOGGER.debug(
            "MerakiNetworkClientCountSensor (network_status.py version) initialized for network '%s' (ID: %s)",
            network_name,
            network_id,
        )


    async def async_update(self) -> None:
        """Fetches the latest client count for the network.

        This method is called periodically by Home Assistant to update the
        sensor's state. It makes a direct API call to get the current count
        of clients on this specific network.
        """
        _LOGGER.debug(
            "Updating client count for network %s (ID: %s) via network_status.py sensor",
            self._network_name,
            self._network_id,
        )
        try:
            client_count = await get_network_clients_count(
                self._coordinator.api_key, self._network_id
            )
            if client_count is not None:
                self._attr_native_value = client_count
            else:
                # If API returns None (e.g. error handled in get_network_clients_count)
                _LOGGER.warning("Received None for client count for network %s.", self._network_name)
                self._attr_native_value = None # Explicitly set to None
        except Exception as e:
            _LOGGER.error(
                "Error updating client count for network %s (network_status.py): %s",
                self._network_name,
                e,
            )
            self._attr_native_value = None # Set to None on error
        # async_write_ha_state() is called by SensorEntity base class after async_update.

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend for this sensor."""
        return "mdi:account-multiple" # Changed icon for differentiation if both are loaded

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity-specific state attributes."""
        return {
            "network_id": self._network_id,
            "network_name": self._network_name,
            "source_file": __file__, # To help identify if this sensor is active
        }
