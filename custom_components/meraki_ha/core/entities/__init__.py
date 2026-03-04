"""Base entity classes for the Meraki integration."""

import logging
from abc import ABC

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN, MANUFACTURER
from ...coordinators import MerakiMainCoordinator
from ..utils.naming_utils import standardize_device_name

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
        self._config_entry = config_entry
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
    def device_info(self) -> DeviceInfo | None:
        """Get device info for this entity."""
        # Handle network-based entities
        if self._network_id and not self._serial:
            network = self.coordinator.get_network(self._network_id)
            if network:
                return DeviceInfo(
                    identifiers={(DOMAIN, f"network_{self._network_id}")},
                    name=standardize_device_name(network.name),
                    manufacturer=MANUFACTURER,
                    model="Network",
                    sw_version="unknown",
                )

        # Handle device-based entities
        if self._serial:
            device = self.coordinator.get_device(self._serial)
            if device:
                model = device.model
                return DeviceInfo(
                    identifiers={(DOMAIN, self._serial)},
                    name=standardize_device_name(device.name),
                    manufacturer=MANUFACTURER,
                    model=model,
                    sw_version=device.firmware or "unknown",
                    suggested_area=device.address or "",
                    hw_version=model,
                    configuration_url=device.url
                    or f"https://dashboard.meraki.com/devices/{self._serial}",
                )

        return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # First check if coordinator has data
        if not self.coordinator.last_update_success:
            return False

        # For device-based entities, check device status
        if self._serial:
            device = self.coordinator.get_device(self._serial)
            return bool(device and device.status == "online")

        # For network-based entities, check network status
        if self._network_id:
            network = self.coordinator.get_network(self._network_id)
            return bool(network)

        return True
