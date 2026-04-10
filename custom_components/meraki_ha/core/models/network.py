"""Network models for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MerakiNetwork:
    """Dataclass for a Meraki network."""

    id: str | None = None
    name: str | None = None
    organization_id: str | None = None
    product_types: list[str] = field(default_factory=list)
    time_zone: str | None = None
    tags: list[str] = field(default_factory=list)
    notes: str | None = None
    status_messages: list[str] = field(default_factory=list)
    is_enabled: bool = True
    ssids: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "organizationId": self.organization_id,
            "productTypes": self.product_types,
            "timeZone": self.time_zone,
            "tags": self.tags,
            "notes": self.notes,
            "is_enabled": self.is_enabled,
            "ssids": self.ssids,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiNetwork:
        """Create a MerakiNetwork instance from a dictionary."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            organization_id=data.get("organizationId"),
            product_types=data.get("productTypes", []),
            time_zone=data.get("timeZone"),
            tags=data.get("tags", []),
            notes=data.get("notes"),
            is_enabled=data.get("is_enabled", True),
            ssids=data.get("ssids", []),
        )


@dataclass
class MerakiVlan:
    """Represents a Meraki VLAN."""

    id: str | None = None
    name: str | None = None
    subnet: str | None = None
    appliance_ip: str | None = None
    ipv6: dict | None = None
    dhcp_handling: str | None = None
    dns_nameservers: str | None = None
    dhcp_lease_time: str | None = None
    dhcp_boot_options_enabled: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiVlan:
        """Create a MerakiVlan instance from a dictionary."""
        return cls(
            id=data.get("id") or data.get("vlanId"),
            name=data.get("name"),
            subnet=data.get("subnet"),
            appliance_ip=data.get("applianceIp"),
            ipv6=data.get("ipv6"),
            dhcp_handling=data.get("dhcpHandling"),
            dns_nameservers=data.get("dnsNameservers"),
            dhcp_lease_time=data.get("dhcpLeaseTime"),
            dhcp_boot_options_enabled=data.get("dhcpBootOptionsEnabled", False),
        )


@dataclass
class MerakiFirewallRule:
    """Represents a Meraki L3 Firewall Rule."""

    comment: str | None = None
    policy: str | None = None
    protocol: str | None = None
    dest_port: str | None = None
    dest_cidr: str | None = None
    src_port: str | None = None
    src_cidr: str | None = None
    syslog_enabled: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiFirewallRule:
        """Create a MerakiFirewallRule instance from a dictionary."""
        return cls(
            comment=data.get("comment"),
            policy=data.get("policy"),
            protocol=data.get("protocol"),
            dest_port=data.get("destPort"),
            dest_cidr=data.get("destCidr"),
            src_port=data.get("srcPort"),
            src_cidr=data.get("srcCidr"),
            syslog_enabled=data.get("syslogEnabled", False),
        )


@dataclass
class MerakiTrafficShaping:
    """Represents Meraki Traffic Shaping settings."""

    enabled: bool = False
    rules: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiTrafficShaping:
        """Create a MerakiTrafficShaping instance from a dictionary."""
        return cls(
            enabled=data.get("enabled", False),
            rules=data.get("rules", []),
        )


@dataclass
class MerakiVpn:
    """Represents Meraki Site-to-Site VPN settings."""

    mode: str | None = None
    hubs: list = field(default_factory=list)
    subnets: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiVpn:
        """Create a MerakiVpn instance from a dictionary."""
        return cls(
            mode=data.get("mode"),
            hubs=data.get("hubs", []),
            subnets=data.get("subnets", []),
        )
