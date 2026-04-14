"""Coordinators for the Meraki HA integration."""

from .base import MerakiBaseCoordinator
from .main import MerakiMainCoordinator

# Aliases for unified polling architecture
MerakiApplianceCoordinator = MerakiMainCoordinator
MerakiCameraCoordinator = MerakiMainCoordinator
MerakiClientCoordinator = MerakiMainCoordinator
MerakiDeviceCoordinator = MerakiMainCoordinator
MerakiSensorCoordinator = MerakiMainCoordinator
MerakiSwitchCoordinator = MerakiMainCoordinator
MerakiWirelessCoordinator = MerakiMainCoordinator

__all__ = [
    "MerakiApplianceCoordinator",
    "MerakiBaseCoordinator",
    "MerakiCameraCoordinator",
    "MerakiClientCoordinator",
    "MerakiDeviceCoordinator",
    "MerakiMainCoordinator",
    "MerakiSensorCoordinator",
    "MerakiSwitchCoordinator",
    "MerakiWirelessCoordinator",
]
