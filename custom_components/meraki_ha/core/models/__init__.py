"""Models package for Meraki API data structures."""

from .device import MerakiAppliancePort, MerakiDevice
from .network import (
    MerakiFirewallRule,
    MerakiNetwork,
    MerakiTrafficShaping,
    MerakiVlan,
    MerakiVpn,
)

__all__ = [
    "MerakiAppliancePort",
    "MerakiDevice",
    "MerakiFirewallRule",
    "MerakiNetwork",
    "MerakiTrafficShaping",
    "MerakiVlan",
    "MerakiVpn",
]
