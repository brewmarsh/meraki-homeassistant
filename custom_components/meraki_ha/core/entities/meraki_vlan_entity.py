"""Base entity for Meraki VLANs."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import DeviceInfo

from ...coordinator import MerakiDataUpdateCoordinator
from ...core.utils.naming_utils import format_device_name
from ...types import MerakiVlan
from . import BaseMerakiEntity


class MerakiVLANEntity(BaseMerakiEntity):
    """Representation of a Meraki VLAN."""

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
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

        vlan_id = vlan.get("id")
        if not vlan_id:
            raise ValueError("VLAN ID not found in VLAN data")
        self._attr_device_info = DeviceInfo(
            identifiers={(self._config_entry.domain, f"vlan_{network_id}_{vlan_id}")},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="VLAN",
            via_device=(self._config_entry.domain, f"network_{network_id}"),
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the device info."""
        return self._attr_device_info
