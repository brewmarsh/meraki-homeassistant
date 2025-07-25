"""Utility functions for classifying Meraki device models.

This module provides helper functions to map specific Meraki device model
strings to more general device type categories. This is useful for
categorizing devices within the Home Assistant integration.
"""


def map_meraki_model_to_device_type(model: str) -> str:
    """Maps a Meraki device model string to a generic device type category.

    The function checks the prefix of the model string to determine its
    general category. Handles all Meraki device types including newer models.

    Args:
        model: The Meraki device model string (e.g., "MR52", "MS220-8P", "GR12",
               "MV12", etc.). It's expected to be a non-empty string.

    Returns:
        A string representing the generic device type:
        - "wireless" for MR and GR series APs
        - "switch" for MS and GS series switches
        - "appliance" for MX series security appliances
        - "camera" for MV series cameras
        - "sensor" for MT series sensors
        - "cellular" for MG series cellular gateways
        Returns "unknown" if the model prefix doesn't match any known category.
    """
    # Handle empty string or None case
    if not model:
        return "unknown"

    # Convert to uppercase for consistent matching
    model_upper = model.upper()

    if model_upper == "NETWORK":  # Specific check for "Network"
        return "network"
    # Wireless Access Points (both traditional MR and cloud-managed GR series)
    if model_upper.startswith(("MR", "GR")):
        return "wireless"

    # Switches (both traditional MS and cloud-managed GS series)
    if model_upper.startswith(("MS", "GS")):
        return "switch"

    # Security Appliances
    if model_upper.startswith("MX"):
        return "appliance"

    # Cameras
    if model_upper.startswith("MV"):
        return "camera"

    # Environmental Sensors
    if model_upper.startswith("MT"):
        return "sensor"

    # Cellular Gateways
    if model_upper.startswith("MG"):
        return "cellular"

    # If no match is found, return unknown
    return "unknown"
