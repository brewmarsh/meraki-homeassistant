"""Utility functions for formatting device names in the Meraki Home Assistant integration."""

import logging
from typing import Optional

from custom_components.meraki_ha.coordinators.meraki_device_types import (
    map_meraki_model_to_device_type,
)

_LOGGER = logging.getLogger(__name__)


def format_device_name(
    device_name_raw: Optional[str],
    device_model: Optional[str],
    device_name_format_option: Optional[str],
    is_org_device: bool = False,
) -> str:
    """Formats the device name based on user's preference and device type.

    Args:
        device_name_raw: The raw name of the device (e.g., from API or a default).
                         Expected type: str.
        device_model: The model of the device (e.g., "MR33", "MS220-8P").
                      For the Organization device, this can be "Organization".
                      Expected type: str.
        device_name_format_option: User's preference for name formatting.
                                   Expected: "prefix", "suffix", or "omitted".
                                   Expected type: str.
        is_org_device: True if the device is the Organization itself.
                       Expected type: bool.

    Returns:
        The formatted device name string. Returns "Unnamed Device" or a partially
        formatted name if critical inputs are invalid.
    """
    original_device_name_raw = device_name_raw # For logging original value

    if not isinstance(is_org_device, bool):
        _LOGGER.warning(
            "Invalid type for 'is_org_device' (expected bool, got %s: %s). Defaulting to False.",
            type(is_org_device).__name__, is_org_device
        )
        is_org_device = False

    if not isinstance(device_name_raw, str) or not device_name_raw:
        _LOGGER.warning(
            "Invalid or empty 'device_name_raw' (expected non-empty str, got %s: %s). Defaulting to 'Unnamed Device'.",
            type(device_name_raw).__name__, original_device_name_raw
        )
        # Even if it's not a string, the prefix/suffix logic might still apply to "Unnamed Device"
        device_name_raw = "Unnamed Device"

    if not isinstance(device_model, str):
        _LOGGER.warning(
            "Invalid type for 'device_model' (expected str, got %s: %s for device '%s'). Defaulting to empty string for model processing.",
            type(device_model).__name__, device_model, original_device_name_raw
        )
        device_model = "" # map_meraki_model_to_device_type expects string

    valid_format_options = ["prefix", "suffix", "omitted"]
    if not isinstance(device_name_format_option, str) or device_name_format_option not in valid_format_options:
        _LOGGER.warning(
            "Invalid 'device_name_format_option' (expected one of %s, got %s: %s for device '%s'). Defaulting to 'omitted'.",
            valid_format_options, type(device_name_format_option).__name__, device_name_format_option, original_device_name_raw
        )
        device_name_format_option = "omitted"

    # Actual formatting logic starts here
    if is_org_device:
        if device_name_format_option == "prefix":
            return f"[Org] {device_name_raw}"
        elif device_name_format_option == "suffix":
            return f"{device_name_raw} [Org]"
        else:  # "omitted"
            return device_name_raw
    else:
        # For physical devices (APs, switches, gateways, etc.)
        # device_model is now guaranteed to be a string
        device_type_mapped = map_meraki_model_to_device_type(device_model)

        if device_name_format_option == "prefix" and device_type_mapped != "Unknown":
            return f"[{device_type_mapped}] {device_name_raw}"
        elif device_name_format_option == "suffix" and device_type_mapped != "Unknown":
            return f"{device_name_raw} [{device_type_mapped}]"
        else:  # "omitted" or if device_type_mapped is "Unknown"
            return device_name_raw
