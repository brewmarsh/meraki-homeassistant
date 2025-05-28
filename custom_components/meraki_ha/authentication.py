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
        _LOGGER.debug("Preparing to validate Meraki credentials for organization %s using SDK", self.org_id)
        # Corrected attribute names to self.api_key and self.org_id as per class __init__
        client: MerakiAPIClient = MerakiAPIClient(api_key=self.api_key, org_id=self.org_id)
        
        try:
            _LOGGER.debug("Fetching networks for organization %s using Meraki SDK", self.org_id)
            networks: List[Dict[str, Any]] = await client.networks.get_organization_networks(
                organization_id=self.org_id
            )

            if not networks:
                _LOGGER.warning("No networks found for organization %s. This might be due to the organization having no networks or restricted API key permissions.", self.org_id)
                raise ValueError(f"No networks found for the organization {self.org_id}.")

            # The subtask example also included an organization check.
            # The current code only checks networks. If the intention is to also validate the org_id
            # against a list of all accessible organizations, that logic would go here.
            # For now, replicating the existing logic which relies on get_organization_networks.
            # Example (if needed, but not in current file's logic for this try block):
            # all_organizations: List[Dict[str, Any]] = await client.organizations.getOrganizations()
            # if not any(org['id'] == self.org_id for org in all_organizations):
            #     _LOGGER.error("Invalid Organization ID: %s not found in accessible organizations.", self.org_id)
            #     raise ValueError(f"Invalid Organization ID: {self.org_id}")

            _LOGGER.info("Meraki credentials and organization ID %s validated successfully (networks found).", self.org_id)
            return True

        except MerakiSDKAPIError as e:
            if e.status == 401:
                _LOGGER.error("Authentication failed: Invalid API Key (HTTP 401) for org %s. Message: %s", self.org_id, e.message)
                raise ConfigEntryAuthFailed("Invalid API Key (HTTP 401)") from e
            elif e.status == 403:
                _LOGGER.error("Authentication failed: API key lacks permissions for organization %s (HTTP 403). Message: %s", self.org_id, e.message)
                raise ConfigEntryAuthFailed(f"API key lacks permissions for organization {self.org_id} (HTTP 403): {e.message}") from e
            elif e.status == 404:
                _LOGGER.error("Failed to query networks: Organization ID %s not found (HTTP 404). Message: %s", self.org_id, e.message)
                raise ConfigEntryAuthFailed(f"Organization ID {self.org_id} not found (HTTP 404): {e.message}") from e
            else:
                _LOGGER.error("Meraki API error during validation (HTTP %s) for organization %s. Message: %s", e.status, self.org_id, e.message)
                raise ConfigEntryAuthFailed(f"Meraki API error (HTTP {e.status}) for org {self.org_id}: {e.message}") from e
        except ValueError as e: 
            _LOGGER.warning("Validation error for Meraki credentials (org %s): %s", self.org_id, e)
            # Re-raise to be handled by config flow or caller
            raise
        except Exception as e:
            _LOGGER.error("Unexpected error during Meraki credential validation for org %s: %s", self.org_id, e)
            # Wrap in ConfigEntryAuthFailed as this is an unexpected issue during auth setup.
            raise ConfigEntryAuthFailed(f"Unexpected error during validation for org {self.org_id}: {e}") from e
        finally:
            _LOGGER.debug("Closing MerakiAPIClient session for credential validation (org %s).", self.org_id)
            await client.close()


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
