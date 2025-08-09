"""Base entity for Meraki VLANs."""
from __future__ import annotations

from typing import Any

from homeassistant.helpers.entity import DeviceInfo

from homeassistant.config_entries import ConfigEntry
from . import BaseMerakiEntity


class MerakiVLANEntity(BaseMerakiEntity):
    """Representation of a Meraki VLAN."""

    def __init__(
        self,
        coordinator: "MerakiDataCoordinator",
        config_entry: ConfigEntry,
        network_id: str,
        vlan: dict[str, Any],
    ) -> None:
        """Initialize the VLAN entity."""
        super().__init__(
            coordinator=coordinator,
            config_entry=config_entry,
            network_id=network_id,
        )
        self._vlan = vlan
        from ...core.utils.naming_utils import format_device_name

        vlan_device_data = {**vlan, "productType": "vlan"}
        formatted_name = format_device_name(
            device=vlan_device_data,
            config=config_entry.options,
        )

        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.domain, f"vlan_{network_id}_{vlan['id']}")},
            name=formatted_name,
            manufacturer="Cisco Meraki",
            model="VLAN",
            via_device=(coordinator.domain, f"network_{network_id}"),
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self._attr_device_info
