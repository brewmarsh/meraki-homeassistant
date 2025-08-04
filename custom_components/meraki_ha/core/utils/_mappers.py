"""Utility functions for mapping and validating Meraki device types."""
from typing import Optional

from ._const import DeviceType, VALID_DEVICE_TYPES
from ._data import DEVICE_PREFIX_MAPPINGS, DEVICE_TYPE_DESCRIPTIONS, MODEL_PATTERN


def map_meraki_model_to_device_type(model: Optional[str]) -> str:
    """Maps a Meraki device model string to a generic device type category."""
    if not model or not validate_model_string(model):
        return DeviceType.UNKNOWN

    model_upper = model.upper()
    if model_upper == "NETWORK":
        return DeviceType.NETWORK

    for prefixes, device_type in DEVICE_PREFIX_MAPPINGS.items():
        if any(model_upper.startswith(prefix) for prefix in prefixes):
            return device_type

    return DeviceType.UNKNOWN


def validate_model_string(model: str) -> bool:
    """Validates that a model string matches expected Meraki model patterns."""
    if not model:
        return False
    model_upper = model.upper()
    if model_upper == "NETWORK":
        return True
    return bool(MODEL_PATTERN.match(model_upper))


def validate_device_type(device_type: str) -> bool:
    """Validates that a device type string is one of the valid types."""
    return device_type in VALID_DEVICE_TYPES


def get_device_type_description(device_type: str) -> str:
    """Gets a human-readable description of a device type."""
    if not validate_device_type(device_type):
        return DEVICE_TYPE_DESCRIPTIONS[DeviceType.UNKNOWN]
    return DEVICE_TYPE_DESCRIPTIONS[device_type]


def get_supported_model_prefixes() -> set[str]:
    """Gets all supported Meraki model prefixes."""
    return {prefix for prefixes in DEVICE_PREFIX_MAPPINGS.keys() for prefix in prefixes}


def get_prefixes_for_device_type(device_type: str) -> set[str]:
    """Gets all model prefixes for a given device type."""
    return {
        prefix
        for prefixes, dtype in DEVICE_PREFIX_MAPPINGS.items()
        if dtype == device_type
        for prefix in prefixes
    }
