"""Handles Meraki API authentication for the Meraki Home Assistant integration.

This module provides mechanisms to validate API keys and organization IDs
against the Meraki Dashboard API.
"""
import logging
from typing import Any, Dict, List

import aiohttp
from homeassistant.exceptions import ConfigEntryAuthFailed

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha authentication.py loaded")


class MerakiAuthentication:
    """Class to handle Meraki API authentication.

    This class encapsulates the logic for validating API credentials by
    making a request to the Meraki API.
    """

    def __init__(self, api_key: str, org_id: str) -> None:
        """Initialize the Meraki Authentication class.

        Args:
            api_key: The Meraki API key.
            org_id: The Meraki Organization ID.
        """
        self.api_key: str = api_key
        self.org_id: str = org_id

    async def validate_credentials(self) -> bool:
        """Validate Meraki API credentials.

        Makes a request to the Meraki API to fetch organizations and checks
        if the provided organization ID is present in the response.

        Returns:
            True if credentials are valid and the organization ID is found.

        Raises:
            ConfigEntryAuthFailed: If authentication fails (e.g., invalid API key).
            ValueError: If the organization ID is not found in the user's organizations.
            aiohttp.ClientError: If there's an issue with the HTTP request.
            Exception: For other unexpected API errors.
        """
        _LOGGER.debug("Validating Meraki credentials")
        url: str = "https://api.meraki.com/api/v1/organizations"
        headers: Dict[str, str] = {
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Content-Type": "application/json",
        }
        try:
            _LOGGER.debug("Starting aiohttp session for credential validation")
            # Create a new aiohttp client session for this validation attempt.
            # Using 'async with' ensures the session is properly closed.
            async with aiohttp.ClientSession() as session:
                _LOGGER.debug(f"Sending GET request to {url}")
                # Make the GET request to the Meraki organizations endpoint.
                async with session.get(url, headers=headers) as response:
                    _LOGGER.debug(f"Meraki API response status: {response.status}")
                    # Check if the request was successful (HTTP 200 OK).
                    if response.status == 200:
                        # Parse the JSON response containing a list of organizations.
                        organizations: List[Dict[str, Any]] = await response.json()
                        _LOGGER.debug(f"Organizations retrieved: {organizations}")
                        # Verify that the provided organization ID is present in the list of organizations
                        # accessible with the given API key.
                        if not any(org["id"] == self.org_id for org in organizations):
                            _LOGGER.error(f"Invalid Organization ID: {self.org_id}")
                            # Raise ValueError if the org_id is not found, indicating invalid configuration.
                            raise ValueError(f"Invalid Organization ID: {self.org_id}")
                        _LOGGER.debug("Credentials validated successfully")
                        return True
                    # Handle authentication failure (HTTP 401 Unauthorized).
                    # This typically means the API key is incorrect or lacks permissions.
                    elif response.status == 401:
                        _LOGGER.debug("Authentication failed (401)")
                        raise ConfigEntryAuthFailed("Invalid API Key")
                    # Handle other non-successful HTTP status codes.
                    else:
                        error_text = await response.text() # Get error details from response body.
                        _LOGGER.error(
                            f"Meraki API Error: Status: {response.status}, Response: {error_text}"
                        )
                        # Raise a generic exception for other API errors.
                        raise Exception(
                            f"Meraki API Error: Status: {response.status}, Response: {error_text}"
                        )
        # Handle client-side errors during the HTTP request (e.g., network issues).
        except aiohttp.ClientError as e:
            _LOGGER.error(f"Aiohttp Client Error during credential validation: {e}")
            raise  # Re-raise the original aiohttp.ClientError to be handled by the caller.
        # Handle the ValueError raised for an invalid org_id.
        except ValueError as ve:
            _LOGGER.error(f"Value Error during credential validation: {ve}")
            raise  # Re-raise the original ValueError.
        # Handle the ConfigEntryAuthFailed raised for authentication issues.
        except ConfigEntryAuthFailed:
            raise  # Re-raise the original ConfigEntryAuthFailed.
        # Handle any other unexpected exceptions during the process.
        except Exception as e:
            _LOGGER.error(f"Unexpected error connecting to Meraki API: {e}")
            # It's generally better to raise a more specific exception or the original one
            # if it provides more context. For now, re-raising a generic Exception.
            raise Exception(f"Unexpected error connecting to Meraki API: {e}")


async def validate_meraki_credentials(api_key: str, org_id: str) -> bool:
    """Validate Meraki API credentials using the MerakiAuthentication class.

    Args:
        api_key: The Meraki API key.
        org_id: The Meraki Organization ID.

    Returns:
        True if credentials are valid.

    Raises:
        ConfigEntryAuthFailed: If authentication fails.
        ValueError: If the organization ID is invalid.
        aiohttp.ClientError: If there's an issue with the HTTP request.
        Exception: For other API errors.
    """
    auth = MerakiAuthentication(api_key, org_id)
    return await auth.validate_credentials()
