"""Base entity for Meraki VLANs."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry

from ...coordinators import MerakiMainCoordinator
from ..models.network import MerakiVlan
from .meraki_network_entity import MerakiNetworkEntity


class MerakiVLANEntity(MerakiNetworkEntity):
    """Representation of a Meraki VLAN."""

    _attr_has_entity_name = True
    _attr_name: str | None = None

    def __init__(
        self,
        coordinator: MerakiMainCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        vlan: MerakiVlan,
    ) -> None:
        """Initialize the VLAN entity."""
        network = coordinator.get_network(network_id)
        if network is None:
            raise ValueError(f"Network {network_id} not found for VLAN entity")

        # Set attributes needed for logic
        self._vlan = vlan
        self._vlan_id = vlan.id
        self._vlan_name = vlan.name
        self._vlan_data = vlan

        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            network=network,
        )

    # Refactor: Removed device_info property to inherit from MerakiNetworkEntity
    # This automatically attaches VLAN entities to the Network Device
    # (Virtual Controller)
