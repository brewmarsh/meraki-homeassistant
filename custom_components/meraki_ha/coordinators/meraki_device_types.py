"""Utility functions for classifying Meraki device models.

This module provides helper functions to map specific Meraki device model
strings to more general device type categories. This is useful for
categorizing devices within the Home Assistant integration.
"""


def map_meraki_model_to_device_type(model: str) -> str:
    """Maps a Meraki device model string to a generic device type category.

    The function checks the prefix of the model string to determine its
    general category (e.g., "MR" models are "Wireless", "MS" models are "Switch").

    Args:
        model: The Meraki device model string (e.g., "MR52",
               "MS220-8P"). It's expected to be a non-empty string.

    Returns:
        A string representing the generic device type (e.g., "Wireless",
        "Switch", "Appliance", "Camera", "Sensor"). Returns "Unknown" if the
        model prefix does not match any known category.
    """
    # Handle empty string case, though API usually provides models
    if not model:
        return "Unknown"

    # Ensure case-insensitivity for prefixes
    model_upper = model.upper()

    if model_upper.startswith("MR") or model_upper.startswith("GR"):
        # Meraki Wireless Access Points (MR series, GR is older/alt)
        return "Wireless"
    elif model_upper.startswith("MS") or model_upper.startswith("GS"):
        # Meraki Switches (MS series, GS is older/alt)
        return "Switch"
    elif model_upper.startswith("MX"):
        # Meraki Security Appliances/Routers
        return "Appliance"
    elif model_upper.startswith("MV"):
        # Meraki Smart Cameras
        return "Camera"
    elif model_upper.startswith("MT"):
        # Meraki MT Series Sensors
        return "Sensor"
    else:
        # Default for unrecognized model prefixes
        return "Unknown"
