"""Base entity for Meraki VLANs."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry

from ...coordinator import MerakiDataUpdateCoordinator
from .meraki_network_entity import MerakiNetworkEntity


class MerakiVLANEntity(MerakiNetworkEntity):
    """Representation of a Meraki VLAN."""

    _attr_has_entity_name = False

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        vlan: dict,
    ) -> None:
        """Initialize the VLAN entity."""
        network = coordinator.get_network(network_id)
        if network is None:
            raise ValueError(f"Network {network_id} not found for VLAN entity")
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            network=network,
        )
        self._vlan = vlan

        vlan_id = vlan["id"]
        vlan_label = vlan.get("name") or ""
        self._attr_name = f"{network.name} VLAN {vlan_id} {vlan_label}"
