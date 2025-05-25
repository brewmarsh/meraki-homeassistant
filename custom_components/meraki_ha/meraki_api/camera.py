"""Provides an interface to Meraki Camera-specific API endpoints.

This module contains the `MerakiCameraAPI` class, which encapsulates methods
for interacting with Meraki API endpoints related to MV series smart cameras.
This includes functionalities like taking snapshots and listing cameras
within a network.
"""
import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional # Added Optional

from .exceptions import MerakiApiError

if TYPE_CHECKING:
    # Avoids circular import with _api_client.py for type hinting
    from ._api_client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class MerakiCameraAPI:
    """Encapsulates Meraki Camera (MV) related API calls.

    This class provides methods to interact with Meraki smart cameras,
    such as retrieving snapshots and listing camera devices. It utilizes
    an instance of `MerakiAPIClient` for API communication.
    """

    def __init__(self, client: "MerakiAPIClient") -> None:
        """Initialize the Meraki Camera API interface.

        Args:
            client: An instance of `MerakiAPIClient` for making API requests.
        """
        self._client: "MerakiAPIClient" = client

    async def async_get_device_camera_snapshot(
        self, serial: str, timestamp: Optional[str] = None # Added timestamp as per API
    ) -> Optional[Dict[str, Any]]: # API returns JSON with URL, not bytes directly
        """Generate a snapshot of what the camera sees at the specified time.

        If no timestamp is specified, it takes a snapshot of the camera's current view.
        The API returns a JSON object with a URL to the snapshot. The image itself
        would need to be fetched from that URL.

        Reference: https://developer.cisco.com/meraki/api-v1/#!generate-device-camera-snapshot

        Args:
            serial: The serial number of the Meraki camera.
            timestamp: (Optional) The timestamp for the snapshot, in ISO8601 format.
                       If omitted, a snapshot of the current time is taken.

        Returns:
            A dictionary containing the snapshot information (e.g., URL to the image)
            if the request is successful. Returns `None` if the snapshot generation
            fails or the device is not found (e.g., API returns 404).
            The structure is defined by the Meraki API. Example: `{"url": "..."}`.

        Raises:
            MerakiApiError: If an error occurs during the API call, other than 404
                            when the device itself isn't found for snapshot generation.
        """
        endpoint = f"/devices/{serial}/camera/generateSnapshot" # Corrected endpoint
        payload: Dict[str, Any] = {}
        if timestamp:
            payload["timestamp"] = timestamp
        # fullframe parameter was for a different endpoint /camera/snapshot which is deprecated or different.
        # generateSnapshot is the current recommended way.

        _LOGGER.debug(
            "Generating camera snapshot for device serial: %s, timestamp: %s",
            serial,
            timestamp or "now",
        )
        try:
            # This endpoint is a POST request to generate the snapshot link.
            return await self._client._async_meraki_request(
                method="POST", endpoint=endpoint, json=payload # Use json for POST payload
            )
        except MerakiApiError as e:
            # Handle 404 for device not found specifically if needed, otherwise re-raise
            if "404" in str(e):
                 _LOGGER.warning("Camera with serial '%s' not found for snapshot generation.", serial)
                 return None
            _LOGGER.error(
                "Meraki API error generating camera snapshot for device '%s': %s",
                serial,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error generating camera snapshot for device '%s': %s",
                serial,
                e,
            )
            raise MerakiApiError(
                f"Unexpected error for device '{serial}' camera snapshot: {e}"
            ) from e

    async def async_get_network_cameras(
        self, network_id: str
    ) -> List[Dict[str, Any]]:
        """List all cameras in a specific Meraki network.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-network-cameras

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a camera
            device. Returns an empty list if no cameras are found or if an
            error occurs. The structure is defined by the Meraki API.

        Raises:
            MerakiApiError: If a critical error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/cameras"
        _LOGGER.debug("Fetching cameras for network ID: %s", network_id)
        try:
            response = await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
            return response if isinstance(response, list) else []
        except MerakiApiError as e:
            _LOGGER.error(
                "Meraki API error fetching cameras for network '%s': %s", network_id, e
            )
            # Depending on desired behavior, could return [] or re-raise.
            # If one network failing shouldn't stop others, returning [] might be preferred for list methods.
            raise # Or return [] if non-critical
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching cameras for network '%s': %s", network_id, e
            )
            raise MerakiApiError(
                f"Unexpected error for network '{network_id}' cameras: {e}"
            ) from e

    async def async_get_device_camera_details( # Renamed from get_network_camera for clarity
        self, serial: str # Changed from network_id, camera_id to just serial
    ) -> Optional[Dict[str, Any]]:
        """Return details for a specific camera device.

        Uses the generic device details endpoint, as camera-specific details
        are often part of the main device object.

        Reference: https://developer.cisco.com/meraki/api-v1/#!get-device

        Args:
            serial: The serial number of the camera device.

        Returns:
            A dictionary representing the specified camera's details if found.
            Returns `None` if the camera is not found (e.g., API returns 404).
            The structure is defined by the Meraki API.

        Raises:
            MerakiApiError: If an error occurs during the API call, other than 404.
        """
        endpoint = f"/devices/{serial}" # Generic device endpoint
        _LOGGER.debug("Fetching details for camera device serial: %s", serial)
        try:
            return await self._client._async_meraki_request(
                method="GET", endpoint=endpoint
            )
        except MerakiApiError as e:
            if "404" in str(e): # Basic check for 404
                _LOGGER.warning(
                    "Camera with serial '%s' not found. API response: %s", serial, e
                )
                return None
            _LOGGER.error(
                "Meraki API error fetching details for camera '%s': %s", serial, e
            )
            raise
        except Exception as e:
            _LOGGER.exception(
                "Unexpected error fetching details for camera '%s': %s", serial, e
            )
            raise MerakiApiError(
                f"Unexpected error for camera '{serial}' details: {e}"
            ) from e

    # Add other camera-related API calls here as needed.
    # Examples from Meraki documentation:
    # - async_get_device_camera_video_link(self, serial: str) -> Optional[Dict[str, Any]]:
    #   Endpoint: /devices/{serial}/camera/videoLink
    # - async_update_device_camera_custom_analytics(self, serial: str, parameters: Dict) -> Dict:
    #   Endpoint: /devices/{serial}/camera/customAnalytics
    # - async_get_network_camera_quality_retention_profiles(self, network_id: str) -> List[Dict[str, Any]]:
    #   Endpoint: /networks/{networkId}/camera/qualityRetentionProfiles
    # - async_update_network_camera_wireless_profile(self, network_id: str, wireless_profile_id: str, name: str, ...) -> Dict:
    #   Endpoint: /networks/{networkId}/camera/wirelessProfiles/{wirelessProfileId}
