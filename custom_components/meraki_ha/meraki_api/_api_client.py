# /config/custom_components/meraki_ha/meraki_api/_api_client.py
"""
This module provides a centralized client for interacting with the Meraki API,
leveraging the meraki.aio.DashboardAPI.
"""

import logging
from typing import Any

from meraki.aio import AsyncDashboardAPI  # Changed from DashboardAPI
# Assuming MerakiApiError might still be used as a base custom error for the integration.
# If not, this can be removed in a later step if all error handling is
# done via meraki.APIError
from .exceptions import MerakiApiError


_LOGGER = logging.getLogger(__name__)


class MerakiAPIClient:
    """Central client for interacting with the Meraki API using meraki.aio.DashboardAPI."""

    def __init__(self, api_key: str, org_id: str) -> None:
        """Initialize the Meraki API client.

        Args:
            api_key (str): The Meraki API key.
            org_id (str): The Meraki organization ID.
        """
        self._api_key = api_key
        self._org_id = org_id  # Store org_id if needed for specific calls

        # Initialize the Meraki SDK
        self._sdk = AsyncDashboardAPI(  # Changed from DashboardAPI
            api_key=api_key,
            base_url="https://api.meraki.com/api/v1",  # Standard base URL
            output_log=False,  # Set to True for SDK-level debug logging if needed
            print_console=False,  # Set to True for SDK-level console output if needed
            suppress_logging=True,  # Prefer HA's logging mechanisms
            # org_id is generally passed to specific SDK method calls
        )

    @property
    def org_id(self) -> str:
        """Returns the organization ID."""
        return self._org_id

    @property
    def appliance(self) -> Any:
        """Provides access to the SDK's appliance controller."""
        return self._sdk.appliance

    @property
    def camera(self) -> Any:
        """Provides access to the SDK's camera controller."""
        return self._sdk.camera

    @property
    def devices(self) -> Any:
        """Provides access to the SDK's devices controller."""
        return self._sdk.devices

    @property
    def networks(self) -> Any:
        """Provides access to the SDK's networks controller."""
        return self._sdk.networks

    @property
    # Or a more specific type like 'OrganizationsController' if known
    def organizations(self) -> Any:
        """Provides access to the SDK's organizations controller."""
        return self._sdk.organizations

    @property
    def sensor(self) -> Any:
        """Provides access to the SDK's sensor controller."""
        return self._sdk.sensor

    @property
    def switch(self) -> Any:
        """Provides access to the SDK's switch controller."""
        return self._sdk.switch

    @property
    def wireless(self) -> Any:
        """Provides access to the SDK's wireless controller."""
        return self._sdk.wireless

    async def close(self) -> None:
        """Closes the underlying aiohttp session managed by the SDK."""
        # Ensure exc_type, exc_val, exc_tb are passed for a clean exit
        await self._sdk.__aexit__(None, None, None)


# Update __all__ based on the refactored client.
# MerakiApiError might be kept if it serves as a custom base error for the
# integration.
__all__ = ["MerakiAPIClient", "MerakiApiError"]
