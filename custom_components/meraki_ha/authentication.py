"""Handles authentication with the Meraki Dashboard API.

This module provides the `MerakiAuthentication` class and a helper function
`validate_meraki_credentials` to verify that the provided API key and
organization ID are valid and can be used to access the Meraki API.
"""

import logging
from typing import Any, Dict, List

import aiohttp
from homeassistant.exceptions import ConfigEntryAuthFailed

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha authentication.py loaded")  # Added Log


class MerakiAuthentication:
    """Handles authentication against the Meraki API.

    This class provides a method to validate a Meraki API key and
    organization ID by attempting to list organizations accessible
    with the given key and checking if the specified organization ID
    is present in the response.

    Attributes:
        api_key (str): The Meraki API key.
        org_id (str): The Meraki organization ID to validate.
    """

    def __init__(self, api_key: str, org_id: str) -> None:
        """Initializes the MerakiAuthentication class.

        Args:
            api_key (str): The API key for accessing the Meraki Dashboard API.
            org_id (str): The ID of the Meraki organization to verify against
                the API key's accessible organizations.
        """
        self.api_key = api_key
        self.org_id = org_id
        _LOGGER.debug("MerakiAuthentication initialized for Org ID: %s", org_id)

    async def validate_credentials(self) -> bool:
        """Validates the stored API key and organization ID.

        Makes a request to the Meraki API to list organizations. If successful,
        it checks if the `self.org_id` is among the organizations returned.

        Returns:
            bool: True if the API key is valid and the organization ID is
                  accessible with that key.

        Raises:
            ConfigEntryAuthFailed: If the API key is invalid (results in a 401
                Unauthorized response).
            ValueError: If the provided `self.org_id` is not found in the list
                of organizations accessible by the API key.
            aiohttp.ClientError: For network or other client-side HTTP issues
                encountered by `aiohttp`.
            Exception: For any other unexpected errors during the validation process,
                       often re-raised from underlying HTTP or JSON parsing issues.
        """
        _LOGGER.info("Attempting to validate Meraki credentials for Org ID: %s", self.org_id)
        # The standard base URL for Meraki API v1.
        organizations_url = "https://api.meraki.com/api/v1/organizations"
        headers = {
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

        try:
            # Using a new session for each validation attempt.
            # For frequent calls, a shared session might be considered, but
            # validation is typically infrequent (e.g., during config flow).
            async with aiohttp.ClientSession() as session:
                _LOGGER.debug("Sending GET request to %s for credential validation.", organizations_url)
                async with session.get(organizations_url, headers=headers, timeout=10) as response: # Added timeout
                    _LOGGER.debug(
                        "Credential validation API response status: %s", response.status
                    )
                    response_text = await response.text() # Get text for logging on error
                    _LOGGER.debug("Credential validation API response text: %s", response_text)


                    if response.status == 200:
                        try:
                            organizations_data: List[Dict[str, Any]] = await response.json()
                        except aiohttp.ContentTypeError:
                            _LOGGER.error("Failed to parse JSON response from Meraki API. Response: %s", response_text)
                            raise Exception("Meraki API returned non-JSON response for organizations.")


                        _LOGGER.debug(
                            "Successfully retrieved %d organizations for API key.",
                            len(organizations_data),
                        )
                        # Check if the provided organization ID is in the list of accessible organizations.
                        if not any(
                            org.get("id") == self.org_id for org in organizations_data
                        ):
                            _LOGGER.error(
                                "Invalid Organization ID: '%s'. Not found in accessible organizations: %s",
                                self.org_id,
                                [org.get("id") for org in organizations_data],
                            )
                            raise ValueError(f"Invalid Organization ID: {self.org_id}")
                        _LOGGER.info(
                            "Meraki credentials validated successfully for Org ID: %s",
                            self.org_id,
                        )
                        return True
                    elif response.status == 401:
                        _LOGGER.warning(
                            "Authentication failed (401) for Meraki API key. "
                            "Please check the API key."
                        )
                        raise ConfigEntryAuthFailed("Invalid Meraki API key.")
                    else:
                        _LOGGER.error(
                            "Meraki API returned an error during credential validation. "
                            "Status: %s, Response: %s",
                            response.status,
                            response_text,
                        )
                        # Generic exception for other HTTP errors (e.g., 400, 404, 5xx).
                        raise Exception(
                            f"Meraki API Error: Status {response.status}, Response: {response_text}"
                        )
        except aiohttp.ClientError as client_error:
            # Handles connection errors, timeouts, etc.
            _LOGGER.error(
                "Aiohttp client error during Meraki credential validation: %s",
                client_error,
            )
            # Re-raise as a more generic exception or a custom one if defined.
            raise Exception(
                "Network or client error validating credentials with Meraki API."
            ) from client_error
        # ValueError and ConfigEntryAuthFailed are explicitly raised and caught by callers.
        # No need to catch them here just to re-raise.
        except Exception as e:
            # Catch any other unexpected errors.
            _LOGGER.exception(
                "Unexpected error during Meraki credential validation: %s", e
            )
            # Re-raise to ensure the error is not silently ignored.
            raise


async def validate_meraki_credentials(api_key: str, org_id: str) -> bool:
    """Validates Meraki API credentials by instantiating and using `MerakiAuthentication`.

    This is a convenience helper function that encapsulates the creation of a
    `MerakiAuthentication` object and the call to its `validate_credentials` method.

    Args:
        api_key (str): The Meraki API key.
        org_id (str): The Meraki organization ID.

    Returns:
        bool: True if credentials are valid, otherwise an exception is raised.

    Raises:
        ConfigEntryAuthFailed: If authentication fails due to an invalid API key.
        ValueError: If the organization ID is invalid or not accessible.
        Exception: For other API or network-related errors.
    """
    _LOGGER.debug(
        "Using helper function to validate Meraki credentials for Org ID: %s", org_id
    )
    auth_handler = MerakiAuthentication(api_key, org_id)
    return await auth_handler.validate_credentials()
