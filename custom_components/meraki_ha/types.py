"""Type definitions for Meraki API data structures."""

from __future__ import annotations

from typing import TypedDict


class MerakiVlan(TypedDict):
    """Represents a Meraki VLAN."""

    id: str
    name: str
    subnet: str | None
    applianceIp: str | None
    ipv6: dict | None


class MerakiNetwork(TypedDict):
    """Represents a Meraki Network."""

    id: str
    name: str
    productTypes: list[str]
    organizationId: str
    tags: str | None
    clientCount: int | None


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
