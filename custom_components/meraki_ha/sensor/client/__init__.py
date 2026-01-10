"""Client sensor entities for Meraki integration.

This module provides sensor entities for Meraki network clients, exposing
dynamic data like VLAN, SSID, connected device, switchport, and data usage
as separate entities that can be tracked in history and used in automations.
"""

from .base import MerakiClientSensorBase
from .connected_device import MerakiClientConnectedDeviceSensor
from .connection_type import MerakiClientConnectionTypeSensor
from .data_usage import (
    MerakiClientReceivedBytesSensor,
    MerakiClientSentBytesSensor,
)
from .ssid import MerakiClientSSIDSensor
from .switchport import MerakiClientSwitchportSensor
from .vlan import MerakiClientVLANSensor

__all__ = [
    "MerakiClientSensorBase",
    "MerakiClientVLANSensor",
    "MerakiClientSSIDSensor",
    "MerakiClientConnectedDeviceSensor",
    "MerakiClientConnectionTypeSensor",
    "MerakiClientSwitchportSensor",
    "MerakiClientSentBytesSensor",
    "MerakiClientReceivedBytesSensor",
]
