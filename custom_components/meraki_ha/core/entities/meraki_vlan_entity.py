"""Base entity for Meraki VLANs."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from ...coordinator import MerakiDataUpdateCoordinator
from . import BaseMerakiEntity


class MerakiVLANEntity(BaseMerakiEntity):
    """Representation of a Meraki VLAN."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        vlan: dict,
    ) -> None:
        """Initialize the VLAN entity."""
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            network_id=network_id,
        )
        self._vlan = vlan
        if self._network_id is None:
            raise ValueError("Network ID cannot be None for a VLAN entity")
        if self._network is None:
            raise ValueError(f"Network {self._network_id} not found for VLAN entity")

        # Handle vlan as a dictionary
        vlan_id = vlan["id"]

        if not vlan_id:
            raise ValueError("VLAN ID not found in VLAN data")

        vlan_label = vlan.get("name") or ""
        device_name = f"{self._network.name} VLAN {vlan_id}"
        if vlan_label:
            device_name += f" {vlan_label}"

        self._attr_device_info = DeviceInfo(
            identifiers={(self._config_entry.domain, f"vlan_{network_id}_{vlan_id}")},
            name=device_name,
            manufacturer="Cisco Meraki",
            model="VLAN",
            via_device=(self._config_entry.domain, f"network_{network_id}"),
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return self._attr_device_info
