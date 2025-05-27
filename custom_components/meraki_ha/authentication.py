"""Handles Meraki API authentication for the Meraki Home Assistant integration.

This module provides mechanisms to validate API keys and organization IDs
against the Meraki Dashboard API using the Meraki SDK.
"""
import logging
from typing import Any, Dict, List # Keep List, Dict, Any if still used for type hints

from homeassistant.exceptions import ConfigEntryAuthFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

from ..meraki_api import MerakiAPIClient # Import the refactored client

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki_ha authentication.py loaded (SDK version)")


class MerakiAuthentication:
    """Class to handle Meraki API authentication using the Meraki SDK.

    This class encapsulates the logic for validating API credentials by
    making a request to the Meraki API via the SDK.
    """

    def __init__(self, api_key: str, org_id: str) -> None:
        """Initialize the Meraki Authentication class.

        Args:
            api_key: The Meraki API key.
            org_id: The Meraki Organization ID.
        """
        self.api_key: str = api_key
        self.org_id: str = org_id
        # No MerakiAPIClient instance created here, will be done in validate_credentials

    async def validate_credentials(self) -> bool:
        """Validate Meraki API credentials using the Meraki SDK.

        Makes a request to the Meraki API to fetch organizations and checks
        if the provided organization ID is present in the response.

        Returns:
            True if credentials are valid and the organization ID is found.

        Raises:
            ConfigEntryAuthFailed: If authentication fails (e.g., invalid API key - HTTP 401).
            ValueError: If the organization ID is not found in the user's organizations.
            MerakiSDKAPIError: For other Meraki API errors not handled as ConfigEntryAuthFailed.
            Exception: For other unexpected errors during validation.
        """
        _LOGGER.debug("Validating Meraki credentials using SDK")
        client: MerakiAPIClient = MerakiAPIClient(api_key=self.api_key, org_id=self.org_id)

        try:
            _LOGGER.debug("Fetching organizations using Meraki SDK")
            organizations: List[Dict[str, Any]] = await client.networks.get_organization_networks(
                organization_id=self.org_id
            ) # Using get_organization_networks with org_id to check both API key and org_id validity in one go.
            # If the above call succeeds, the API key is valid and has access to the org.
            # The Meraki SDK's get_organization_networks would typically raise an APIError
            # if the org_id is invalid or the API key doesn't have access to it,
            # often as a 404 or 403, or if the API key is invalid (401).

            # However, the original logic was to fetch all orgs and check if self.org_id is in them.
            # Let's stick to that pattern for functional equivalence.
            all_organizations: List[Dict[str, Any]] = await client.organizations.get_organizations()

            _LOGGER.debug("Organizations retrieved via SDK: %s", all_organizations)

            if not any(org['id'] == self.org_id for org in all_organizations):
                _LOGGER.error(
                    "Invalid Organization ID: %s not found in accessible organizations.", self.org_id
                )
                raise ValueError(f"Invalid Organization ID: {self.org_id}")

            _LOGGER.debug("Credentials validated successfully via SDK")
            await client.close()
            return True

        except MerakiSDKAPIError as e:
            await client.close() # Ensure client is closed on API error
            if e.status == 401:
                _LOGGER.error("Authentication failed: Invalid API Key (HTTP 401). Message: %s", e.message)
                raise ConfigEntryAuthFailed("Invalid API Key (HTTP 401)") from e
            elif e.status == 403:
                _LOGGER.error("Authentication failed: API key lacks permissions (HTTP 403). Message: %s", e.message)
                raise ConfigEntryAuthFailed(f"API key lacks permissions (HTTP 403): {e.message}") from e
            elif e.status == 404: # This occurs if the get_organizations endpoint itself returns 404
                _LOGGER.error("Failed to query organizations (HTTP 404). Message: %s", e.message)
                raise ConfigEntryAuthFailed(f"Failed to query organizations (HTTP 404): {e.message}") from e
            else: # For other MerakiSDKAPIError status codes (e.g., 400, 500, 502, etc.)
                _LOGGER.error("Meraki API error during validation (HTTP %s). Message: %s", e.status, e.message)
                raise ConfigEntryAuthFailed(f"Meraki API error (HTTP {e.status}): {e.message}") from e
        except ValueError: # Catch ValueError for invalid org_id (org_id not in the list of fetched orgs)
            await client.close() # Ensure client is closed
            _LOGGER.error("Invalid Organization ID: %s not found in accessible organizations.", self.org_id)
            raise # Re-raise the ValueError
        except Exception as e:
            # Ensure client is closed on any other unexpected error
            # Check if 'client' was defined and has 'close' method
            if 'client' in locals() and hasattr(client, 'close'):
                 await client.close()
            _LOGGER.error("Unexpected error connecting to Meraki API via SDK: %s", e)
            raise Exception(f"Unexpected error connecting to Meraki API: {e}") from e


async def validate_meraki_credentials(
    api_key: str, org_id: str
) -> bool:
    """Validate Meraki API credentials via MerakiAuthentication class (SDK version).

    Args:
        api_key: The Meraki API key.
        org_id: The Meraki Organization ID.

    Returns:
        True if credentials are valid.

    Raises:
        ConfigEntryAuthFailed: If authentication fails.
        ValueError: If the organization ID is invalid.
        MerakiSDKAPIError: For Meraki API errors from the SDK.
        Exception: For other unexpected errors.
    """
    auth = MerakiAuthentication(api_key, org_id)
    return await auth.validate_credentials()
