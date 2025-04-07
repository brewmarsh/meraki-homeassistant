from .ssid_availability import MerakiSSIDAvailabilitySensor
from .ssid_channel import MerakiSSIDChannelSensor
from .ssid_client_count import MerakiSSIDClientCountSensor


def create_ssid_sensors(coordinator, device, ssid):
    """Create sensor entities for a given SSID."""
    sensors = []
    sensors.append(MerakiSSIDAvailabilitySensor(coordinator, device, ssid))
    sensors.append(MerakiSSIDChannelSensor(coordinator, device, ssid))
    sensors.append(MerakiSSIDClientCountSensor(coordinator, device, ssid))
    # Add other sensor types as needed
    return sensors
