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

    # Extra fields for internal use
    status_messages: list[str] = field(default_factory=list)
    entity_id: str | None = None
    ssids: list[dict[str, Any]] = field(default_factory=list)
    is_enabled: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiNetwork:
        """Create a MerakiNetwork from a dictionary."""
        # Filter keys to match dataclass fields
        known_keys = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if k in known_keys}
        return cls(**filtered_data)


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

    # Additional fields from API or usage
    mac: str | None = None
    firmware: str | None = None
    publicIp: str | None = None
    wan1Ip: str | None = None
    wan2Ip: str | None = None
    tags: list[str] = field(default_factory=list)
    uplinks: list[dict[str, Any]] = field(default_factory=list)
    lat: float | None = None
    lng: float | None = None
    address: str | None = None
    notes: str | None = None

    # Extra fields for internal use
    status_messages: list[str] = field(default_factory=list)
    entity_id: str | None = None
    entities: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiDevice:
        """Create a MerakiDevice from a dictionary."""
        known_keys = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if k in known_keys}
        return cls(**filtered_data)
