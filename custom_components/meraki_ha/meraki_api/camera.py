# /config/custom_components/meraki_ha/meraki_api/camera.py
import logging
from typing import Any, Dict, List
from ._api_client import MerakiAPIClient
from .exceptions import MerakiApiError

_LOGGER = logging.getLogger(__name__)


class MerakiCameraAPI:
    """Meraki camera API functions."""

    def __init__(self, client: MerakiAPIClient):
        """Initialize the Meraki Camera API.

        Args:
            client: An instance of the MerakiAPIClient.
        """
        self._client = client

    async def async_get_device_camera_snapshot(
        self, serial: str, fullframe: bool = False
    ) -> bytes:
        """Take a snapshot of what the camera last saw.

        Args:
            serial: Serial number of the Meraki camera.
            fullframe: Boolean indicating if the full frame should be returned.
                         Defaults to False (cropped snapshot).

        Returns:
            bytes: The image data of the snapshot.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/devices/{serial}/camera/snapshot"
        url = f"{self._client._base_url}{endpoint}"
        headers = {"X-Cisco-Meraki-API-Key": self._client._api_key}
        params = {"fullframe": str(fullframe).lower()}
        try:
            response = await self._client._async_meraki_request(
                "GET", url, headers, params=params
            )
            return response
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error fetching camera snapshot for device '{serial}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching camera snapshot for device '{serial}': {e}"
            ) from e

    async def async_get_network_cameras(self, network_id: str) -> List[Dict[str, Any]]:
        """List the cameras in a network.

        Args:
            network_id: The ID of the Meraki network.

        Returns:
            A list of dictionaries, where each dictionary represents a camera.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/cameras"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            return await self._client._async_meraki_request("GET", url, headers)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error fetching cameras for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching cameras for network '{network_id}': {e}"
            ) from e

    async def async_get_network_camera(
        self, network_id: str, camera_id: str
    ) -> Dict[str, Any]:
        """Return a camera.

        Args:
            network_id: The ID of the Meraki network.
            camera_id: The ID of the camera.

        Returns:
            A dictionary representing the specified camera.

        Raises:
            MerakiApiError: If an error occurs during the API call.
        """
        endpoint = f"/networks/{network_id}/cameras/{camera_id}"
        url = f"{self._client._base_url}{endpoint}"
        headers = {
            "X-Cisco-Meraki-API-Key": self._client._api_key,
            "Content-Type": "application/json",
        }
        try:
            return await self._client._async_meraki_request("GET", url, headers)
        except MerakiApiError:
            raise
        except Exception as e:
            _LOGGER.error(
                f"Unexpected error fetching camera '{camera_id}' for network '{network_id}': {e}"
            )
            raise MerakiApiError(
                f"Unexpected error fetching camera '{camera_id}' for network '{network_id}': {e}"
            ) from e

    # Add other camera-related API calls here as needed.
    # Examples:
    # - async_get_device_camera_analytics_live(...)
    # - async_get_network_camera_quality_retention_profiles(...)
    # - async_get_network_camera_schedules(...)
