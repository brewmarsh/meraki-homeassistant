"""Platform for Meraki device tracker integration in Home Assistant.

This module sets up device tracker entities for Meraki devices. Each
Meraki device (e.g., an access point) can be represented as a device
tracker, which can then be used to determine if any clients are
connected to it, effectively acting as a presence detection mechanism
for the device itself being "active" or having connected clients.
"""
from __future__ import annotations  # For type hints pre Python 3.9

import logging
from typing import Any, Dict, List, Optional  # Added List, Optional

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback  # Added callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
# Base class for coordinator entities
from homeassistant.helpers.update_coordinator import CoordinatorEntity

# Assuming MerakiDataUpdateCoordinator is the central coordinator for
# the Meraki integration and it's correctly defined in .coordinator
from .const import DATA_COORDINATOR, DOMAIN
from .coordinators import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki device tracker entities from a config entry.

    This function is called by Home Assistant to initialize device tracker
    entities based on the Meraki clients discovered by the central data
    update coordinator.

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry for this Meraki integration instance.
        async_add_entities: Callback function to add entities to Home Assistant.
    """
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        DATA_COORDINATOR
    ]

    # Ensure coordinator data is available
    if coordinator.data is None or "clients" not in coordinator.data:  # Ensure 'clients' key exists
        _LOGGER.warning(
            "No client data available from Meraki coordinator. Cannot set up device trackers."
        )
        return

    clients: List[Dict[str, Any]] = coordinator.data.get("clients", []) # Get clients list
    if not clients:
        _LOGGER.info("No Meraki clients found to set up device trackers.")
        return

    entities: List[MerakiDeviceTracker] = []
    for client_data in clients:
        # Ensure essential client data (e.g., MAC address) is present
        if "mac" not in client_data:
            _LOGGER.warning(
                "Skipping device tracker setup for client with missing MAC address: %s",
                client_data,
            )
            continue
        entities.append(MerakiDeviceTracker(coordinator, client_data))

    if entities:
        async_add_entities(entities)
        _LOGGER.info("Added %d Meraki client trackers.", len(entities))


class MerakiDeviceTracker(
    CoordinatorEntity[MerakiDataUpdateCoordinator], TrackerEntity
):
    """Representation of an individual client device connected to a Meraki network.

    This entity tracks the connectivity of a single client (e.g., a laptop,
    phone) by checking its presence in the Meraki coordinator's data.
    """

    # For Home Assistant 2022.11+ to use device name as base
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        client_info: Dict[str, Any],
    ) -> None:
        """Initialize the Meraki client device tracker.

        Args:
            coordinator: The `MerakiDataUpdateCoordinator` for data updates.
            client_info: A dictionary containing the client's
                         information, including 'mac', 'ip', 'description',
                         'ap_serial' (if connected to an AP), etc.
        """
        super().__init__(coordinator)  # Initialize CoordinatorEntity
        self._client_info_data: Dict[str, Any] = client_info
        # Name can be client's description or IP if description is not available
        self._attr_name = self._client_info_data.get(
            "description"
        ) or self._client_info_data.get("ip")
        self._attr_unique_id = f"{self._client_info_data['mac']}_client_tracker"

        # Initial update of attributes based on current data
        self._update_attributes()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_attributes()
        self.async_write_ha_state()

    def _update_attributes(self) -> None:
        """Update entity attributes based on coordinator data.

        This method checks if the current client (identified by MAC address)
        is present in the coordinator's list of active clients.
        """
        self._attr_is_connected = False  # Default to not connected
        client_mac = self._client_info_data["mac"]

        if self.coordinator.data and "clients" in self.coordinator.data:
            active_clients: List[Dict[str, Any]] = self.coordinator.data["clients"]
            for client_data in active_clients:
                if client_data.get("mac") == client_mac:
                    self._attr_is_connected = True
                    # Update client info if more details are available from active list
                    self._client_info_data.update(client_data) 
                    break
        
        _LOGGER.debug(
            "Client tracker %s (MAC: %s) is_connected: %s",
            self._attr_name,
            client_mac,
            self._attr_is_connected,
        )
        if not self._attr_is_connected:
             _LOGGER.debug( # More specific log if client not found in active list
                "Client tracker %s (MAC: %s) not found in coordinator's active client list.",
                self._attr_name,
                client_mac,
            )


    @property
    def source_type(self) -> SourceType:
        """Return the source type of the device tracker."""
        return SourceType.ROUTER # Client is tracked by the router/AP

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information for linking this entity to the parent Meraki device.

        This information is used by Home Assistant to correctly group
        entities and display device details in the UI.
        """
        # Link to the AP the client is connected to, or the network.
        # This assumes 'ap_serial' or 'network_id' is in _client_info_data
        # Default to network if AP serial is not present
        parent_identifier_value = self._client_info_data.get(
            "ap_serial"
        ) or self._client_info_data.get("networkId", "meraki_network")

        # Use client's description or IP as name, fallback to MAC
        entity_name = self._client_info_data.get(
            "description"
        ) or self._client_info_data.get("ip", self._client_info_data["mac"])

        return {
            "identifiers": {(DOMAIN, parent_identifier_value)},
            # No 'name', 'manufacturer', or 'model' for the parent device here
        }

    # Icon can be dynamic based on connection state
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return "mdi:lan-connect" if self._attr_is_connected else "mdi:lan-disconnect"
