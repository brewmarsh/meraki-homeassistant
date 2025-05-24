"""Factory function for creating SSID-specific sensor entities.

This module provides a centralized function (`create_ssid_sensors`) that
instantiates and returns a list of all sensor entities relevant to a single
Meraki SSID. This helps in organizing sensor creation within the main
sensor platform setup.
"""
from typing import Any, Dict, List # Added for type hinting

from homeassistant.components.sensor import SensorEntity
# Assuming MerakiDataUpdateCoordinator is the type of coordinator used.
from ..coordinator import MerakiDataUpdateCoordinator
from .ssid_availability import MerakiSSIDAvailabilitySensor
from .ssid_channel import MerakiSSIDChannelSensor
from .ssid_client_count import MerakiSSIDClientCountSensor


def create_ssid_sensors(
    coordinator: MerakiDataUpdateCoordinator,
    device_info: Dict[str, Any],
    ssid_info: Dict[str, Any],
) -> List[SensorEntity]:
    """Creates and returns a list of sensor entities for a given SSID.

    This factory function is responsible for instantiating all sensors that
    are associated with a specific SSID on a Meraki device. Currently, this
    includes:
    - `MerakiSSIDAvailabilitySensor`: Tracks if the SSID is enabled/broadcasting.
    - `MerakiSSIDChannelSensor`: (If applicable) Displays the channel the SSID operates on.
    - `MerakiSSIDClientCountSensor`: Shows the number of clients connected to this SSID
      on the specific device.

    Args:
        coordinator (MerakiDataUpdateCoordinator): The main data update coordinator
            instance, passed to each sensor for data access.
        device_info (Dict[str, Any]): A dictionary containing information about the
            parent Meraki device (e.g., serial, name).
        ssid_info (Dict[str, Any]): A dictionary containing information about the
            specific SSID (e.g., name, number, enabled status).

    Returns:
        List[SensorEntity]: A list containing all instantiated sensor entities
            for the given SSID. This list can be directly used with
            `async_add_entities`.
    """
    sensors: List[SensorEntity] = []

    # Instantiate and add the SSID Availability sensor.
    sensors.append(
        MerakiSSIDAvailabilitySensor(coordinator, device_info, ssid_info)
    )

    # Instantiate and add the SSID Channel sensor.
    # Note: Channel information might be device-specific or band-specific,
    # ensure MerakiSSIDChannelSensor can correctly derive its state.
    sensors.append(MerakiSSIDChannelSensor(coordinator, device_info, ssid_info))

    # Instantiate and add the SSID Client Count sensor.
    sensors.append(MerakiSSIDClientCountSensor(coordinator, device_info, ssid_info))

    # Example for adding future SSID-specific sensors:
    # if "some_other_feature" in ssid_info:
    #     sensors.append(MerakiSomeOtherSSIDSensor(coordinator, device_info, ssid_info))

    return sensors
