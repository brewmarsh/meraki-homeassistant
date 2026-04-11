"""Base entity classes for the Meraki integration."""

import logging
from abc import ABC
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinators import MerakiMainCoordinator
from ...helpers.device_info_helpers import resolve_device_info

_LOGGER = logging.getLogger(__name__)


class BaseMerakiEntity(CoordinatorEntity, Entity, ABC):
    """
    Base entity class for Meraki entities.

    Provides common functionality for all Meraki entities including:
    - Device info management
    - State availability tracking
    - Common properties and attributes
    """

    coordinator: MerakiMainCoordinator
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        config_entry: ConfigEntry,
        serial: str | None = None,
        network_id: str | None = None,
    ) -> None:
        """
        Initialize the entity.

        Args:
        ----
            coordinator: The data coordinator
            config_entry: The config entry
            serial: Device serial number (if this is a device-based entity)
            network_id: Network ID (if this is a network-based entity)

        """
        super().__init__(coordinator)
        self._serial = serial
        self._network_id = network_id
        self._attr_has_entity_name = True
        self._network = self.coordinator.get_network(network_id) if network_id else None
        _LOGGER.debug(
            "Naming Debug - Entity: %s | Class: %s | has_entity_name: %s "
            "| _attr_name: %s | Device Identifiers: %s",
            self.entity_id if hasattr(self, "entity_id") else "New Entity",
            self.__class__.__name__,
            getattr(self, "_attr_has_entity_name", "Not Set"),
            getattr(self, "_attr_name", "None"),
            self.device_info.get("identifiers")
            if self.device_info
            else "NO DEVICE INFO",
        )

    @property
    def device_data(self) -> Any | None:
        """Get the updated device data from the God dictionary."""
        if not self.coordinator.data or not self._serial:
            return None
        devices_map = self.coordinator.data.get("devices_by_serial")
        if not isinstance(devices_map, dict):
            return None
        return devices_map.get(self._serial)

    @property
    def network_data(self) -> Any | None:
        """Get the updated network data from the God dictionary."""
        if not self.coordinator.data or not self._network_id:
            return None
        networks_map = self.coordinator.data.get("networks_by_id")
        if not isinstance(networks_map, dict):
            return None
        return networks_map.get(self._network_id)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Get device info for this entity."""
        # Handle network-based entities
        if self._network_id and not self._serial:
            network = self.network_data
            if network:
                return resolve_device_info(network, self.coordinator.config_entry)

        # Handle device-based entities
        if self._serial:
            device = self.device_data
            if device:
                return resolve_device_info(device, self.coordinator.config_entry)

        return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # First check if coordinator has data
        if self.coordinator.data is None or not self.coordinator.last_update_success:
            return False

        # For device-based entities, check device status
        if self._serial:
            device = self.device_data
            if not device:
                return False
            if hasattr(device, "is_online"):
                return bool(device.is_online)
            # Fallback for dictionary-style data
            status = device.get("status", "offline")
            return str(status).lower() in ("online", "alerting", "dormant")

        # For network-based entities, check network status
        if self._network_id:
            network = self.network_data
            return bool(network)

        return True
