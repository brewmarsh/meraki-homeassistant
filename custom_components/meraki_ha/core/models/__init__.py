"""Models package for Meraki API data structures."""

from .appliance import ApplianceMixin, MerakiAppliancePort
from .camera import CameraMixin
from .device import MerakiDevice
from .network import (
    MerakiFirewallRule,
    MerakiNetwork,
    MerakiTrafficShaping,
    MerakiVlan,
    MerakiVpn,
)
from .organization import MerakiOrganization
from .sensor import SensorMixin
from .switch import SwitchMixin
from .wireless import WirelessMixin

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
