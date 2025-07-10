"""Handles Meraki API authentication for the Meraki Home Assistant integration.

This module provides mechanisms to validate API keys and organization IDs
against the Meraki Dashboard API using the Meraki SDK.
"""

import logging

# Keep List, Dict, Any if still used for type hints
from typing import Any, Dict, List, Optional

from homeassistant.exceptions import ConfigEntryAuthFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

# Import the refactored client
from custom_components.meraki-ha.meraki-api import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("meraki-ha authentication.py loaded (SDK version)")


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
        # No MerakiAPIClient instance created here, will be done in
        # validate_credentials

    async def validate_credentials(self) -> Dict[str, Any]:
        """Validate Meraki API credentials using the Meraki SDK.

        Makes a request to the Meraki API to fetch organizations and checks
        if the provided organization ID is present in the response.

        Returns:
            A dictionary with "valid": True and "org_name": "Organization Name" if credentials are valid.

        Raises:
            ConfigEntryAuthFailed: If authentication fails (e.g., invalid API key - HTTP 401).
            ValueError: If the organization ID is not found in the user's organizations.
            MerakiSDKAPIError: For other Meraki API errors not handled as ConfigEntryAuthFailed.
            Exception: For other unexpected errors during validation.
        """
        _LOGGER.debug(
            "Preparing to validate Meraki credentials for organization %s using SDK",
            self.org_id,
        )
        # Corrected attribute names to self.api_key and self.org_id as per
        # class __init__
        client: MerakiAPIClient = MerakiAPIClient(
            api_key=self.api_key, org_id=self.org_id
        )

        try:
            _LOGGER.debug(
                "Fetching networks for organization %s using Meraki SDK", self.org_id
            )  # This log line might become inaccurate
            # networks: List[Dict[str, Any]] = await client.networks.get_organization_networks(
            #     organization_id=self.org_id
            # )

            # if not networks:
            #     _LOGGER.warning("No networks found for organization %s. This might be due to the organization having no networks or restricted API key permissions.", self.org_id)
            #     raise ValueError(f"No networks found for the organization {self.org_id}.")

            _LOGGER.debug(
                "Fetching all organizations accessible by the API key to validate Organization ID %s",
                self.org_id,
            )
            # Assuming client.organizations.getOrganizations exists and returns
            # a list of dicts, each with an 'id' key.
            all_organizations: List[Dict[str, Any]] = (
                await client.organizations.getOrganizations()
            )

            # Initialize fetched_org_name
            fetched_org_name: Optional[str] = None
            org_found = False
            if all_organizations:  # Ensure all_organizations is not None or empty
                for org in all_organizations:
                    if org.get("id") == self.org_id:
                        org_found = True
                        # Store the organization name
                        fetched_org_name = org.get("name")
                        break

            if not org_found:
                _LOGGER.warning(
                    "Organization ID %s not found among accessible organizations or API key lacks permissions to list organizations.",
                    self.org_id,
                )
                # This specific error message helps differentiate from other
                # ValueErrors.
                raise ValueError(
                    f"Specified Organization ID {self.org_id} is not accessible with the provided API key."
                )

            # If org_found is True, the validation specific to org_id's accessibility is successful.
            # The original log message for success was:
            # _LOGGER.info("Meraki credentials and organization ID %s validated successfully (networks found).", self.org_id)
            # Change it to reflect the new validation method:
            _LOGGER.info(
                "Meraki API key validated and Organization ID %s found in accessible organizations. Name: %s",
                self.org_id,
                fetched_org_name,
            )
            return {"valid": True, "org_name": fetched_org_name}

        except MerakiSDKAPIError as e:
            if e.status == 401:
                _LOGGER.error(
                    "Authentication failed: Invalid API Key (HTTP 401) for org %s. Message: %s",
                    self.org_id,
                    e.message,
                )
                raise ConfigEntryAuthFailed("Invalid API Key (HTTP 401)") from e
            elif e.status == 403:
                _LOGGER.error(
                    "Authentication failed: API key lacks permissions for organization %s (HTTP 403). Message: %s",
                    self.org_id,
                    e.message,
                )
                raise ConfigEntryAuthFailed(
                    f"API key lacks permissions for organization {self.org_id} (HTTP 403): {e.message}"
                ) from e
            elif e.status == 404:
                _LOGGER.error(
                    "Failed to query networks: Organization ID %s not found (HTTP 404). Message: %s",
                    self.org_id,
                    e.message,
                )
                raise ConfigEntryAuthFailed(
                    f"Organization ID {self.org_id} not found (HTTP 404): {e.message}"
                ) from e
            else:
                _LOGGER.error(
                    "Meraki API error during validation (HTTP %s) for organization %s. Message: %s",
                    e.status,
                    self.org_id,
                    e.message,
                )
                raise ConfigEntryAuthFailed(
                    f"Meraki API error (HTTP {e.status}) for org {self.org_id}: {e.message}"
                ) from e
        except ValueError as e:
            _LOGGER.warning(
                "Validation error for Meraki credentials (org %s): %s", self.org_id, e
            )
            # Re-raise to be handled by config flow or caller
            raise
        except Exception as e:
            _LOGGER.error(
                "Unexpected error during Meraki credential validation for org %s: %s",
                self.org_id,
                e,
            )
            # Wrap in ConfigEntryAuthFailed as this is an unexpected issue
            # during auth setup.
            raise ConfigEntryAuthFailed(
                f"Unexpected error during validation for org {self.org_id}: {e}"
            ) from e
        finally:
            _LOGGER.debug(
                "Closing MerakiAPIClient session for credential validation (org %s).",
                self.org_id,
            )
            await client.close()


async def validate_meraki_credentials(api_key: str, org_id: str) -> Dict[str, Any]:
    """Validate Meraki API credentials via MerakiAuthentication class (SDK version).

    Args:
        api_key: The Meraki API key.
        org_id: The Meraki Organization ID.

    Returns:
        A dictionary with "valid": True and "org_name": "Organization Name" if credentials are valid.

    Raises:
        ConfigEntryAuthFailed: If authentication fails.
        ValueError: If the organization ID is invalid.
        MerakiSDKAPIError: For Meraki API errors from the SDK.
        Exception: For other unexpected errors.
    """
    auth = MerakiAuthentication(api_key, org_id)
    return await auth.validate_credentials()
