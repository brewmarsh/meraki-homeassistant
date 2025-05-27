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
from .coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Meraki device tracker entities from a config entry.

    This function is called by Home Assistant to initialize device tracker
    entities based on the Meraki devices discovered by the central data
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
    if coordinator.data is None or "devices" not in coordinator.data:
        _LOGGER.warning(
            "No device data available from Meraki coordinator. Cannot set up device trackers."
        )
        return

    devices: List[Dict[str, Any]] = coordinator.data.get("devices", [])
    if not devices:
        _LOGGER.info("No Meraki devices found to set up device trackers.")
        return

    entities: List[MerakiDeviceTracker] = []
    for device_data in devices:
        # Ensure essential device data (serial, model, name) is present
        if not all(k in device_data for k in ["serial", "model", "name"]):
            _LOGGER.warning(
                "Skipping device tracker setup for device with missing "
                "essential data: %s",
                device_data.get("serial", "Unknown Serial"),
            )
            continue
        entities.append(MerakiDeviceTracker(coordinator, device_data))

    if entities:
        async_add_entities(entities)
        _LOGGER.info("Added %d Meraki device trackers.", len(entities))


class MerakiDeviceTracker(
    CoordinatorEntity[MerakiDataUpdateCoordinator], TrackerEntity
):
    """Representation of a Meraki device as a Home Assistant device tracker.

    This entity tracks the "connectivity" or "activity" of a Meraki
    device (like an access point) by checking if it has any connected
    clients. It is not tracking individual clients, but rather the
    device itself.
    """

    # For Home Assistant 2022.11+ to use device name as base
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        device_info: Dict[str, Any],  # Renamed for clarity
    ) -> None:
        """Initialize the Meraki device tracker.

        Args:
            coordinator: The `MerakiDataUpdateCoordinator` for data updates.
            device_info: A dictionary containing the Meraki device's
                         information, including 'serial', 'name',
                         'model', etc.
        """
        super().__init__(coordinator)  # Initialize CoordinatorEntity
        self._device_info_data: Dict[str, Any] = device_info
        # Let HA generate from device name if _attr_has_entity_name is True
        self._attr_name = None
        # Or set explicitly:
        # self._attr_name = device_info["name"]
        self._attr_unique_id = (
            f"{self._device_info_data['serial']}_device_tracker"
        )

        # Initial update of attributes based on current data
        self._update_attributes()

    @callback  # For properties derived from coordinator data
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_attributes()
        self.async_write_ha_state()

    def _update_attributes(self) -> None:
        """Update entity attributes based on coordinator data.

        This method finds the current device's data from the
        coordinator's latest device list and updates the
        `is_connected` status.
        """
        # Find this specific device in the coordinator's latest data
        current_device_data: Optional[Dict[str, Any]] = None
        if self.coordinator.data and "devices" in self.coordinator.data:
            for dev_data in self.coordinator.data["devices"]:
                if dev_data.get("serial") == self._device_info_data["serial"]:
                    current_device_data = dev_data
                    break
        
        if current_device_data:
            # Assuming 'connected_clients_count' is populated by the
            # coordinator (e.g., by MerakiDeviceCoordinator) for MR/GR
            # devices. If not, this logic needs adjustment based on
            # available data. The original code checked
            # `len(meraki_device.get("clients")) > 0`.
            # Let's assume a field like 'connected_clients_count' exists
            # from prior processing.
            connected_clients_count: int = current_device_data.get(
                "connected_clients_count", 0
            )
            self._attr_is_connected = connected_clients_count > 0
            _LOGGER.debug(
                "Device tracker %s (%s) connected_clients_count: %d, "
                "is_connected: %s",
                self._device_info_data.get("name"),
                self._device_info_data["serial"],
                connected_clients_count,
                self._attr_is_connected,
            )
        else:
            _LOGGER.warning(
                "Device tracker %s (%s) could not find its data in "
                "coordinator update. Setting is_connected to False.",
                self._device_info_data.get("name"),
                self._device_info_data["serial"],
            )
            self._attr_is_connected = False

    # No need for a separate @property is_connected if _attr_is_connected
    # is set in _update_attributes and updated via _handle_coordinator_update.
    # If direct calculation is preferred over storing in _attr_is_connected:
    # @property
    # def is_connected(self) -> bool:
    #     """Return true if device has connected clients or is active."""
    #     # Find this specific device in coordinator's latest data
    #     if self.coordinator.data and "devices" in self.coordinator.data:
    #         for dev_data in self.coordinator.data["devices"]:
    #             if dev_data.get("serial") == self._device_info_data["serial"]:
    #                 # Logic based on 'connected_clients_count' or similar
    #                 return dev_data.get("connected_clients_count", 0) > 0
    #     return False  # Default to False if data not found

    @property
    def source_type(self) -> SourceType:
        """Return the source type of the device tracker (router/AP)."""
        # Indicates the device itself is a network device
        return SourceType.ROUTER

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information for linking this entity to the registry.

        This information is used by Home Assistant to correctly group
        entities and display device details in the UI.
        """
        return {
            "identifiers": {(DOMAIN, self._device_info_data["serial"])},
            "name": str(self._device_info_data["name"]),  # Ensure name is string
            "manufacturer": "Cisco Meraki",
            # Ensure model is string
            "model": str(self._device_info_data.get("model", "Unknown")),
            # Ensure sw_version is string
            "sw_version": str(self._device_info_data.get("firmware", "")),
            # If network is also a device
            # "via_device": (DOMAIN, self._device_info_data.get("networkId")),
        }

    # Potentially add other properties if needed, e.g., location,
    # battery_level (if applicable)
    # @property
    # def icon(self) -> str:
    #     """Return the icon to use in the frontend, if any."""
    #     return "mdi:router-wireless" if self.is_connected else "mdi:router-wireless-off"
