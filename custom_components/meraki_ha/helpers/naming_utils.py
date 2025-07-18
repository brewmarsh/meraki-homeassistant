"""Utility functions for formatting device names in the Meraki Home Assistant integration."""

from typing import Optional

from .coordinators.meraki_device_types import (
    map_meraki_model_to_device_type,
)


def format_device_name(
    device_name_raw: str,
    device_model: str,  # For physical devices, model string; for Org, could be "Organization"
    device_name_format_option: str,
    is_org_device: bool = False,
) -> str:
    """Formats the device name based on user's preference and device type.

    Args:
        device_name_raw: The raw name of the device (e.g., from API or a default).
        device_model: The model of the device (e.g., "MR33", "MS220-8P").
                      For the Organization device, this can be "Organization".
        device_name_format_option: User's preference for name formatting
                                   ("prefix", "suffix", "omitted").
        is_org_device: True if the device is the Organization itself.

    Returns:
        The formatted device name string.
    """
    if not device_name_raw:  # Should not happen if called correctly, but as a safeguard
        return "Unnamed Device"

    if is_org_device:
        if device_name_format_option == "prefix":
            return f"[Org] {device_name_raw}"
        elif device_name_format_option == "suffix":
            return f"{device_name_raw} [Org]"
        else:  # "omitted" or any other value
            return device_name_raw
    else:
        # For physical devices (APs, switches, gateways, cameras, etc.)
        device_type_mapped = map_meraki_model_to_device_type(device_model or "")

        # Apply prefix/suffix only if the device type is known and user selected that option.
        # If the device type is "Unknown", the raw name is returned to avoid unhelpful "[Unknown]" tags.
        if device_name_format_option == "prefix" and device_type_mapped != "Unknown":
            return f"[{device_type_mapped}] {device_name_raw}"
        elif device_name_format_option == "suffix" and device_type_mapped != "Unknown":
            return f"{device_name_raw} [{device_type_mapped}]"
        else:  # "omitted" or if device_type_mapped is "Unknown" or any other format option
            return device_name_raw
