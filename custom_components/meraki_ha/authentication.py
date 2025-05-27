"""Handles Meraki API authentication for the Meraki Home Assistant integration.

This module provides mechanisms to validate API keys and organization IDs
against the Meraki Dashboard API using the Meraki SDK.
"""
import logging
from typing import Any, Dict, List # Keep List, Dict, Any if still used for type hints

from homeassistant.exceptions import ConfigEntryAuthFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

from custom_components.meraki_ha.meraki_api import MerakiAPIClient # Import the refactored client

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
            _LOGGER.debug("Fetching networks for organization %s using Meraki SDK", self.org_id)
            # Changed method name, parameters, and variable name as per instructions
            networks: List[Dict[str, Any]] = await client.networks.getOrganizationNetworks(
                organization_id=self.org_id, total_pages="all"
            )

            # Check if any networks were returned for the organization.
            # This indirectly validates that the API key has access to the specified org_id
            # and that the org_id itself is valid, as getOrganizationNetworks would likely
            # raise an APIError (e.g., 404 for invalid org_id, 403 for permission issues)
            # if there's an issue before returning an empty list for a valid org with no networks.
            if not networks:
                # This case implies the org_id was valid and accessible, but it contains no networks.
                # Or, it could be that the API key has restricted access that prevents listing networks
                # even if the org_id is correct.
                _LOGGER.warning("No networks found for organization %s. This might be due to the organization having no networks or restricted API key permissions.", self.org_id)
                # The original instruction was to raise ValueError here.
                # Consider if this should be ConfigEntryAuthFailed or a custom error if no networks
                # is a valid state but not for this integration's purpose.
                # For now, sticking to ValueError as requested.
                raise ValueError(f"No networks found for the organization {self.org_id}.")

            # If networks are found, it implies the API key is valid and has access to the organization.
            # The original code also fetched all organizations to explicitly check if self.org_id was in the list.
            # This new approach relies on getOrganizationNetworks succeeding for self.org_id.
            # If that call is successful and returns networks (or even an empty list for an org with no networks),
            # it implies the org_id is valid and accessible by the API key.
            # No need for the separate client.organizations.get_organizations() call if this interpretation is correct.

            _LOGGER.debug("Successfully fetched networks for organization %s. Credentials and Org ID are considered valid.", self.org_id)
            # await client.close() # Removed as per instruction
            return True

        except MerakiSDKAPIError as e:
            # await client.close() # Removed as per instruction
            if e.status == 401:
                _LOGGER.error("Authentication failed: Invalid API Key (HTTP 401). Message: %s", e.message)
                raise ConfigEntryAuthFailed("Invalid API Key (HTTP 401)") from e
            elif e.status == 403: # Forbidden, API key might not have access to this org or networks
                _LOGGER.error("Authentication failed: API key lacks permissions for organization %s (HTTP 403). Message: %s", self.org_id, e.message)
                raise ConfigEntryAuthFailed(f"API key lacks permissions for organization {self.org_id} (HTTP 403): {e.message}") from e
            elif e.status == 404: # Not Found, Organization ID might be incorrect
                _LOGGER.error("Failed to query networks: Organization ID %s not found (HTTP 404). Message: %s", self.org_id, e.message)
                raise ConfigEntryAuthFailed(f"Organization ID {self.org_id} not found (HTTP 404): {e.message}") from e
            else: # For other MerakiSDKAPIError status codes
                _LOGGER.error("Meraki API error during validation (HTTP %s) for organization %s. Message: %s", e.status, self.org_id, e.message)
                raise ConfigEntryAuthFailed(f"Meraki API error (HTTP {e.status}) for org {self.org_id}: {e.message}") from e
        except ValueError as e: # Catch ValueError (e.g., from "No networks found")
            # await client.close() # Removed as per instruction
            _LOGGER.error("Validation error: %s", str(e)) # Log the specific ValueError
            # Re-raise the ValueError to be handled by the caller, potentially as a config flow step error.
            # Or, if appropriate, map to ConfigEntryAuthFailed if it implies an auth/setup issue.
            # For "No networks found", this might indicate a setup issue rather than bad auth.
            raise # Re-raise the ValueError
        except Exception as e:
            # if 'client' in locals() and hasattr(client, 'close'): # Client variable is always defined here
            # await client.close() # Removed as per instruction
            _LOGGER.error("Unexpected error connecting to Meraki API via SDK for organization %s: %s", self.org_id, e)
            # It's generally better to raise a specific HA exception if possible.
            raise ConfigEntryAuthFailed(f"Unexpected error for org {self.org_id}: {e}") from e


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
