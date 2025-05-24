"""Sensor entity for monitoring the client count on a Meraki network.

This module defines the `MerakiNetworkClientCountSensor`, a Home Assistant
sensor entity that displays the total number of clients connected to a
specific Meraki network within the last 24 hours.
"""
import logging # Added logging
from typing import Any, Dict, Optional # Added for type hinting

from homeassistant.components.sensor import SensorEntity, SensorStateClass
# Assuming get_network_clients_count is part of the Meraki API client library
# and coordinator is MerakiDataUpdateCoordinator
from ..meraki_api.networks import get_network_clients_count
from ..coordinator import MerakiDataUpdateCoordinator # For type hinting

_LOGGER = logging.getLogger(__name__)


class MerakiNetworkClientCountSensor(SensorEntity):
    """Represents a sensor for the total number of clients on a Meraki network.

    This sensor fetches the count of clients seen on a specific Meraki network
    over the past 24 hours. It makes a direct API call via `get_network_clients_count`
    during its `async_update` cycle, rather than relying on pre-fetched data
    from the coordinator that might be aggregated across all networks.

    Attributes:
        _coordinator (MerakiDataUpdateCoordinator): The data update coordinator,
            used here primarily to access the API key.
        _network_id (str): The ID of the Meraki network this sensor monitors.
        _network_name (str): The name of the Meraki network.
        _attr_name (str): The friendly name of the sensor in Home Assistant.
        _attr_unique_id (str): The unique ID for this sensor entity.
        _attr_native_value (Optional[int]): The current value (client count).
        _attr_icon (str): The icon for the sensor.
        _attr_state_class (SensorStateClass): The state class ("measurement").
        _attr_native_unit_of_measurement (str): Unit of measurement ("clients").
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        network_id: str,
        network_name: str,
    ) -> None:
        """Initializes the Meraki Network Client Count sensor.

        Args:
            coordinator (MerakiDataUpdateCoordinator): The main data coordinator,
                used here to access shared information like the API key.
            network_id (str): The unique identifier of the Meraki network.
            network_name (str): The human-readable name of the Meraki network.
        """
        self._coordinator = coordinator # Store the coordinator instance
        self._network_id = network_id
        self._network_name = network_name

        # Set Home Assistant entity attributes
        self._attr_name = f"{network_name} Total Clients (24h)"
        self._attr_unique_id = f"meraki_network_clients_{network_id}"
        self._attr_icon = "mdi:account-group" # Icon representing a group of users/clients
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "clients"
        self._attr_native_value: Optional[int] = None # Initialize native_value

        _LOGGER.debug(
            "Meraki Network Client Count Sensor initialized for network '%s' (ID: %s)",
            network_name,
            network_id,
        )

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity-specific state attributes."""
        return {
            "network_id": self._network_id,
            "network_name": self._network_name,
        }

    async def async_update(self) -> None:
        """Fetches the latest client count for the network.

        This method is called periodically by Home Assistant to update the
        sensor's state. It makes a direct API call to get the current count
        of clients on this specific network.
        """
        _LOGGER.debug(
            "Updating client count for Meraki network: %s (ID: %s)",
            self._network_name,
            self._network_id,
        )
        try:
            # Fetch the client count using the dedicated API function.
            # This makes a direct API call specific to this network's client count.
            client_count = await get_network_clients_count(
                self._coordinator.api_key,  # Access API key from the coordinator
                self._network_id,
            )
            if client_count is not None:
                self._attr_native_value = client_count
                _LOGGER.debug(
                    "Successfully updated client count for network %s to: %s",
                    self._network_name,
                    self._attr_native_value,
                )
            else:
                # Handle cases where client_count might be None (e.g., API error handled in get_network_clients_count)
                _LOGGER.warning(
                    "Received None for client count for network %s. Retaining previous value or setting to None.",
                    self._network_name,
                )
                # Optionally set to None or a specific error value if preferred
                # self._attr_native_value = None
        except Exception as e:
            # Catch any other unexpected errors during the update.
            _LOGGER.error(
                "Error updating client count for Meraki network %s: %s",
                self._network_name,
                e,
            )
            # Optionally set value to None or unavailable on error
            self._attr_native_value = None
        # self.async_write_ha_state() # Not needed here as HA handles it after async_update
