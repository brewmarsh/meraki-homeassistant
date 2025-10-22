"""Type definitions for Meraki API data structures."""

from typing import List, Optional
from typing_extensions import TypedDict


class MerakiVlan(TypedDict):
    """Represents a Meraki VLAN."""

    id: str
    name: str
    subnet: Optional[str]
    applianceIp: Optional[str]
    ipv6: Optional[dict]


class MerakiNetwork(TypedDict):
    """Represents a Meraki Network."""

    id: str
    name: str
    productTypes: List[str]
    organizationId: str
    tags: Optional[str]
    clientCount: Optional[int]


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
    status: Optional[str]
    productType: str
    lanIp: Optional[str]
    video_settings: dict
    ports_statuses: list
    radio_settings: dict
    dynamicDns: dict
    rtsp_url: Optional[str]
    sense_settings: dict
