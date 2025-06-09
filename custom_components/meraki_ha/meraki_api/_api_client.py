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

    async def get_network_clients(self, network_id: str, **kwargs) -> Any:
        """Get the clients of a network.

        Args:
            network_id: The ID of the network.
            kwargs: Additional arguments to pass to the API call.

        Returns:
            The clients of the network.
        """
        try:
            return await self._sdk.networks.getNetworkClients(networkId=network_id, **kwargs)
        except Exception as e:
            _LOGGER.error(f"Error fetching clients for network {network_id}: {e}")
            # Depending on desired error handling, you might raise a custom exception
            # or return a specific value like None or an empty list.
            # For now, re-raising the exception to be handled by the caller.
            raise MerakiApiError(f"Failed to fetch clients for network {network_id}: {e}") from e

    async def get_camera_sense_settings(self, serial: str) -> Any:
        """Get the sense settings for a camera.

        Args:
            serial: The serial number of the camera.

        Returns:
            The sense settings for the camera.
        """
        try:
            _LOGGER.debug("Fetching camera sense settings for device %s", serial)
            return await self._sdk.camera.getDeviceCameraSense(serial=serial)
        except Exception as e:
            _LOGGER.error("Error fetching camera sense settings for device %s: %s", serial, e)
            raise MerakiApiError(
                f"Failed to fetch camera sense settings for device {serial}: {e}"
            ) from e

    async def update_camera_sense_settings(
        self,
        serial: str,
        sense_enabled: bool | None = None,
        audio_detection_enabled: bool | None = None,
    ) -> Any:
        """Update the sense settings for a camera.

        Args:
            serial: The serial number of the camera.
            sense_enabled: Optional. Target state for MV Sense (`senseEnabled`).
            audio_detection_enabled: Optional. Target state for audio detection
                                     (`audioDetection.enabled`).

        Returns:
            The response from the Meraki API after attempting the update.
            If no settings are provided to update, returns the current settings.

        Raises:
            MerakiApiError: If the API call fails.
        """
        payload = {}
        # Construct payload only with provided (non-None) arguments
        if sense_enabled is not None:
            payload["senseEnabled"] = sense_enabled

        if audio_detection_enabled is not None:
            # The API expects audioDetection to be a dictionary
            payload.setdefault("audioDetection", {})["enabled"] = audio_detection_enabled

        if not payload:
            _LOGGER.debug(
                "No camera sense settings provided to update for device %s. "
                "Returning current settings instead.", serial
            )
            # As per previous logic, if no payload, fetch and return current settings.
            return await self.get_camera_sense_settings(serial)

        _LOGGER.debug(
            "Updating camera sense settings for device %s with payload: %s",
            serial,
            payload,
        )
        try:
            # The meraki.aio SDK's updateDeviceCameraSense method
            # directly accepts keyword arguments that match the API payload structure.
            return await self._sdk.camera.updateDeviceCameraSense(
                serial=serial, **payload
            )
        except Exception as e: # Catch specific meraki.APIError if possible/preferred
            _LOGGER.error(
                "Error updating camera sense settings for device %s: %s", serial, e
            )
            raise MerakiApiError(
                f"Failed to update camera sense settings for device {serial}: {e}"
            ) from e

    async def close(self) -> None:
        """Closes the underlying aiohttp session managed by the SDK."""
        # Ensure exc_type, exc_val, exc_tb are passed for a clean exit
        await self._sdk.__aexit__(None, None, None)


# Update __all__ based on the refactored client.
# MerakiApiError might be kept if it serves as a custom base error for the
# integration.
__all__ = ["MerakiAPIClient", "MerakiApiError"]
