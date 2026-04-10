"""Models package for Meraki API data structures."""

from .appliance import ApplianceMixin, MerakiApplianceDevice, MerakiAppliancePort
from .base import MerakiBaseDevice
from .camera import CameraMixin, MerakiCameraDevice
from .device import MerakiDevice
from .network import (
    MerakiFirewallRule,
    MerakiNetwork,
    MerakiTrafficShaping,
    MerakiVlan,
    MerakiVpn,
)
from .organization import MerakiOrganization
from .sensor import MerakiSensorDevice, SensorMixin
from .switch import MerakiSwitchDevice, SwitchMixin
from .wireless import MerakiWirelessDevice, WirelessMixin

__all__ = [
    "ApplianceMixin",
    "CameraMixin",
    "MerakiApplianceDevice",
    "MerakiAppliancePort",
    "MerakiBaseDevice",
    "MerakiCameraDevice",
    "MerakiDevice",
    "MerakiFirewallRule",
    "MerakiNetwork",
    "MerakiOrganization",
    "MerakiSensorDevice",
    "MerakiSwitchDevice",
    "MerakiWirelessDevice",
    "SensorMixin",
    "SwitchMixin",
    "MerakiTrafficShaping",
    "MerakiVlan",
    "MerakiVpn",
    "WirelessMixin",
]
