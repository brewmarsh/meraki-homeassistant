"""Factory function for creating SSID-related sensor entities.

This module provides a utility function `create_ssid_sensors` that
instantiates and returns a list of all sensor entities relevant to a
specific Meraki SSID (Service Set Identifier).
"""

from typing import Any, Dict, List  # Added Any, Dict, List

from homeassistant.components.sensor import SensorEntity  # For type hinting return

# Import the specific sensor classes that will be instantiated
from .ssid_availability import MerakiSSIDAvailabilitySensor
from .ssid_channel import MerakiSSIDChannelSensor
from .ssid_client_count import MerakiSSIDClientCountSensor

# Assuming MerakiDataUpdateCoordinator is the specific coordinator type
# from ..coordinator import MerakiDataUpdateCoordinator
# Placeholder for type hinting if the actual coordinator class is complex
# or causes circular imports
MerakiDataUpdateCoordinator = Any


def create_ssid_sensors(
    coordinator: MerakiDataUpdateCoordinator,  # Type hint for the coordinator
    device_data: Dict[str, Any],  # Type hint for the parent device data
    ssid_data: Dict[str, Any],  # Type hint for the specific SSID data
) -> List[SensorEntity]:
    """Create and return a list of sensor entities for a given SSID.

    This function acts as a factory to instantiate various sensor types
    that are relevant to a single SSID, such as its availability,
    channel, and client count.

    Args:
        coordinator: The data update coordinator instance for these sensors.
        device_data: A dictionary containing information about the parent Meraki
                     device (e.g., an access point) to which the SSID belongs.
                     Expected to contain at least 'serial' and 'name'.
        ssid_data: A dictionary containing information about the specific SSID.
                   Expected to contain at least 'name' and 'number'.

    Returns:
        A list of initialized sensor entities (subclasses of `SensorEntity`)
        for the given SSID.
    """
    sensors: List[SensorEntity] = []

    # Instantiate each type of sensor for the SSID
    sensors.append(MerakiSSIDAvailabilitySensor(coordinator, device_data, ssid_data))
    sensors.append(MerakiSSIDChannelSensor(coordinator, device_data, ssid_data))
    sensors.append(MerakiSSIDClientCountSensor(coordinator, device_data, ssid_data))

    # Add other SSID-specific sensor types here as they are developed
    # Example:
    # sensors.append(MerakiSSIDSignalStrengthSensor(coordinator, device_data, ssid_data))
    # sensors.append(MerakiSSIDDataUsageSensor(coordinator, device_data, ssid_data))

    return sensors
