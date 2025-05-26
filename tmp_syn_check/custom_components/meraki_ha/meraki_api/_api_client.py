# /config/custom_components/meraki_ha/meraki_api/_api_client.py
"""
This module provides a centralized client for interacting with the Meraki API,
managing API requests and the aiohttp ClientSession.
"""

import logging
import aiohttp
from typing import Any, Dict, Optional

from .exceptions import MerakiApiError
from .appliance import MerakiApplianceAPI
from .clients import MerakiClientsAPI
from .devices import MerakiDevicesAPI
from .wireless import MerakiWirelessAPI
from .switch import MerakiSwitchAPI
from .camera import MerakiCameraAPI
from .sensor import MerakiSensorAPI
from .networks import MerakiNetworksAPI

_LOGGER = logging.getLogger(__name__)

MERAKI_API_URL = "https://api.meraki.com/api/v1"  # [cite: 1] Base URL for Meraki API

_CLIENT_SESSION: Optional[aiohttp.ClientSession] = None  # Module-level session


async def _get_client_session() -> aiohttp.ClientSession:
    """
    Get or create the aiohttp ClientSession.
    """
    global _CLIENT_SESSION
    if _CLIENT_SESSION is None or _CLIENT_SESSION.closed:
        _CLIENT_SESSION = aiohttp.ClientSession()
    return _CLIENT_SESSION


async def _close_client_session() -> None:
    """
    Close the aiohttp ClientSession.
    """
    global _CLIENT_SESSION
    if _CLIENT_SESSION:
        await _CLIENT_SESSION.close()
        _CLIENT_SESSION = None


async def _async_api_request(
    method: str,
    url: str,  # Now expects the full URL
    headers: Dict[str, str],  # Now expects the headers to be passed
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Makes an asynchronous request to the Meraki API using a centralized session.

    Args:
        method: The HTTP method to use (e.g., "GET", "POST", "PUT", "DELETE").
        url: The full URL to the API endpoint.
        headers: A dictionary of HTTP headers to include in the request.
        data: (Optional) The data to send in the request body (for POST, PUT).
        params: (Optional) Query parameters to include in the URL.

    Returns:
        The JSON response from the API (or bytes for binary data).

    Raises:
        aiohttp.ClientResponseError: If the API returns an error status code.
        Exception: For other errors during the API request.
    """

    session = await _get_client_session()  # Get the session

    _LOGGER.debug(
        "Making %s request to %s with params=%s and data=%s",
        method,
        url,
        params,
        data,
    )  # Log request details
    _LOGGER.debug(f"Request headers: {headers}")

    try:
        async with session.request(
            method, url, headers=headers, json=data, params=params
        ) as response:
            _LOGGER.debug(f"Response from {response.url}: Status - {response.status}")
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            if response.content_type == "application/json":
                response_json = await response.json()
                _LOGGER.debug(f"Response body (JSON): {response_json}")
                return response_json
            else:
                response_text = await response.text()
                _LOGGER.debug(f"Response body (non-JSON): {response_text}")
                return response_text
    except aiohttp.ClientResponseError as err:
        _LOGGER.error(
            "Meraki API request failed with status %s: %s for URL: %s",
            err.status,
            err.message,
            url,
        )  # Log detailed error with URL
        raise MerakiApiError(f"API error: {err}")
    except aiohttp.ClientConnectionError as err:
        _LOGGER.error("Could not connect to Meraki API: %s for URL: %s", err, url)
        raise MerakiApiError(f"Connection error: {err}")
    except Exception as err:
        _LOGGER.exception(
            "Unexpected error during Meraki API request to %s: %s", url, err
        )
        raise MerakiApiError(f"Unexpected error: {err}")


class MerakiAPIClient:
    """Central client for interacting with the Meraki API."""

    def __init__(self, api_key: str, org_id: str) -> None:
        """Initialize the Meraki API client.

        Args:
            api_key (str): The Meraki API key.
            org_id (str): The Meraki organization ID.
        """
        self._api_key = api_key
        self._org_id = org_id
        self._base_url = "https://api.meraki.com/api/v1"  # Consider making this configurable if needed
        self.appliance = MerakiApplianceAPI(self)
        self.clients = MerakiClientsAPI(self)
        self.devices = MerakiDevicesAPI(self)
        self.wireless = MerakiWirelessAPI(self)
        self.switch = MerakiSwitchAPI(self)
        self.camera = MerakiCameraAPI(self)
        self.sensor = MerakiSensorAPI(self)
        self.networks = MerakiNetworksAPI(self)

    async def _async_meraki_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> Any:
        """Internal method to make asynchronous Meraki API requests.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST").
            endpoint (str): The API endpoint path (relative to the base URL).
            params (dict, optional): Query parameters for the request. Defaults to None.
            json (dict, optional): JSON data for the request body (for POST, PUT). Defaults to None.

        Returns:
            dict | list: The JSON response from the Meraki API.

        Raises:
            MerakiApiError: If there is an error communicating with the Meraki API.
        """
        headers = {
            "X-Cisco-Meraki-API-Key": self._api_key,
            "Content-Type": "application/json",
        }
        url = f"{self._base_url}{endpoint}"
        return await _async_api_request(method, url, headers, params=params, data=json)


__all__ = [
    "MerakiAPIClient",
    "MerakiApiError",
]
