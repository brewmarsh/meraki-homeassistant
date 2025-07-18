# /config/custom_components/meraki_ha/meraki_api/_api_client.py
"""
This module provides a centralized client for interacting with the Meraki API,
leveraging the meraki.aio.DashboardAPI.
"""

import logging
import aiohttp
from typing import Any, List, Dict, Optional # Added List, Dict, Optional
from ...patched_meraki_session import PatchedAsyncRestSession
from meraki.aio import AsyncDashboardAPI
from meraki.exceptions import APIError as MerakiSDKAPIError

from .exceptions import (
    MerakiApiError,
    MerakiApiConnectionError,
    MerakiApiAuthError,
    MerakiApiNotFoundError, # Added import
)


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
        self._sdk = AsyncDashboardAPI(
            api_key=api_key,
            base_url="https://api.meraki.com/api/v1",
            output_log=False,
            print_console=False,
            suppress_logging=True,
        )
        self._sdk._session = PatchedAsyncRestSession(
            logger=_LOGGER,
            api_key=api_key,
            base_url="https://api.meraki.com/api/v1",
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
            List[Dict[str, Any]]: Raw list of client dictionaries from the Meraki SDK on success.

        Raises:
            MerakiApiAuthError: If authentication fails (e.g., HTTP 401).
            MerakiApiConnectionError: For connection issues to the Meraki API.
            MerakiApiError: For other Meraki API related errors.
        """
        method_description = f"fetching clients for network {network_id}"
        try:
            return await self._sdk.networks.getNetworkClients(networkId=network_id, **kwargs)
        except MerakiSDKAPIError as e:
            _LOGGER.error(
                f"Meraki SDK API error while {method_description}: {e.message} "
                f"(Status: {e.status}, Reason: {e.reason}, Action: {e.action}, Response: {str(e.response)[:200]})"
            )
            if e.status == 401:
                raise MerakiApiAuthError(f"Authentication failed while {method_description}: {e.message} (Status: {e.status})") from e
            if e.status is None or "Temporary failure in name resolution" in e.message or "Connection timed out" in e.message:
                 raise MerakiApiConnectionError(f"Connection error while {method_description}: {e.message}") from e
            raise MerakiApiError(f"Failed while {method_description}: {e.message} (Status: {e.status})") from e
        except Exception as e:
            _LOGGER.exception(f"Unexpected error while {method_description}: {e}")
            raise MerakiApiError(f"An unexpected error occurred while {method_description}: {e}") from e

    async def get_camera_sense_settings(self, serial: str) -> Dict[str, Any]:
        """Get the sense settings for a camera.

        Args:
            serial: The serial number of the camera.

        Returns:
            Dict[str, Any]: Raw dictionary of sense settings from the Meraki SDK on success.

        Raises:
            MerakiApiAuthError: If authentication fails.
            MerakiApiConnectionError: For connection issues.
            MerakiApiError: For other API errors.
        """
        method_description = f"fetching camera sense settings for device {serial}"
        # _LOGGER.debug("Fetching camera sense settings for device %s", serial) # Removed
        try:
            return await self._sdk.camera.getDeviceCameraSense(serial=serial)
        except MerakiSDKAPIError as e:
            _LOGGER.error(
                f"Meraki SDK API error while {method_description}: {e.message} "
                f"(Status: {e.status}, Reason: {e.reason}, Action: {e.action}, Response: {str(e.response)[:200]})"
            )
            if e.status == 401:
                raise MerakiApiAuthError(f"Authentication failed while {method_description}: {e.message} (Status: {e.status})") from e
            if e.status is None or "Temporary failure in name resolution" in e.message or "Connection timed out" in e.message:
                 raise MerakiApiConnectionError(f"Connection error while {method_description}: {e.message}") from e
            raise MerakiApiError(f"Failed while {method_description}: {e.message} (Status: {e.status})") from e
        except Exception as e:
            _LOGGER.exception(f"Unexpected error while {method_description}: {e}")
            raise MerakiApiError(f"An unexpected error occurred while {method_description}: {e}") from e

    async def get_camera_video_settings(self, serial: str) -> Dict[str, Any]:
        """Get the video settings for a camera.

        Args:
            serial: The serial number of the camera.

        Returns:
            Dict[str, Any]: Raw dictionary of video settings from the Meraki SDK on success.

        Raises:
            MerakiApiAuthError: If authentication fails.
            MerakiApiConnectionError: For connection issues.
            MerakiApiError: For other API errors.
        """
        method_description = f"fetching camera video settings for device {serial}"
        # _LOGGER.debug("Fetching camera video settings for device %s", serial) # Removed
        try:
            return await self._sdk.camera.getDeviceCameraVideoSettings(serial=serial)
        except MerakiSDKAPIError as e:
            _LOGGER.error(
                f"Meraki SDK API error while {method_description}: {e.message} "
                f"(Status: {e.status}, Reason: {e.reason}, Action: {e.action}, Response: {str(e.response)[:200]})"
            )
            if e.status == 401:
                raise MerakiApiAuthError(f"Authentication failed while {method_description}: {e.message} (Status: {e.status})") from e
            if e.status is None or "Temporary failure in name resolution" in e.message or "Connection timed out" in e.message:
                 raise MerakiApiConnectionError(f"Connection error while {method_description}: {e.message}") from e
            raise MerakiApiError(f"Failed while {method_description}: {e.message} (Status: {e.status})") from e
        except Exception as e:
            _LOGGER.exception(f"Unexpected error while {method_description}: {e}")
            raise MerakiApiError(f"An unexpected error occurred while {method_description}: {e}") from e

    async def update_camera_video_settings(
        self, serial: str, rtsp_server_enabled: bool
    ) -> Dict[str, Any]:
        """Update the video settings for a camera.

        Args:
            serial: The serial number of the camera.
            rtsp_server_enabled: Target state for RTSP server.

        Returns:
            Dict[str, Any]: Raw dictionary response from the Meraki SDK after attempting the update.

        Raises:
            MerakiApiAuthError: If authentication fails.
            MerakiApiConnectionError: For connection issues.
            MerakiApiError: For other API errors.
        """
        method_description = f"updating camera video settings for device {serial}"
        # _LOGGER.debug(
        #     "Updating camera video settings for device %s with payload: externalRtspEnabled=%s",
        #     serial,
        #     rtsp_server_enabled,
        # ) # Removed
        try:
            return await self._sdk.camera.updateDeviceCameraVideoSettings(
                serial=serial, externalRtspEnabled=rtsp_server_enabled
            )
        except MerakiSDKAPIError as e:
            _LOGGER.error(
                f"Meraki SDK API error while {method_description}: {e.message} "
                f"(Status: {e.status}, Reason: {e.reason}, Action: {e.action}, Response: {str(e.response)[:200]})"
            )
            if e.status == 401:
                raise MerakiApiAuthError(f"Authentication failed while {method_description}: {e.message} (Status: {e.status})") from e
            if e.status is None or "Temporary failure in name resolution" in e.message or "Connection timed out" in e.message:
                 raise MerakiApiConnectionError(f"Connection error while {method_description}: {e.message}") from e
            raise MerakiApiError(f"Failed while {method_description}: {e.message} (Status: {e.status})") from e
        except Exception as e:
            _LOGGER.exception(f"Unexpected error while {method_description}: {e}")
            raise MerakiApiError(f"An unexpected error occurred while {method_description}: {e}") from e

    async def update_camera_sense_settings(
        self,
        serial: str,
        sense_enabled: bool | None = None,
        audio_detection_enabled: bool | None = None,
    ) -> Dict[str, Any]:
        """Update the sense settings for a camera.

        Args:
            serial: The serial number of the camera.
            sense_enabled: Optional. Target state for MV Sense (`senseEnabled`).
            audio_detection_enabled: Optional. Target state for audio detection
                                     (`audioDetection.enabled`).

        Returns:
            Dict[str, Any]: Raw dictionary response from the Meraki SDK.
            If no settings are provided to update, returns the current settings.

        Raises:
            MerakiApiAuthError: If authentication fails.
            MerakiApiConnectionError: For connection issues.
            MerakiApiError: For other API errors.
        """
        payload = {}
        # Construct payload only with provided (non-None) arguments
        if sense_enabled is not None:
            payload["senseEnabled"] = sense_enabled

        if audio_detection_enabled is not None:
            # The API expects audioDetection to be a dictionary
            payload["audioDetection"] = audio_detection_enabled

        if not payload:
            _LOGGER.debug(
                "No camera sense settings provided to update for device %s. "
                "Returning current settings instead.", serial
            )
            # As per previous logic, if no payload, fetch and return current settings.
            return await self.get_camera_sense_settings(serial)

        method_description = f"updating camera sense settings for device {serial}"
        # _LOGGER.debug(
        #     "Updating camera sense settings for device %s with payload: %s",
        #     serial,
        #     payload,
        # ) # Removed
        try:
            # directly accepts keyword arguments that match the API payload structure.
            return await self._sdk.camera.updateDeviceCameraSense(
                serial=serial, **payload
            )
        except MerakiSDKAPIError as e:
            _LOGGER.error(
                f"Meraki SDK API error while {method_description}: {e.message} "
                f"(Status: {e.status}, Reason: {e.reason}, Action: {e.action}, Response: {str(e.response)[:200]})"
            )
            if e.status == 401:
                raise MerakiApiAuthError(f"Authentication failed while {method_description}: {e.message} (Status: {e.status})") from e
            if e.status is None or "Temporary failure in name resolution" in e.message or "Connection timed out" in e.message:
                 raise MerakiApiConnectionError(f"Connection error while {method_description}: {e.message}") from e
            raise MerakiApiError(f"Failed while {method_description}: {e.message} (Status: {e.status})") from e
        except Exception as e:
            _LOGGER.exception(f"Unexpected error while {method_description}: {e}")
            raise MerakiApiError(f"An unexpected error occurred while {method_description}: {e}") from e

    async def close(self) -> None:
        """Closes the underlying aiohttp session managed by the SDK."""
        # Ensure exc_type, exc_val, exc_tb are passed for a clean exit
        await self._sdk.__aexit__(None, None, None)

    async def async_update_device_tags(self, serial: str, tags: List[str]) -> bool:
        """
        Placeholder for updating device tags.
        The python-meraki SDK's updateDevice method can be used to update tags.
        This method attempts to replace all existing tags with the provided list.

        Args:
            serial: The serial number of the device.
            tags: A list of strings representing the desired tags.

        Returns:
            True if the update was successful, False otherwise (though exceptions are raised on failure).

        Raises:
            MerakiApiAuthError: If authentication fails (HTTP 401).
            MerakiApiNotFoundError: If the device is not found (HTTP 404).
            MerakiApiConnectionError: For connection issues to the Meraki API.
            MerakiApiError: For other Meraki API related errors.
        """
        method_description = f"updating tags for device {serial} to {tags}"
        # _LOGGER.debug("Attempting to %s", method_description) # Removed

        try:
            await self._sdk.devices.updateDevice(serial=serial, tags=tags)
            # _LOGGER.debug("Successfully %s", method_description) # Removed
            return True
        except MerakiSDKAPIError as e:
            _LOGGER.error(
                "Meraki SDK API error while %s: %s (Status: %s, Reason: %s, Action: %s, Response: %s)",
                method_description,
                e.message,
                e.status,
                e.reason,
                e.action,
                str(e.response)[:200],
            )
            if e.status == 401:
                raise MerakiApiAuthError(f"Authentication failed while {method_description}: {e.message} (Status: {e.status})") from e
            elif e.status == 404:
                raise MerakiApiNotFoundError(f"Device {serial} not found while {method_description}: {e.message} (Status: {e.status})") from e
            # Check for connection-related issues based on status or message content
            if e.status is None or "Temporary failure in name resolution" in e.message or "Connection timed out" in e.message:
                 raise MerakiApiConnectionError(f"Connection error while {method_description}: {e.message}") from e
            raise MerakiApiError(f"Failed while {method_description}: {e.message} (Status: {e.status})") from e
        except Exception as e:
            _LOGGER.exception("Unexpected error while %s: %s", method_description, e)
            raise MerakiApiError(f"An unexpected error occurred while {method_description}: {e}") from e


__all__ = [
    "MerakiAPIClient",
    "MerakiApiError",
    "MerakiApiConnectionError",
    "MerakiApiAuthError",
    "MerakiApiNotFoundError", # Added export
]
