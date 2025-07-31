"""Utility functions for classifying Meraki device models.

This module provides helper functions to map specific Meraki device model
strings to more general device type categories. This is useful for
categorizing devices within the Home Assistant integration.

Device Types:
    - wireless: Access Points (MR/GR series)
    - switch: Network Switches (MS/GS series)
    - appliance: Security Appliances (MX series)
    - camera: Smart Cameras (MV series)
    - sensor: Environmental Sensors (MT series)
    - cellular: Cellular Gateways (MG series)
    - network: Virtual Network Devices
    - unknown: Unrecognized Device Types

Example:
    >>> model = "MR52"
    >>> device_type = map_meraki_model_to_device_type(model)
    >>> print(device_type)
    'wireless'

References:
    - Meraki Device Documentation: https://documentation.meraki.com/Hardware
    - MR Series: https://documentation.meraki.com/MR
    - MS Series: https://documentation.meraki.com/MS
    - MX Series: https://documentation.meraki.com/MX
    - MV Series: https://documentation.meraki.com/MV
    - MT Series: https://documentation.meraki.com/MT
    - MG Series: https://documentation.meraki.com/MG
"""

from enum import Enum
from typing import Final, List, Optional
import re

# Define device type constants
DEVICE_TYPE_WIRELESS: Final = "wireless"
DEVICE_TYPE_SWITCH: Final = "switch"
DEVICE_TYPE_APPLIANCE: Final = "appliance"
DEVICE_TYPE_CAMERA: Final = "camera"
DEVICE_TYPE_SENSOR: Final = "sensor"
DEVICE_TYPE_CELLULAR: Final = "cellular"
DEVICE_TYPE_NETWORK: Final = "network"
DEVICE_TYPE_UNKNOWN: Final = "unknown"

# Compiled regex pattern for model validation
MODEL_PATTERN: Final = re.compile(r"^(MR|MS|MX|MV|MT|MG|GR|GS)[\d-]+([A-Z0-9-]+)?$")

# Valid device types for type checking
VALID_DEVICE_TYPES: Final[List[str]] = [
    DEVICE_TYPE_WIRELESS,
    DEVICE_TYPE_SWITCH,
    DEVICE_TYPE_APPLIANCE,
    DEVICE_TYPE_CAMERA,
    DEVICE_TYPE_SENSOR,
    DEVICE_TYPE_CELLULAR,
    DEVICE_TYPE_NETWORK,
    DEVICE_TYPE_UNKNOWN,
]


class DeviceType(str, Enum):
    """Enum for Meraki device types."""

    WIRELESS = DEVICE_TYPE_WIRELESS
    SWITCH = DEVICE_TYPE_SWITCH
    APPLIANCE = DEVICE_TYPE_APPLIANCE
    CAMERA = DEVICE_TYPE_CAMERA
    SENSOR = DEVICE_TYPE_SENSOR
    CELLULAR = DEVICE_TYPE_CELLULAR
    NETWORK = DEVICE_TYPE_NETWORK
    UNKNOWN = DEVICE_TYPE_UNKNOWN


# Map device prefixes to types
DEVICE_PREFIX_MAPPINGS: Final[dict[tuple[str, ...], str]] = {
    # Wireless Access Points (both traditional MR and cloud-managed GR series)
    ("MR", "GR"): DeviceType.WIRELESS,
    # Switches (both traditional MS and cloud-managed GS series)
    ("MS", "GS"): DeviceType.SWITCH,
    # Security Appliances
    ("MX",): DeviceType.APPLIANCE,
    # Cameras
    ("MV",): DeviceType.CAMERA,
    # Environmental Sensors
    ("MT",): DeviceType.SENSOR,
    # Cellular Gateways
    ("MG",): DeviceType.CELLULAR,
}

# Device type descriptions for UI and logging
DEVICE_TYPE_DESCRIPTIONS: Final[dict[str, str]] = {
    DEVICE_TYPE_WIRELESS: "Wireless Access Point",
    DEVICE_TYPE_SWITCH: "Network Switch",
    DEVICE_TYPE_APPLIANCE: "Security Appliance",
    DEVICE_TYPE_CAMERA: "Smart Camera",
    DEVICE_TYPE_SENSOR: "Environmental Sensor",
    DEVICE_TYPE_CELLULAR: "Cellular Gateway",
    DEVICE_TYPE_NETWORK: "Virtual Network Device",
    DEVICE_TYPE_UNKNOWN: "Unknown Device",
}


class DeviceType(str, Enum):
    """Enum for Meraki device types."""

    WIRELESS = DEVICE_TYPE_WIRELESS
    SWITCH = DEVICE_TYPE_SWITCH
    APPLIANCE = DEVICE_TYPE_APPLIANCE
    CAMERA = DEVICE_TYPE_CAMERA
    SENSOR = DEVICE_TYPE_SENSOR
    CELLULAR = DEVICE_TYPE_CELLULAR
    NETWORK = DEVICE_TYPE_NETWORK
    UNKNOWN = DEVICE_TYPE_UNKNOWN


def map_meraki_model_to_device_type(model: Optional[str]) -> str:
    """Maps a Meraki device model string to a generic device type category.

    The function checks the prefix of the model string to determine its
    general category. Handles all Meraki device types including newer models
    and non-Meraki GO devices. Case-insensitive matching is used for robustness.

    Model Prefixes:
        - MR/GR: Wireless Access Points
        - MS/GS: Network Switches (including GS110-24P format)
        - MX: Security Appliances
        - MV: Smart Cameras
        - MT: Environmental Sensors
        - MG: Cellular Gateways

    Special Cases:
        - "Network": Virtual network device
        - Empty/None: Returns unknown type
        - Unrecognized prefix: Returns unknown type
        - Invalid format: Returns unknown type

    Args:
        model: The Meraki device model string (e.g., "MR52", "MS220-8P").
              Can be None or empty string.

    Returns:
        A string from VALID_DEVICE_TYPES representing the device category.

    Examples:
        >>> map_meraki_model_to_device_type("MR52")
        'wireless'
        >>> map_meraki_model_to_device_type("MS220-8P")
        'switch'
        >>> map_meraki_model_to_device_type(None)
        'unknown'
        >>> map_meraki_model_to_device_type("INVALID")
        'unknown'
    """
    # Handle empty string or None case
    if not model or not validate_model_string(model):
        return DeviceType.UNKNOWN

    # Convert to uppercase for consistent matching
    model_upper = model.upper()

    # Special case for virtual network devices
    if model_upper == "NETWORK":
        return DeviceType.NETWORK

    # Check each prefix group from the mappings
    for prefixes, device_type in DEVICE_PREFIX_MAPPINGS.items():
        if any(model_upper.startswith(prefix) for prefix in prefixes):
            return device_type

    # If no match is found, return unknown
    return DeviceType.UNKNOWN


def validate_model_string(model: str) -> bool:
    """Validates that a model string matches expected Meraki model patterns.

    Args:
        model: The model string to validate (e.g., "MR52", "MS220-8P")

    Returns:
        bool: True if the model string matches expected patterns, False otherwise

    Examples:
        >>> validate_model_string("MR52")
        True
        >>> validate_model_string("MS220-8P")
        True
        >>> validate_model_string("INVALID")
        False
    """
    if not model:
        return False

    model_upper = model.upper()

    # Special case for virtual network devices
    if model_upper == "NETWORK":
        return True

    # Use pre-compiled pattern to validate model format
    return bool(MODEL_PATTERN.match(model_upper))


def validate_device_type(device_type: str) -> bool:
    """Validates that a device type string is one of the valid types.

    Args:
        device_type: The device type string to validate

    Returns:
        bool: True if the device type is valid, False otherwise

    Examples:
        >>> validate_device_type("wireless")
        True
        >>> validate_device_type("invalid")
        False
    """
    return device_type in VALID_DEVICE_TYPES


def get_device_type_description(device_type: str) -> str:
    """Gets a human-readable description of a device type.

    Args:
        device_type: The device type string (e.g., "wireless", "switch")

    Returns:
        str: A human-readable description of the device type.
             Returns the unknown device description for invalid types.

    Examples:
        >>> get_device_type_description("wireless")
        'Wireless Access Point'
        >>> get_device_type_description("unknown")
        'Unknown Device'
        >>> get_device_type_description("invalid")
        'Unknown Device'
    """
    if not validate_device_type(device_type):
        return DEVICE_TYPE_DESCRIPTIONS[DEVICE_TYPE_UNKNOWN]
    return DEVICE_TYPE_DESCRIPTIONS[device_type]


def get_supported_model_prefixes() -> set[str]:
    """Gets all supported Meraki model prefixes.

    Returns:
        set[str]: A set of all supported model prefixes (e.g., {'MR', 'MS', 'MX'})

    Examples:
        >>> prefixes = get_supported_model_prefixes()
        >>> 'MR' in prefixes
        True
        >>> len(prefixes) > 0
        True
    """
    return {prefix for prefixes in DEVICE_PREFIX_MAPPINGS.keys() for prefix in prefixes}


def get_prefixes_for_device_type(device_type: str) -> set[str]:
    """Gets all model prefixes for a given device type.

    Args:
        device_type: The device type to get prefixes for (e.g., "wireless", "switch")

    Returns:
        set[str]: A set of model prefixes for the device type (e.g., {'MR', 'GR'} for wireless)

    Examples:
        >>> get_prefixes_for_device_type("wireless")
        {'MR', 'GR'}
        >>> get_prefixes_for_device_type("unknown")
        set()
    """
    return {
        prefix
        for prefixes, dtype in DEVICE_PREFIX_MAPPINGS.items()
        if dtype == device_type
        for prefix in prefixes
    }
