"""Sensors for Meraki VLANs."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory

from ...coordinator import MerakiDataUpdateCoordinator
from ...core.entities.meraki_vlan_entity import MerakiVLANEntity
from ...core.utils.entity_id_utils import get_vlan_entity_id

_LOGGER = logging.getLogger(__name__)


class MerakiVLANStatusSensor(MerakiVLANEntity, SensorEntity):
    """Representation of a Meraki VLAN Status sensor."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: MerakiDataUpdateCoordinator,
        config_entry: ConfigEntry,
        network_id: str,
        vlan: dict,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, network_id, vlan)
        if not self._network_id:
            raise ValueError("Network ID cannot be None for a VLAN entity")
        vlan_id = self._vlan["id"]
        vlan_name = self._vlan.get("name", "")

        # Unique ID
        self._attr_unique_id = get_vlan_entity_id(self._network_id, vlan_id, "status")

        # Name: VLAN 10 (Staff) Subnet
        if vlan_name:
             self._attr_name = f"VLAN {vlan_id} ({vlan_name}) Subnet"
        else:
             self._attr_name = f"VLAN {vlan_id} Subnet"

    @property
    def native_value(self) -> str | None:
        """Return the subnet (CIDR)."""
        return self._vlan.get("subnet")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "vlan_id": self._vlan.get("id"),
            "name": self._vlan.get("name"),
            "appliance_ip": self._vlan.get("applianceIp"),
            "ipv6_enabled": self._vlan.get("ipv6", {}).get("enabled", False),
            "ipv6_prefix": self._vlan.get("ipv6", {}).get("prefix"),
            "dns_nameservers": self._vlan.get("dnsNameservers"),
            "dhcp_handling": self._vlan.get("dhcpHandling"),
            "dhcp_lease_time": self._vlan.get("dhcpLeaseTime"),
            "dhcp_boot_options_enabled": self._vlan.get("dhcpBootOptionsEnabled", False),
        }
