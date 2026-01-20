"""Type definitions for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypedDict


@dataclass
class MerakiDevice:
    """Dataclass for a Meraki device."""

    serial: str
    name: str
    model: str
    mac: str
    lan_ip: str | None = None
    wan1_ip: str | None = None
    wan2_ip: str | None = None
    public_ip: str | None = None
    network_id: str | None = None
    status: str | None = None
    product_type: str | None = None
    tags: list[str] = field(default_factory=list)
    readings: list[dict[str, Any]] = field(default_factory=list)
    video_settings: dict[str, Any] | None = None
    rtsp_url: str | None = None
    sense_settings: dict[str, Any] | None = None
    ports_statuses: list[dict[str, Any]] = field(default_factory=list)
    dynamic_dns: dict[str, Any] | None = None
    status_messages: list[str] = field(default_factory=list)
    entity_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MerakiDevice":
        """Create a MerakiDevice instance from a dictionary."""
        return cls(
            serial=data.get("serial"),
            name=data.get("name"),
            model=data.get("model"),
            mac=data.get("mac"),
            lan_ip=data.get("lanIp"),
            wan1_ip=data.get("wan1Ip"),
            wan2_ip=data.get("wan2Ip"),
            public_ip=data.get("publicIp"),
            network_id=data.get("networkId"),
            status=data.get("status"),
            product_type=data.get("productType"),
            tags=data.get("tags", []),
        )


@dataclass
class MerakiNetwork:
    """Dataclass for a Meraki network."""

    id: str
    name: str
    organization_id: str
    product_types: list[str] = field(default_factory=list)
    time_zone: str | None = None
    tags: list[str] = field(default_factory=list)
    notes: str | None = None
    status_messages: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MerakiNetwork":
        """Create a MerakiNetwork instance from a dictionary."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            organization_id=data.get("organizationId"),
            product_types=data.get("productTypes", []),
            time_zone=data.get("timeZone"),
            tags=data.get("tags", []),
            notes=data.get("notes"),
        )


class MerakiVlan(TypedDict):
    """Represents a Meraki VLAN."""

    id: str
    name: str
    subnet: str | None
    applianceIp: str | None
    ipv6: dict | None


class MerakiFirewallRule(TypedDict):
    """Represents a Meraki L3 Firewall Rule."""

    comment: str
    policy: str
    protocol: str
    destPort: str
    destCidr: str
    srcPort: str
    srcCidr: str
    syslogEnabled: bool


class MerakiTrafficShaping(TypedDict):
    """Represents Meraki Traffic Shaping settings."""

    enabled: bool
    rules: list


class MerakiVpn(TypedDict):
    """Represents Meraki Site-to-Site VPN settings."""

    mode: str
    hubs: list
    subnets: list
