"""Models package for Meraki API data structures."""

from .appliance import MerakiApplianceMixin, MerakiAppliancePort
from .camera import MerakiCameraMixin
from .device import MerakiDevice
from .network import (
    MerakiFirewallRule,
    MerakiNetwork,
    MerakiTrafficShaping,
    MerakiVlan,
    MerakiVpn,
)
from .organization import MerakiOrganization
from .sensor import MerakiSensorMixin
from .switch import MerakiSwitchMixin
from .wireless import MerakiWirelessMixin

__all__ = [
    "MerakiApplianceMixin",
    "MerakiAppliancePort",
    "MerakiCameraMixin",
    "MerakiDevice",
    "MerakiFirewallRule",
    "MerakiNetwork",
    "MerakiOrganization",
    "MerakiSensorMixin",
    "MerakiSwitchMixin",
    "MerakiTrafficShaping",
    "MerakiVlan",
    "MerakiVpn",
    "MerakiWirelessMixin",
]
