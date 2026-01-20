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
    appliance_uplink_statuses: list[dict[str, Any]] = field(default_factory=list)
    status: str | None = None
    firmware: str | None = None
    product_type: str | None = None
    tags: list[str] = field(default_factory=list)
    readings: list[dict[str, Any]] = field(default_factory=list)
    video_settings: dict[str, Any] | None = None
    rtsp_url: str | None = None
    sense_settings: dict[str, Any] | None = None
    analytics: list[dict[str, Any]] = field(default_factory=list)
    ports_statuses: list[dict[str, Any]] = field(default_factory=list)
    appliance_ports: list["MerakiAppliancePort"] = field(default_factory=list)
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
            firmware=data.get("firmware"),
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


@dataclass
class MerakiVlan:
    """Represents a Meraki VLAN."""

    id: str
    name: str
    subnet: str | None = None
    appliance_ip: str | None = None
    ipv6: dict | None = None
    dhcp_handling: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MerakiVlan":
        """Create a MerakiVlan instance from a dictionary."""
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            subnet=data.get("subnet"),
            appliance_ip=data.get("applianceIp"),
            ipv6=data.get("ipv6"),
            dhcp_handling=data.get("dhcpHandling"),
        )


@dataclass
class MerakiFirewallRule:
    """Represents a Meraki L3 Firewall Rule."""

    comment: str
    policy: str
    protocol: str
    dest_port: str | None = None
    dest_cidr: str | None = None
    src_port: str | None = None
    src_cidr: str | None = None
    syslog_enabled: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MerakiFirewallRule":
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
    def from_dict(cls, data: dict[str, Any]) -> "MerakiTrafficShaping":
        """Create a MerakiTrafficShaping instance from a dictionary."""
        return cls(
            enabled=data.get("enabled", False),
            rules=data.get("rules", []),
        )


@dataclass
class MerakiVpn:
    """Represents Meraki Site-to-Site VPN settings."""

    mode: str
    hubs: list = field(default_factory=list)
    subnets: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MerakiVpn":
        """Create a MerakiVpn instance from a dictionary."""
        return cls(
            mode=data.get("mode"),
            hubs=data.get("hubs", []),
            subnets=data.get("subnets", []),
        )


@dataclass
class MerakiAppliancePort:
    """Represents a Meraki Appliance Port."""

    number: int
    enabled: bool = False
    type: str | None = None
    drop_untagged_traffic: bool = False
    vlan: int | None = None
    access_policy: str | None = None
    allowed_vlans: str | None = None
    status: str | None = None
    speed: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MerakiAppliancePort":
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
