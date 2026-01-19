"""Type definitions for Meraki API data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypedDict


class MerakiVlan(TypedDict):
    """Represents a Meraki VLAN."""

    id: str
    name: str
    subnet: str | None
    applianceIp: str | None
    ipv6: dict | None


@dataclass
class MerakiNetwork:
    """Represents a Meraki Network."""

    id: str
    name: str
    productTypes: list[str]
    organizationId: str
    tags: str | None = None
    clientCount: int | None = None
    # Dynamic fields added by coordinator
    ssids: list[dict[str, Any]] = field(default_factory=list)
    status_messages: list[str] = field(default_factory=list)
    is_enabled: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiNetwork:
        """Create a MerakiNetwork from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            productTypes=data.get("productTypes", []),
            organizationId=data["organizationId"],
            tags=data.get("tags"),
            clientCount=data.get("clientCount"),
        )


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


@dataclass
class MerakiDevice:
    """Represents a Meraki Device."""

    serial: str
    name: str
    model: str
    networkId: str
    productType: str
    status: str | None = None
    lanIp: str | None = None
    video_settings: dict[str, Any] = field(default_factory=dict)
    ports_statuses: list[dict[str, Any]] = field(default_factory=list)
    radio_settings: dict[str, Any] = field(default_factory=dict)
    dynamicDns: dict[str, Any] = field(default_factory=dict)
    rtsp_url: str | None = None
    sense_settings: dict[str, Any] = field(default_factory=dict)
    readings: list[dict[str, Any]] = field(default_factory=list)
    firmware: str | None = None
    mac: str | None = None
    ports: list[dict[str, Any]] = field(default_factory=list)

    # Dynamic fields added by coordinator
    entity_id: str | None = None
    status_messages: list[str] = field(default_factory=list)
    entities: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiDevice:
        """Create a MerakiDevice from a dictionary."""
        return cls(
            serial=data["serial"],
            name=data.get("name", ""),
            model=data.get("model", ""),
            networkId=data.get("networkId", ""),
            productType=data.get("productType", ""),
            status=data.get("status"),
            lanIp=data.get("lanIp"),
            video_settings=data.get("video_settings", {}),
            ports_statuses=data.get("ports_statuses", []),
            radio_settings=data.get("radio_settings", {}),
            dynamicDns=data.get("dynamicDns", {}),
            rtsp_url=data.get("rtsp_url"),
            sense_settings=data.get("sense_settings", {}),
            readings=data.get("readings", []),
            firmware=data.get("firmware"),
            mac=data.get("mac"),
            ports=data.get("ports", []),
        )
