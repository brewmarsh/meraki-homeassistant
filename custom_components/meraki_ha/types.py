"""Type definitions for Meraki API data structures (re-exports)."""

from __future__ import annotations

from .core.models import MerakiAppliancePort
from .core.models.device import MerakiDevice
from .core.models.network import (
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
