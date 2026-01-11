"""Base entity for Meraki VLANs."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from ...const import DOMAIN
from ...core.utils.naming_utils import format_device_name
from ...meraki_data_coordinator import MerakiDataCoordinator
from ...types import MerakiVlan
from . import BaseMerakiEntity


class MerakiVLANEntity(BaseMerakiEntity):
    """Representation of a Meraki VLAN.

    Device Hierarchy: Organization → Network → VLANs Group → VLAN
    """

    def __init__(
        self,
        coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        vlan: MerakiVlan,
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
        vlan_device_data = {**vlan, "productType": "vlan"}
        formatted_name = format_device_name(
            device=vlan_device_data,
            config=self._config_entry.options,
        )

        # Link VLAN to its VLANs group (under network)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"vlan_{network_id}_{vlan['id']}")},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="VLAN",
            via_device=(DOMAIN, f"devicetype_{network_id}_vlans"),
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return self._attr_device_info
