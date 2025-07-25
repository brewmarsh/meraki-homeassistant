"""Helper functions for the Meraki API data fetcher."""

import logging
from typing import Any, Dict
from meraki.exceptions import APIError as MerakiSDKAPIError

_LOGGER = logging.getLogger(__name__)


def is_network_feature_not_found(error: MerakiSDKAPIError) -> bool:
    """Determine if the error is due to a network feature not being found."""
    return (
        error.status == 404
        and "not found" in (error.reason or "").lower()
        and "feature" in (error.message or "").lower()
    )


def is_valid_device(device: Dict[str, Any]) -> bool:
    """Check if the device dictionary has all required attributes."""
    required_attributes = ["serial", "model", "mac", "name"]
    return all(
        attr in device and device[attr] is not None for attr in required_attributes
    )


def log_skipped_device(device: Dict[str, Any], reason: str) -> None:
    """Log a skipped device due to missing attributes or other issues."""
    _LOGGER.info(
        "Skipping device %s (Serial: %s, MAC: %s) - %s",
        device.get("name", "Unknown"),
        device.get("serial", "Unknown"),
        device.get("mac", "Unknown"),
        reason,
    )
