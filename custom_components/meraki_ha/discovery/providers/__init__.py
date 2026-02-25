"""Discovery providers for Meraki devices."""
from .appliance import AppliancePortProvider
from .camera import CameraAnalyticsProvider, CameraStreamProvider
from .device import PhysicalSensorProvider
from .mt_sensor import MT40PowerMonitorProvider
from .switch import SwitchPortProvider
from .uplink import UplinkPerformanceProvider, UplinkProvider
from .wireless import WirelessRadioProvider

__all__ = [
    "AppliancePortProvider",
    "CameraAnalyticsProvider",
    "CameraStreamProvider",
    "MT40PowerMonitorProvider",
    "PhysicalSensorProvider",
    "SwitchPortProvider",
    "UplinkPerformanceProvider",
    "UplinkProvider",
    "WirelessRadioProvider",
]
