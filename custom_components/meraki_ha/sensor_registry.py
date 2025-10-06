# custom_components/meraki_ha/sensor_registry.py
"""Sensor registry for Meraki Home Assistant integration."""

from typing import List, Type, Dict
from homeassistant.helpers.entity import Entity

# Import sensor classes
from .sensor.device.device_status import MerakiDeviceStatusSensor
from .sensor.device.connected_clients import MerakiDeviceConnectedClientsSensor
from .sensor.device.meraki_wan1_connectivity import MerakiWAN1ConnectivitySensor
from .sensor.device.meraki_wan2_connectivity import MerakiWAN2ConnectivitySensor
from .sensor.device.meraki_firmware_status import MerakiFirmwareStatusSensor
from .sensor.device.data_usage import MerakiDataUsageSensor
from .sensor.device.poe_usage import MerakiPoeUsageSensor
from .sensor.device.camera_sense_status import MerakiCameraSenseStatusSensor
from .sensor.device.camera_audio_detection import MerakiCameraAudioDetectionSensor


SensorClassList = List[Type[Entity]]

# Sensors with __init__(coordinator, device_info)
SENSORS_COORD_DEV: Dict[str, SensorClassList] = {
    "switch": [
        MerakiPoeUsageSensor,
    ],
}

# Sensors with __init__(coordinator, device_info, config_entry)
SENSORS_COORD_DEV_CONF: Dict[str, SensorClassList] = {
    "appliance": [
        MerakiDeviceConnectedClientsSensor,
        MerakiWAN1ConnectivitySensor,
        MerakiWAN2ConnectivitySensor,
        MerakiFirmwareStatusSensor,
        MerakiDataUsageSensor,
    ],
    "wireless": [
        MerakiDeviceConnectedClientsSensor,
    ],
    "switch": [
        MerakiDeviceConnectedClientsSensor,
    ],
    "camera": [
        MerakiCameraSenseStatusSensor,
        MerakiCameraAudioDetectionSensor,
        MerakiFirmwareStatusSensor,
    ],
    "cellularGateway": [
        MerakiDeviceConnectedClientsSensor,
    ],
}

# Common sensors for all devices
COMMON_SENSORS_COORD_DEV_CONF: SensorClassList = [
    MerakiDeviceStatusSensor,
]


def get_sensors_for_device_type(
    product_type: str, with_config_entry: bool
) -> SensorClassList:
    """Return a list of sensor classes for a given Meraki product type."""
    if with_config_entry:
        return SENSORS_COORD_DEV_CONF.get(product_type, [])
    return SENSORS_COORD_DEV.get(product_type, [])