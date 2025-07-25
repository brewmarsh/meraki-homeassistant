"""Utility functions for formatting device names in the Meraki Home Assistant integration."""


from ..meraki_device_types import (
    map_meraki_model_to_device_type,
)
import logging
from typing import Any, Dict
from meraki.exceptions import APIError as MerakiSDKAPIError  # type: ignore

_LOGGER = logging.getLogger(__name__)


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


def _is_network_feature_not_found(error: MerakiSDKAPIError) -> bool:
    """Determine if the error is due to a network feature not being found.

    Args:
        error: The MerakiSDKAPIError instance to check.

    Returns:
        True if the error indicates a network feature not found, False otherwise.
    """
    # Check if the error message or reason indicates a feature not found scenario
    return (
        error.status == 404
        and "not found" in (error.reason or "").lower()
        and "feature" in (error.message or "").lower()
    )


def _is_valid_device(device: Dict[str, Any]) -> bool:
    """Check if the device dictionary has all required attributes.

    Args:
        device: The device dictionary to check.

    Returns:
        True if the device is valid, False otherwise.
    """
    required_attributes = ["serial", "model", "mac", "name"]
    return all(
        attr in device and device[attr] is not None for attr in required_attributes
    )


def _log_skipped_device(device: Dict[str, Any], reason: str) -> None:
    """Log a skipped device due to missing attributes or other issues.

    Args:
        device: The device dictionary that was skipped.
        reason: The reason why the device was skipped.
    """
    _LOGGER.info(
        "Skipping device %s (Serial: %s, MAC: %s) - %s",
        device.get("name", "Unknown"),
        device.get("serial", "Unknown"),
        device.get("mac", "Unknown"),
        reason,
    )
