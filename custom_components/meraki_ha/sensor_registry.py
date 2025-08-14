# custom_components/meraki_ha/sensor_registry.py
"""Sensor registry for Meraki Home Assistant integration."""

from typing import List, Type, Dict
from homeassistant.helpers.entity import Entity

# Import sensor classes
from .sensor.device.device_status import MerakiDeviceStatusSensor
from .sensor.device.connected_clients import MerakiDeviceConnectedClientsSensor
from .sensor.device.radio_settings import MerakiRadioSettingsSensor
from .sensor.device.meraki_wan1_connectivity import MerakiWAN1ConnectivitySensor
from .sensor.device.meraki_wan2_connectivity import MerakiWAN2ConnectivitySensor
from .sensor.device.meraki_firmware_status import MerakiFirmwareStatusSensor
from .sensor.device.data_usage import MerakiDataUsageSensor
from .sensor.device.poe_usage import MerakiPoeUsageSensor

# Camera-specific sensors from new modules
from .sensor.device.camera_sense_status import MerakiCameraSenseStatusSensor
from .sensor.device.camera_audio_detection import MerakiCameraAudioDetectionSensor
from .sensor.device.camera_rtsp_url import MerakiCameraRTSPUrlSensor


SensorClassList = List[Type[Entity]]

SENSOR_REGISTRY: Dict[str, SensorClassList] = {
    "appliance": [
        MerakiWAN1ConnectivitySensor,
        MerakiWAN2ConnectivitySensor,
        MerakiFirmwareStatusSensor,
        MerakiDataUsageSensor,
        MerakiDeviceConnectedClientsSensor,
    ],
    "wireless": [
        MerakiDeviceConnectedClientsSensor,
        MerakiRadioSettingsSensor,
    ],
    "switch": [
        MerakiPoeUsageSensor,
    ],
    "camera": [],
    "sensor": [],
}

COMMON_DEVICE_SENSORS: SensorClassList = [
    MerakiDeviceStatusSensor,
]


def get_sensors_for_device_type(product_type: str) -> SensorClassList:
    """Return a list of sensor classes for a given Meraki product type."""
    return SENSOR_REGISTRY.get(product_type, [])
