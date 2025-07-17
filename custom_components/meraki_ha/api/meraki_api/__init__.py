# /config/custom_components/meraki_ha/meraki_api/__init__.py
"""Meraki API client and exceptions."""

from ._api_client import MerakiAPIClient
from .exceptions import (
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
