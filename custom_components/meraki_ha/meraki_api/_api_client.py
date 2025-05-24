"""Provides a centralized asynchronous client for interacting with the Meraki API.

This module handles the creation and management of an `aiohttp.ClientSession`
for making HTTP requests to the Meraki Dashboard API. It includes a core
function `_async_meraki_request` that abstracts the request logic,
handling authentication, URL construction, and error logging.
"""

import logging
import aiohttp
from typing import Any, Dict, Optional

_LOGGER = logging.getLogger(__name__)

MERAKI_API_URL = "https://api.meraki.com/api/v1"  # [cite: 1] Base URL for Meraki API

_CLIENT_SESSION: Optional[aiohttp.ClientSession] = None  # Module-level session


async def _get_client_session() -> aiohttp.ClientSession:
    """Retrieves or creates the global aiohttp ClientSession.

    Ensures that a single, reusable `aiohttp.ClientSession` is used for all
    API requests, improving efficiency by reusing connections. If the session
    does not exist or has been closed, a new one is created.

    Returns:
        aiohttp.ClientSession: The active aiohttp client session.
    """
    global _CLIENT_SESSION
    if _CLIENT_SESSION is None or _CLIENT_SESSION.closed:
        # Create a new session if one doesn't exist or the previous one is closed.
        _CLIENT_SESSION = aiohttp.ClientSession()
    return _CLIENT_SESSION


async def _close_client_session() -> None:
    """Closes the global aiohttp ClientSession.

    If an active session exists, this function closes it and resets the
    global `_CLIENT_SESSION` variable to None. This is typically called
    during application shutdown or when a new configuration requires
    re-initialization of the session.
    """
    global _CLIENT_SESSION
    if _CLIENT_SESSION:
        await _CLIENT_SESSION.close()
        _CLIENT_SESSION = None  # Reset the global session variable.


async def _async_meraki_request(
    api_key: str,
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Any:
    """Makes an asynchronous HTTP request to a specified Meraki API endpoint.

    This function uses a globally managed `aiohttp.ClientSession` to send
    requests. It constructs the full URL, includes necessary headers
    (including the API key), and handles JSON request bodies and URL parameters.

    Args:
        api_key (str): The Meraki API key for authentication. [cite: 1, 2]
        method (str): The HTTP method to use (e.g., "GET", "POST", "PUT", "DELETE").
        endpoint (str): The API endpoint path (e.g., "/networks/{networkId}/wireless/ssids").
        data (Optional[Dict[str, Any]]): A dictionary of data to send in the
            request body, typically for "POST" or "PUT" methods. Defaults to None.
        params (Optional[Dict[str, Any]]): A dictionary of query parameters to
            append to the URL. Defaults to None.

    Returns:
        Any: The JSON response from the API, parsed into Python objects.

    Raises:
        aiohttp.ClientResponseError: If the API returns an HTTP error status
            (e.g., 4xx or 5xx).
        aiohttp.ClientConnectionError: If there's an issue connecting to the API
            (e.g., DNS resolution failure, network unreachable).
        Exception: For other unexpected errors that occur during the request process.
    """

    session = await _get_client_session()  # Obtain the shared client session.
    url = f"{MERAKI_API_URL}{endpoint}"  # Construct the full API URL.
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

    try:
        async with session.request(
            method, url, headers=headers, json=data, params=params
        ) as response:
            response.raise_for_status()  # Raises an exception for 4xx/5xx status codes.
            return await response.json()  # Parse and return the JSON response.
    except aiohttp.ClientResponseError as err:
        # Log specific details for HTTP errors.
        _LOGGER.error(
            "Meraki API request to %s failed with status %s: %s",
            url,
            err.status,
            err.message,
        )
        raise  # Re-raise the exception to be handled by the caller.
    except aiohttp.ClientConnectionError as err:
        # Log errors related to establishing a connection.
        _LOGGER.error("Could not connect to Meraki API at %s: %s", url, err)
        raise  # Re-raise the exception.
    except Exception as err:
        # Log any other unexpected errors.
        _LOGGER.exception(
            "Unexpected error during Meraki API request to %s: %s", url, err
        )
        raise  # Re-raise the exception.
