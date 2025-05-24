"""Provides utility functions for classifying Meraki device models.

This module contains functions to map specific Meraki device model strings
to more general device type categories, which can be useful for logging,
device representation in Home Assistant, or conditional logic based on
device capabilities.
"""


def map_meraki_model_to_device_type(model: str) -> str:
    """Maps a Meraki device model string to a generic device type category.

    The function checks the prefix of the model string to determine its
    general type (e.g., "MR" models are wireless access points, "MS" are
    switches).

    Args:
        model (str): The Meraki device model string (e.g., "MR56", "MS220-8P", "MX67").
            It's expected to be a non-empty string.

    Returns:
        str: A string representing the generic device type (e.g., "Wireless",
             "Switch", "Appliance", "Camera", "Sensor"). Returns "Unknown" if the
             model prefix does not match any known Meraki product lines or if the
             input model string is empty or None (though type hint expects str).
    """
    if not isinstance(model, str) or not model:
        # Handle cases where model is not a string or is an empty string.
        return "Unknown"

    # Check model prefixes to determine the device type.
    # Order might matter if some prefixes are subsets of others, though not currently the case.
    if model.startswith("MR") or model.startswith("GR"):
        # MR series are indoor Access Points.
        # GR series are outdoor Access Points.
        return "Wireless"
    elif model.startswith("MS") or model.startswith("GS"):
        # MS series are network Switches.
        # GS series might be a typo or a less common series, often MS is used.
        # Assuming GS here is also intended to be a switch.
        return "Switch"
    elif model.startswith("MX"):
        # MX series are Security Appliances (firewalls, routers).
        return "Appliance"
    elif model.startswith("MV"):
        # MV series are smart Cameras.
        return "Camera"
    elif model.startswith("MT"):
        # MT series are environmental Sensors.
        return "Sensor"
    else:
        # If the model prefix doesn't match known types.
        return "Unknown"
