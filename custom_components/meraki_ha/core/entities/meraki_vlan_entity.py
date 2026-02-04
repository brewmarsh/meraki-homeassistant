"""Base entity for Meraki VLANs."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry

from ...coordinator import MerakiDataUpdateCoordinator
from .meraki_network_entity import MerakiNetworkEntity


class MerakiVLANEntity(MerakiNetworkEntity):
    """Representation of a Meraki VLAN."""

    _attr_has_entity_name = True

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
        prefix = f"VLAN {vlan_id}"
        if vlan_label:
            prefix = f"{prefix} {vlan_label}"

        current_name = getattr(self, "_attr_name", None)
        if current_name:
            self._attr_name = f"{prefix} {current_name}"
        else:
            self._attr_name = prefix
