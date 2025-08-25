"""Type definitions for Meraki API data structures."""

from typing import List, Optional
from typing_extensions import TypedDict


class MerakiVlan(TypedDict):
    """Represents a Meraki VLAN."""

    id: str
    name: str
    subnet: Optional[str]
    applianceIp: Optional[str]


class MerakiNetwork(TypedDict):
    """Represents a Meraki Network."""

    id: str
    name: str
    productTypes: List[str]


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
