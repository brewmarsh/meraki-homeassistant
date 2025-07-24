"""Helper functions for the Meraki Home Assistant integration."""

import logging
from typing import Any, Dict
from meraki.exceptions import APIError as MerakiSDKAPIError  # type: ignore

_LOGGER = logging.getLogger(__name__)


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
