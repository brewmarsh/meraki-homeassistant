"""Base entity classes for the Meraki integration."""

from abc import ABC

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import (
    DOMAIN,
    MANUFACTURER,
)
from ...meraki_data_coordinator import MerakiDataCoordinator
from ..utils.naming_utils import format_device_name


class BaseMerakiEntity(CoordinatorEntity, Entity, ABC):  # type: ignore[type-arg]
    """
    Base entity class for Meraki entities.

    Provides common functionality for all Meraki entities including:
    - Device info management
    - State availability tracking
    - Common properties and attributes
    """

    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
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

    @property
    def device_info(self) -> DeviceInfo | None:
        """Get device info for this entity.

        Device Hierarchy:
        - Organization (top-level hub)
          - Network (under organization)
            - Device Type Group (Access Points, Switches, etc.)
              - Devices (under device type group)
            - Clients (under network)
        """
        # Handle network-based entities (linked to organization)
        if self._network_id and not self._serial:
            network = self.coordinator.get_network(self._network_id)
            if network:
                firmware = network.get("firmware")
                org_id = network.get("organizationId")
                device_info = DeviceInfo(
                    identifiers={(DOMAIN, f"network_{self._network_id}")},
                    name=format_device_name(network, self._config_entry.options),
                    manufacturer=MANUFACTURER,
                    model="Network",
                    sw_version=str(firmware) if firmware else None,
                )
                # Link network to its parent organization
                if org_id:
                    device_info["via_device"] = (DOMAIN, f"org_{org_id}")
                return device_info

        # Handle device-based entities (linked to device type group)
        if self._serial:
            device = self.coordinator.get_device(self._serial)
            if device:
                model = str(device.get("model", "unknown"))
                firmware = device.get("firmware")
                address = device.get("address")
                network_id = device.get("networkId")
                product_type = device.get("productType")
                device_info = DeviceInfo(
                    identifiers={(DOMAIN, self._serial)},
                    name=format_device_name(device, self._config_entry.options),
                    manufacturer=MANUFACTURER,
                    model=model,
                    sw_version=str(firmware) if firmware else None,
                    suggested_area=str(address) if address else None,
                    hw_version=model,
                    configuration_url=f"https://dashboard.meraki.com/devices/{self._serial}",
                )
                # Link device to its device type group (if product type known)
                # Otherwise fall back to linking directly to network
                if network_id and product_type:
                    device_info["via_device"] = (
                        DOMAIN,
                        f"devicetype_{network_id}_{product_type}",
                    )
                elif network_id:
                    device_info["via_device"] = (DOMAIN, f"network_{network_id}")
                return device_info

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
            return bool(device and device.get("status") == "online")

        # For network-based entities, check network status
        if self._network_id:
            network = self.coordinator.get_network(self._network_id)
            return bool(network)

        return True

    @property
    def entity_category(self) -> EntityCategory | None:
        """Return the entity category."""
        return None  # Override in child classes if needed
