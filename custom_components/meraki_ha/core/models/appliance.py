"""Appliance models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(kw_only=True)
class MerakiAppliancePort:
    """Represents a Meraki Appliance Port."""

    number: int | None = None
    enabled: bool = False
    type: str | None = None
    drop_untagged_traffic: bool = False
    vlan: int | None = None
    access_policy: str | None = None
    allowed_vlans: str | None = None
    status: str | None = None
    speed: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "number": self.number,
            "enabled": self.enabled,
            "type": self.type,
            "dropUntaggedTraffic": self.drop_untagged_traffic,
            "vlan": self.vlan,
            "accessPolicy": self.access_policy,
            "allowedVlans": self.allowed_vlans,
            "status": self.status,
            "speed": self.speed,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiAppliancePort:
        """Create a MerakiAppliancePort instance from a dictionary."""
        return cls(
            number=data.get("number"),
            enabled=data.get("enabled", False),
            type=data.get("type"),
            drop_untagged_traffic=data.get("dropUntaggedTraffic", False),
            vlan=data.get("vlan"),
            access_policy=data.get("accessPolicy"),
            allowed_vlans=data.get("allowedVlans"),
            status=data.get("status"),
            speed=data.get("speed"),
        )


@dataclass(kw_only=True)
class MerakiApplianceMixin:
    """Mixin for Meraki Appliance specific fields."""

    appliance_uplink_statuses: list[dict[str, Any]] = field(default_factory=list)
    appliance_ports: list[MerakiAppliancePort] = field(default_factory=list)
    dynamic_dns: dict[str, Any] | None = None
