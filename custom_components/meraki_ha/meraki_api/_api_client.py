"""
This module provides a centralized function for making asynchronous requests to the Meraki API.
It also manages the aiohttp ClientSession.
"""

import logging
import aiohttp
from typing import Any, Dict, Optional

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


async def _async_meraki_request(
    api_key: str,
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Makes an asynchronous request to the Meraki API using a centralized session.

    Args:
        api_key: The Meraki API key. [cite: 1, 2]
        method: The HTTP method to use (e.g., "GET", "POST", "PUT", "DELETE").
        endpoint: The API endpoint (e.g., "/networks/{networkId}/wireless/ssids").
        data: (Optional) The data to send in the request body (for POST, PUT).
        params: (Optional) Query parameters to include in the URL.

    Returns:
        The JSON response from the API.

    Raises:
        aiohttp.ClientResponseError: If the API returns an error status code.
        Exception: For other errors during the API request.
    """

    session = await _get_client_session()  # Get the session
    url = f"{MERAKI_API_URL}{endpoint}"
    headers = {
        "X-Cisco-Meraki-API-Key": api_key,
        "Content-Type": "application/json",
    }

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
            try:
                response_json = await response.json()
                _LOGGER.debug(f"Response body: {response_json}")
                return response_json
            except aiohttp.ContentTypeError:
                response_text = await response.text()
                _LOGGER.debug(f"Response body (non-JSON): {response_text}")
                return response_text
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return await response.json()
    except aiohttp.ClientResponseError as err:
        _LOGGER.error(
            "Meraki API request failed with status %s: %s", err.status, err.message
        )  # Log detailed error
        raise
    except aiohttp.ClientConnectionError as err:
        _LOGGER.error("Could not connect to Meraki API: %s", err)
        raise
    except Exception as err:
        _LOGGER.exception("Unexpected error during Meraki API request: %s", err)
        raise
