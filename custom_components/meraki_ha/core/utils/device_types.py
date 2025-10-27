"""
Utility functions for classifying Meraki device models.

This module re-exports the constants, data structures, and functions
from the internal _const, _data, and _mappers modules.
"""

from ._const import (
    DEVICE_TYPE_APPLIANCE,
    DEVICE_TYPE_CAMERA,
    DEVICE_TYPE_CELLULAR,
    DEVICE_TYPE_NETWORK,
    DEVICE_TYPE_SENSOR,
    DEVICE_TYPE_SSID,
    DEVICE_TYPE_SWITCH,
    DEVICE_TYPE_UNKNOWN,
    DEVICE_TYPE_WIRELESS,
    VALID_DEVICE_TYPES,
    DeviceType,
)
from ._data import (
    DEVICE_PREFIX_MAPPINGS,
    DEVICE_TYPE_DESCRIPTIONS,
    MODEL_PATTERN,
)
from ._mappers import (
    get_device_type_description,
    get_prefixes_for_device_type,
    get_supported_model_prefixes,
    map_meraki_model_to_device_type,
    validate_device_type,
    validate_model_string,
)

__all__ = [
    "DeviceType",
    "VALID_DEVICE_TYPES",
    "DEVICE_TYPE_WIRELESS",
    "DEVICE_TYPE_SWITCH",
    "DEVICE_TYPE_APPLIANCE",
    "DEVICE_TYPE_CAMERA",
    "DEVICE_TYPE_SENSOR",
    "DEVICE_TYPE_CELLULAR",
    "DEVICE_TYPE_NETWORK",
    "DEVICE_TYPE_SSID",
    "DEVICE_TYPE_UNKNOWN",
    "DEVICE_PREFIX_MAPPINGS",
    "DEVICE_TYPE_DESCRIPTIONS",
    "MODEL_PATTERN",
    "map_meraki_model_to_device_type",
    "validate_model_string",
    "validate_device_type",
    "get_device_type_description",
    "get_supported_model_prefixes",
    "get_prefixes_for_device_type",
]
