"""Base entity for Meraki Networks."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...const import DOMAIN
from ...meraki_data_coordinator import MerakiDataCoordinator
from ...types import MerakiNetwork
from ..utils.naming_utils import format_device_name


class MerakiNetworkEntity(CoordinatorEntity):  # type: ignore[type-arg]
    """Representation of a Meraki Network."""

    coordinator: MerakiDataCoordinator

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network: MerakiNetwork,
    ) -> None:
        """Initialize the network entity."""
        super().__init__(coordinator=coordinator)
        self._config_entry = config_entry
        self._network = network
        self._network_id = network["id"]

        device_data_for_naming = {**network, "productType": "network"}
        formatted_name = format_device_name(
            device=device_data_for_naming,
            config=config_entry.options,
        )
        # Link network to its parent organization
        # Hierarchy: Organization → Network → Devices/VLANs/Clients
        org_id = network.get("organizationId")
        device_info = DeviceInfo(
            identifiers={(DOMAIN, f"network_{network['id']}")},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="Network",
        )
        if org_id:
            device_info["via_device"] = (DOMAIN, f"org_{org_id}")
        self._attr_device_info = device_info

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return self._attr_device_info
