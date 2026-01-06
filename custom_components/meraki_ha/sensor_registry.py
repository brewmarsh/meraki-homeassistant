"""Sensor registry for Meraki Home Assistant integration."""

from __future__ import annotations

from homeassistant.helpers.entity import Entity

from .sensor.device.camera_audio_detection import MerakiCameraAudioDetectionSensor
from .sensor.device.camera_sense_status import MerakiCameraSenseStatusSensor
from .sensor.device.connected_clients import MerakiDeviceConnectedClientsSensor
from .sensor.device.data_usage import MerakiDataUsageSensor
from .sensor.device.device_status import MerakiDeviceStatusSensor
from .sensor.device.meraki_firmware_status import MerakiFirmwareStatusSensor
from .sensor.device.meraki_wan1_connectivity import MerakiWAN1ConnectivitySensor
from .sensor.device.meraki_wan2_connectivity import MerakiWAN2ConnectivitySensor
from .sensor.device.poe_usage import MerakiPoeUsageSensor

SensorClassList = list[type[Entity]]

# Sensors with __init__(coordinator, device_info)
SENSORS_COORD_DEV: dict[str, SensorClassList] = {
    "switch": [
        MerakiPoeUsageSensor,
    ],
}

# Sensors with __init__(coordinator, device_info, config_entry)
SENSORS_COORD_DEV_CONF: dict[str, SensorClassList] = {
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

<<<<<<< HEAD
<<<<<<< HEAD
=======
# Alias for backward compatibility or clarity if needed
COMMON_DEVICE_SENSORS = COMMON_SENSORS_COORD_DEV_CONF

>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129

def get_sensors_for_device_type(
    product_type: str,
    with_config_entry: bool,
) -> SensorClassList:
    """
    Return a list of sensor classes for a given Meraki product type.

    Args:
    ----
        product_type: The product type of the device.
        with_config_entry: Whether to include sensors that require a config entry.

    Returns
    -------
        A list of sensor classes.

    """
    if with_config_entry:
        return SENSORS_COORD_DEV_CONF.get(product_type, [])
    return SENSORS_COORD_DEV.get(product_type, [])
