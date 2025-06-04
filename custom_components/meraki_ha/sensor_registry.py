# custom_components/meraki_ha/sensor_registry.py
"""Sensor registry for Meraki Home Assistant integration."""

from typing import List, Type, Dict, Any
from homeassistant.helpers.entity import Entity

# Import sensor classes
# Physical device sensors
from .sensor.device_status import MerakiDeviceStatusSensor
from .sensor.uplink_status import MerakiUplinkStatusSensor
from .sensor.connected_clients import MerakiDeviceConnectedClientsSensor # For MR devices

# MX-specific sensors
from .sensor.meraki_wan1_connectivity import MerakiWAN1ConnectivitySensor
from .sensor.meraki_wan2_connectivity import MerakiWAN2ConnectivitySensor
from .sensor.meraki_network_info import MerakiNetworkInfoSensor
from .sensor.meraki_firmware_status import MerakiFirmwareStatusSensor

# SSID-specific sensors (These are typically handled by SSIDDeviceCoordinator,
# but listed here for completeness or future refactoring if structure changes.
# For now, they might not be used by the physical device sensor setup loop)
# from .sensor.ssid_availability import MerakiSSIDAvailabilitySensor
# from .sensor.ssid_channel import MerakiSSIDChannelSensor
# from .sensor.ssid_client_count import MerakiSSIDClientCountSensor

# Define which sensors apply to which productType
# Note: MerakiDeviceStatusSensor is added by default to all physical devices
# in the current sensor/__init__.py, so it might be handled separately or included here.

# Type hint for a list of sensor entity classes
SensorClassList = List[Type[Entity]]

SENSOR_REGISTRY: Dict[str, SensorClassList] = {
    "appliance": [  # For MX devices
        MerakiNetworkInfoSensor,
        MerakiWAN1ConnectivitySensor,
        MerakiWAN2ConnectivitySensor,
        MerakiFirmwareStatusSensor,
        MerakiUplinkStatusSensor, # Reinstated in previous work
    ],
    "wireless": [  # For MR devices
        MerakiDeviceConnectedClientsSensor,
        # Add other MR-specific sensors here if any, e.g., radio_settings could be a sensor
    ],
    "switch": [  # For MS devices
        # Add MS-specific sensors here, e.g., port status summaries, PoE consumption
    ],
    "camera": [  # For MV devices
        # Add MV-specific sensors here
    ],
    "sensor": [  # For MT devices
        # Add MT-specific sensors here
    ],
}

# Sensors to be added to all devices regardless of product type
# (unless already covered by specific product type lists)
COMMON_DEVICE_SENSORS: SensorClassList = [
    MerakiDeviceStatusSensor,
]

def get_sensors_for_device_type(product_type: str) -> SensorClassList:
    """Return a list of sensor classes for a given Meraki product type."""
    return SENSOR_REGISTRY.get(product_type, [])
