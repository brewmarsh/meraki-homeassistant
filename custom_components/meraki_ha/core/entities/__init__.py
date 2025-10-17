"""Base entity classes for the Meraki integration."""

from abc import ABC
from typing import Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import (
    DOMAIN,
    MANUFACTURER,
)
from ..coordinators import MerakiDataUpdateCoordinator
from ..utils.naming_utils import format_device_name


class BaseMerakiEntity(CoordinatorEntity[MerakiDataUpdateCoordinator], Entity, ABC):
    """Base entity class for Meraki entities.

    Provides common functionality for all Meraki entities including:
    - Device info management
    - State availability tracking
    - Common properties and attributes
    """

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        serial: Optional[str] = None,
        network_id: Optional[str] = None,
    ) -> None:
        """Initialize the entity.

        Args:
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

    @property
    def device_info(self) -> Optional[DeviceInfo]:
        """Get device info for this entity."""
        # Handle network-based entities
        if self._network_id and not self._serial:
            network = self.coordinator.networks_by_id.get(self._network_id)
            if network:
                return DeviceInfo(
                    identifiers={(DOMAIN, f"network_{self._network_id}")},
                    name=format_device_name(network, self._config_entry.options),
                    manufacturer=MANUFACTURER,
                    model="Network",
                    sw_version=network.get("firmware", "unknown"),
                )

        # Handle device-based entities
        if self._serial:
            device = self.coordinator.devices_by_serial.get(self._serial)
            if device:
                model = device.get("model", "unknown")
                return DeviceInfo(
                    identifiers={(DOMAIN, self._serial)},
                    name=format_device_name(device, self._config_entry.options),
                    manufacturer=MANUFACTURER,
                    model=model,
                    sw_version=device.get("firmware", "unknown"),
                    suggested_area=device.get("address", ""),
                    hw_version=model,
                    configuration_url=f"https://dashboard.meraki.com/devices/{self._serial}",
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
            device = self.coordinator.devices_by_serial.get(self._serial)
            return bool(device and device.get("status") == "online")

        # For network-based entities, check network status
        if self._network_id:
            network = self.coordinator.networks_by_id.get(self._network_id)
            return bool(network)

        return True

    @property
    def entity_category(self) -> Optional[EntityCategory]:
        """Return the entity category."""
        return None  # Override in child classes if needed
