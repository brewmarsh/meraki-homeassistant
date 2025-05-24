"""Device tracker platform for the Meraki Home Assistant integration.

This module defines `MerakiDeviceTracker` entities, which represent
Meraki network devices (like APs, switches, security appliances) and their
connectivity status within Home Assistant. The "connected" status in this
context seems to indicate if the Meraki device itself has any clients connected
to it, rather than tracking individual client devices.
"""
from __future__ import annotations # Ensures compatibility with type hints

import logging
from typing import Any, Dict, Optional # Added Optional

from homeassistant.components.device_tracker import (
    SourceType, # Standard HA source type for device trackers
    TrackerEntity, # Base class for device tracker entities
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback # Added callback for HA methods
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity # For coordinator integration

from .const import DOMAIN, DATA_COORDINATOR # Core constants
from .coordinator import MerakiDataUpdateCoordinator # Specific coordinator type

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Sets up Meraki device tracker entities from a config entry.

    This function is called by Home Assistant when a Meraki config entry is
    set up for the device_tracker platform. It retrieves the central data
    coordinator and iterates through the Meraki devices reported by the
    coordinator. For each Meraki device with a model specified, it creates a
    `MerakiDeviceTracker` entity.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        config_entry (ConfigEntry): The configuration entry for this Meraki
            integration instance.
        async_add_entities (AddEntitiesCallback): Callback function to add
            entities to Home Assistant.
    """
    _LOGGER.info("Setting up Meraki device tracker entities.")
    coordinator: MerakiDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        DATA_COORDINATOR
    ]

    # Ensure coordinator data is available.
    if not coordinator.data or "devices" not in coordinator.data:
        _LOGGER.warning(
            "Coordinator data is not available or does not contain 'devices'. "
            "Cannot set up Meraki device trackers."
        )
        return

    devices_data = coordinator.data.get("devices", [])
    if not isinstance(devices_data, list):
        _LOGGER.error("Expected 'devices' in coordinator data to be a list, but got %s.", type(devices_data))
        return


    entities_to_add: list[MerakiDeviceTracker] = []
    for device_info in devices_data:
        if not isinstance(device_info, dict):
            _LOGGER.warning("Skipping non-dictionary device item: %s", device_info)
            continue

        # A model is essential for identifying the device type.
        if device_info.get("model") is not None and device_info.get("serial") is not None:
            _LOGGER.debug(
                "Creating MerakiDeviceTracker for device: %s (Serial: %s, Model: %s)",
                device_info.get("name", "N/A"),
                device_info.get("serial"),
                device_info.get("model"),
            )
            entities_to_add.append(MerakiDeviceTracker(coordinator, device_info))
        else:
            _LOGGER.debug(
                "Skipping device tracker creation for device due to missing model or serial: %s",
                device_info.get("name", device_info.get("serial", "Unknown")),
            )

    if entities_to_add:
        async_add_entities(entities_to_add)
        _LOGGER.info("Added %d Meraki device tracker entities.", len(entities_to_add))
    else:
        _LOGGER.info("No Meraki device tracker entities were added.")


class MerakiDeviceTracker(CoordinatorEntity[MerakiDataUpdateCoordinator], TrackerEntity):
    """Represents a Meraki network device as a Home Assistant device tracker.

    This entity tracks the "connectivity" of a Meraki device (e.g., AP, switch, MX).
    The `is_connected` property determines its state, which seems to be based on
    whether the Meraki device itself has any clients connected to *it*, rather than
    tracking specific end-user client devices.

    Attributes:
        _device_info_dict (Dict[str, Any]): Raw information about the Meraki device
            this entity represents, obtained from the coordinator.
        _attr_name (str): The friendly name of the device tracker entity.
        _attr_unique_id (str): The unique ID for this entity.
        _attr_is_connected (bool): The current connected state of the tracker.
    """

    # Define _attr_has_entity_name = True if the name is derived from device_info
    # and you don't want Home Assistant to prefix it with the integration name.
    # However, for device trackers, the name is often the device name directly.
    # _attr_has_entity_name = True # Uncomment if desired, and adjust _attr_name if needed.

    def __init__(
        self, coordinator: MerakiDataUpdateCoordinator, device_info_dict: Dict[str, Any]
    ) -> None:
        """Initializes the Meraki device tracker.

        Args:
            coordinator (MerakiDataUpdateCoordinator): The data update coordinator.
            device_info_dict (Dict[str, Any]): A dictionary containing information
                about the Meraki device (e.g., "name", "serial", "model").
        """
        super().__init__(coordinator) # Initialize CoordinatorEntity
        self._device_info_dict = device_info_dict
        device_name = device_info_dict.get("name", device_info_dict.get("serial", "Unknown Meraki Device"))
        device_serial = device_info_dict.get("serial", "unknown_serial_tracker")

        self._attr_name = device_name # Directly use device name for tracker entity name
        self._attr_unique_id = f"{device_serial}_tracker"
        # Initial connected state is determined by _update_state() called by _handle_coordinator_update on init.
        self._attr_is_connected: bool = False # Default to False, will be updated.
        self._update_state() # Set initial state

        _LOGGER.debug(
            "MerakiDeviceTracker initialized: %s (Unique ID: %s)",
            self._attr_name,
            self._attr_unique_id,
        )

    def _update_state(self) -> None:
        """Updates the `is_connected` status of the device tracker.

        The "connected" status is determined by checking if the coordinator's data
        for this Meraki device indicates any connected clients.
        """
        new_is_connected = False # Assume not connected by default
        device_serial = self._device_info_dict.get("serial")

        if self.coordinator.data and "devices" in self.coordinator.data:
            current_device_data_from_coord = next(
                (
                    dev
                    for dev in self.coordinator.data["devices"]
                    if isinstance(dev, dict) and dev.get("serial") == device_serial
                ),
                None,
            )

            if current_device_data_from_coord:
                # The 'connected_clients' key (or similar like 'connected_clients_raw')
                # is expected to be populated by a coordinator (e.g., MerakiDeviceCoordinator).
                # This needs to be consistent with how client data is stored.
                # The original code checked `meraki_device.get("clients")`.
                # Adjusting to `connected_clients_raw` or `connected_clients` based on device_coordinator.py
                client_list = current_device_data_from_coord.get("connected_clients_raw") # Or "connected_clients" count
                if client_list is not None: # Could be an empty list or a count (int)
                    if isinstance(client_list, list):
                        new_is_connected = len(client_list) > 0
                    elif isinstance(client_list, int): # If it's a count
                        new_is_connected = client_list > 0
                    else:
                        _LOGGER.warning("Unexpected type for client data of device %s: %s", device_serial, type(client_list))

                _LOGGER.debug(
                    "Device %s client data: %s, IsConnected: %s",
                    device_serial,
                    client_list if client_list is not None else "N/A",
                    new_is_connected,
                )
            else:
                _LOGGER.debug("Device %s not found in coordinator data for state update.", device_serial)
        else:
            _LOGGER.debug("Coordinator data or 'devices' key unavailable for device tracker %s.", self.name)

        if self._attr_is_connected != new_is_connected:
            self._attr_is_connected = new_is_connected
            _LOGGER.debug("Device tracker %s connection state changed to: %s", self.name, self._attr_is_connected)


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handles updates from the data coordinator.
        This method is called whenever the coordinator has new data.
        """
        self._update_state() # Recalculate and update the state
        self.async_write_ha_state() # Persist the new state to Home Assistant
        _LOGGER.debug("MerakiDeviceTracker %s updated via coordinator.", self.name)


    @property
    def is_connected(self) -> bool:
        """Return True if the Meraki device is considered 'connected'.

        "Connected" here implies that the Meraki device itself has active clients,
        not necessarily that the device tracker entity (representing a person/phone)
        is connected to this Meraki device.
        """
        return self._attr_is_connected

    @property
    def source_type(self) -> SourceType:
        """Return the source type, typically `SourceType.ROUTER` for network gear."""
        return SourceType.ROUTER # Indicates the tracker is based on router/AP data

    @property
    def device_info(self) -> Optional[Dict[str, Any]]:
        """Return device information to link this entity to a Home Assistant device.

        This ensures the device tracker entity is associated with the correct
        Meraki device entry in the Home Assistant device registry.
        """
        device_serial = self._device_info_dict.get("serial")
        if not device_serial:
            return None # Cannot form identifiers without a serial

        return {
            "identifiers": {(DOMAIN, device_serial)},
            # Name, model, etc., are already part of the device registry entry
            # created by a coordinator (e.g., MerakiDeviceCoordinator).
            # This association links the entity to that existing device entry.
            # No need to repeat name, model, manufacturer here if already registered.
        }

    # Other properties like `latitude`, `longitude`, `mac_address`, `host_name`
    # could be implemented if relevant for this type of device tracker.
    # For a tracker representing the Meraki device itself, these might not be applicable
    # or would be static. If this were tracking a *client* device, they'd be more relevant.
    # For now, only essential TrackerEntity properties are implemented.
