"""Base entity for Meraki VLANs."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ...const import DOMAIN
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

        # Set attributes needed for device_info BEFORE super().__init__
        # because BaseMerakiEntity.__init__ logs device_info
        self._vlan = vlan
        self._vlan_id = vlan["id"]
        self._vlan_data = vlan

        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            network=network,
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the VLAN."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self._network_id}vlan{self._vlan_id}")},
            name=f"[VLAN {self._vlan_id}] {self._vlan_data.get('name', '')}",
            via_device=(DOMAIN, f"network_{self._network_id}"),
            model="Virtual Local Area Network",
            manufacturer="Cisco Meraki",
        )
