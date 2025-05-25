"""Utility functions for classifying Meraki device models.

This module provides helper functions to map specific Meraki device model strings
to more general device type categories. This is useful for categorizing devices
within the Home Assistant integration.
"""


def map_meraki_model_to_device_type(model: str) -> str:
    """Maps a Meraki device model string to a generic device type category.

    The function checks the prefix of the model string to determine its
    general category (e.g., "MR" models are "Wireless", "MS" models are "Switch").

    Args:
        model: The Meraki device model string (e.g., "MR52", "MS220-8P").
               It's expected to be a non-empty string.

    Returns:
        A string representing the generic device type (e.g., "Wireless",
        "Switch", "Appliance", "Camera", "Sensor"). Returns "Unknown" if the
        model prefix does not match any known category.
    """
    if not model: # Handle empty string case, though API usually provides models
        return "Unknown"

    model_upper = model.upper() # Ensure case-insensitivity for prefixes

    if model_upper.startswith("MR") or model_upper.startswith("GR"):
        return "Wireless"  # Meraki Wireless Access Points (MR series, GR is older/alt)
    elif model_upper.startswith("MS") or model_upper.startswith("GS"):
        return "Switch"    # Meraki Switches (MS series, GS is older/alt)
    elif model_upper.startswith("MX"):
        return "Appliance" # Meraki Security Appliances/Routers
    elif model_upper.startswith("MV"):
        return "Camera"    # Meraki Smart Cameras
    elif model_upper.startswith("MT"):
        return "Sensor"    # Meraki MT Series Sensors
    else:
        return "Unknown"   # Default for unrecognized model prefixes
