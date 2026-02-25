"""Models package for Meraki API data structures."""

from .device import MerakiDevice
from .mixins import (
    ApplianceMixin,
    CameraMixin,
    MerakiAppliancePort,
    SensorMixin,
    SwitchMixin,
    WirelessMixin,
)
from .network import (
    MerakiFirewallRule,
    MerakiNetwork,
    MerakiTrafficShaping,
    MerakiVlan,
    MerakiVpn,
)
from .organization import MerakiOrganization

__all__ = [
    "ApplianceMixin",
    "CameraMixin",
    "MerakiAppliancePort",
    "MerakiDevice",
    "MerakiFirewallRule",
    "MerakiNetwork",
    "MerakiOrganization",
    "SensorMixin",
    "SwitchMixin",
    "MerakiTrafficShaping",
    "MerakiVlan",
    "MerakiVpn",
    "WirelessMixin",
]
