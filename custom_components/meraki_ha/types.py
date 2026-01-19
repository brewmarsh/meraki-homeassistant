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
    firmware: str | None = None
    mac: str | None = None
    networkId: str | None = None
    status: str | None = None
    productType: str | None = None
    lanIp: str | None = None
    wan1Ip: str | None = None
    wan2Ip: str | None = None
    publicIp: str | None = None
    video_settings: dict[str, Any] | None = None
    ports_statuses: list[dict[str, Any]] = field(default_factory=list)
    ports: list[dict[str, Any]] = field(default_factory=list)
    radio_settings: dict[str, Any] | None = None
    dynamicDns: dict[str, Any] | None = None
    rtsp_url: str | None = None
    sense_settings: dict[str, Any] | None = None
    readings: list[dict[str, Any]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    # Internal/HA fields
    entity_id: str | None = None
    status_messages: list[str] = field(default_factory=list)
    entities: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiDevice:
        """Create a MerakiDevice from a dictionary, filtering unknown keys."""
        # Get field names from the dataclass
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        # Filter input data to only include known fields
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)


@dataclass
class MerakiNetwork:
    """Dataclass for a Meraki network."""

    id: str
    name: str
    organizationId: str
    productTypes: list[str] = field(default_factory=list)
    tags: list[str] | str | None = None
    clientCount: int | None = None
    timeZone: str | None = None
    notes: str | None = None

    # Internal/HA fields
    status_messages: list[str] = field(default_factory=list)
    is_enabled: bool = True
    ssids: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MerakiNetwork:
        """Create a MerakiNetwork from a dictionary, filtering unknown keys."""
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)


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
