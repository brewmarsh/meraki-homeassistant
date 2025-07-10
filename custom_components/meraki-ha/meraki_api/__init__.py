# /config/custom_components/meraki-ha/meraki_api/__init__.py
"""Meraki API client and exceptions."""

from custom_components.meraki-ha.meraki-api._api_client import MerakiAPIClient
from custom_components.meraki-ha.meraki-api.exceptions import (
    MerakiApiError,  # Alias for MerakiApiException
    MerakiApiException,  # Base exception
    MerakiApiConnectionError,
    MerakiApiAuthError,
    MerakiApiNotFoundError,
    MerakiApiRateLimitError,
    MerakiApiServerError,
)

__all__ = [
    "MerakiAPIClient",
    "MerakiApiError",
    "MerakiApiException",
    "MerakiApiConnectionError",
    "MerakiApiAuthError",
    "MerakiApiNotFoundError",
    "MerakiApiRateLimitError",
    "MerakiApiServerError",
]
