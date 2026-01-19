"""Type definitions for Meraki API data structures."""

from __future__ import annotations

<<<<<<< HEAD
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
=======
from typing import TypedDict
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)


class MerakiVlan(TypedDict):
    """Represents a Meraki VLAN."""

    id: str
    name: str
    subnet: str | None
    applianceIp: str | None
    ipv6: dict | None


<<<<<<< HEAD
=======
class MerakiNetwork(TypedDict):
    """Represents a Meraki Network."""

    id: str
    name: str
    productTypes: list[str]
    organizationId: str
    tags: str | None
    clientCount: int | None


>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
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
<<<<<<< HEAD
=======


class MerakiDevice(TypedDict, total=False):
    """Represents a Meraki Device. Not all keys are guaranteed."""

    serial: str
    name: str
    model: str
    networkId: str
    status: str | None
    productType: str
    lanIp: str | None
    video_settings: dict
    ports_statuses: list
    radio_settings: dict
    dynamicDns: dict
    rtsp_url: str | None
    sense_settings: dict
    readings: list[dict]
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
