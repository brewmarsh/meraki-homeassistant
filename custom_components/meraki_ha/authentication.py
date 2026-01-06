"""
Handles Meraki API authentication for the Meraki Home Assistant integration.

This module provides mechanisms to validate API keys and organization IDs
against the Meraki Dashboard API using the Meraki SDK.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from meraki.exceptions import APIError as MerakiSDKAPIError

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

from .core.api.client import MerakiAPIClient
from .core.errors import MerakiAuthenticationError, MerakiConnectionError

_LOGGER = logging.getLogger(__name__)


class MerakiAuthentication:
    """
    Class to handle Meraki API authentication using the Meraki SDK.

    This class encapsulates the logic for validating API credentials by
    making a request to the Meraki API via the SDK.
    """

    def __init__(self, hass: HomeAssistant, api_key: str, organization_id: str) -> None:
        """
        Initialize the Meraki Authentication class.

        Args:
        ----
            hass: The Home Assistant instance.
            api_key: The Meraki API key.
            organization_id: The Meraki Organization ID.

        """
        self.hass = hass
        self.api_key: str = api_key
        self.organization_id: str = organization_id

    async def validate_credentials(self) -> dict[str, Any]:
        """
        Validate Meraki API credentials using the Meraki SDK.

        Makes a request to the Meraki API to fetch organizations and checks
        if the provided organization ID is present in the response.

        Returns
        -------
            A dictionary with "valid": True and "org_name": "Org Name".

        Raises
        ------
            ConfigEntryAuthFailed: If authentication fails.
            ValueError: If the organization ID is not found.
            MerakiConnectionError: If there is a connection error.

        """
        client = MerakiAPIClient(
            hass=self.hass,
            api_key=self.api_key,
            org_id=self.organization_id,
        )
        await client.async_setup()

        try:
            all_organizations: list[
                dict[str, Any]
            ] = await client.organization.get_organizations()

            org_found = False
            fetched_org_name: str | None = None

            if all_organizations:
                for org in all_organizations:
                    if org.get("id") == self.organization_id:
                        org_found = True
                        fetched_org_name = org.get("name")
                        break

            if not org_found:
                _LOGGER.warning(
                    "Organization ID %s not found in accessible organizations.",
                    self.organization_id,
                )
                raise ValueError(
                    f"Org ID {self.organization_id} not accessible with this API key.",
                )

            _LOGGER.info(
                "API key validated for Organization ID %s (Name: %s)",
                self.organization_id,
                fetched_org_name,
            )
            return {"valid": True, "org_name": fetched_org_name}

        except MerakiAuthenticationError as e:
<<<<<<< HEAD
<<<<<<< HEAD
            _LOGGER.error("Authentication failed: %s", e.message)
            raise ConfigEntryAuthFailed(f"Authentication failed: {e.message}") from e
        except MerakiConnectionError as e:
            _LOGGER.error("Connection error: %s", e.message)
            raise MerakiConnectionError(f"Connection error: {e.message}") from e
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
            _LOGGER.error("Authentication failed: %s", e)
            raise ConfigEntryAuthFailed(f"Authentication failed: {e}") from e
        except MerakiConnectionError as e:
            _LOGGER.error("Connection error: %s", e)
            raise MerakiConnectionError(f"Connection error: {e}") from e
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
        except MerakiSDKAPIError as e:
            if e.status == 401:
                _LOGGER.error(
                    "Auth failed (HTTP 401) for org %s.",
                    self.organization_id,
                )
                raise ConfigEntryAuthFailed("Invalid API Key (HTTP 401)") from e
            if e.status == 403:
                _LOGGER.error(
                    "Auth failed (HTTP 403) for org %s.",
                    self.organization_id,
                )
                raise ConfigEntryAuthFailed(
                    f"API key lacks permissions for org {self.organization_id}.",
                ) from e
            if e.status == 404:
                _LOGGER.error(
                    "Query failed (HTTP 404) for org %s.",
                    self.organization_id,
                )
                raise ConfigEntryAuthFailed(
                    f"Organization ID {self.organization_id} not found.",
                ) from e

            _LOGGER.error(
                "Meraki API error for org %s (HTTP %s).",
                self.organization_id,
                e.status,
            )
            raise ConfigEntryAuthFailed(
                f"Meraki API error for org {self.organization_id}: {e.message}",
            ) from e
        except ValueError as e:
            _LOGGER.warning(
                "Validation error for Meraki credentials (org %s): %s",
                self.organization_id,
                e,
            )
            raise
        except Exception as e:
            _LOGGER.error(
                "Unexpected error during validation for org %s: %s",
                self.organization_id,
                e,
            )
            raise ConfigEntryAuthFailed(
                f"Unexpected error for org {self.organization_id}: {e}",
            ) from e


async def validate_meraki_credentials(
    hass: HomeAssistant,
    api_key: str,
    organization_id: str,
) -> dict[str, Any]:
    """
    Validate Meraki API credentials via MerakiAuthentication class (SDK version).

    Args:
    ----
        hass: The Home Assistant instance.
        api_key: The Meraki API key.
        organization_id: The Meraki Organization ID.

    Returns
    -------
        A dictionary with "valid": True and "org_name": "Organization Name".

    Raises
    ------
        ConfigEntryAuthFailed: If authentication fails.
        ValueError: If the organization ID is invalid.
        MerakiConnectionError: For Meraki connection errors.

    """
    auth = MerakiAuthentication(hass, api_key, organization_id)
    return await auth.validate_credentials()
