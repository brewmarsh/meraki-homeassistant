"""Tests for the Meraki authentication."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from meraki.exceptions import APIError

from custom_components.meraki_ha.authentication import (
    validate_meraki_credentials,
)
from custom_components.meraki_ha.core.errors import (
    InvalidOrgID,
    MerakiConnectionError,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed


@pytest.mark.asyncio
async def test_validate_meraki_credentials(hass: HomeAssistant) -> None:
    """
    Test validate_meraki_credentials.

    Args:
    ----
        hass: The Home Assistant instance.

    """
    with patch(
        "custom_components.meraki_ha.core.api.create_api_client",
    ) as mock_create_client:
        mock_client = AsyncMock()
        mock_create_client.return_value = mock_client
        mock_client.async_setup = AsyncMock()
        mock_client.organization.get_organization = AsyncMock(
            return_value={"id": "test-org-id", "name": "Test Org"},
        )
        result = await validate_meraki_credentials(hass, "test-api-key", "test-org-id")
        assert result == {"org_name": "Test Org", "valid": True}


@pytest.mark.asyncio
async def test_validate_meraki_credentials_invalid_org(hass: HomeAssistant) -> None:
    """
    Test validate_meraki_credentials with invalid org.

    Args:
    ----
        hass: The Home Assistant instance.

    """
    with (
        patch(
            "custom_components.meraki_ha.core.api.create_api_client",
        ) as mock_create_client,
        pytest.raises(InvalidOrgID),
    ):
        mock_client = AsyncMock()
        mock_create_client.return_value = mock_client
        mock_client.async_setup = AsyncMock()
        mock_client.organization.get_organization = AsyncMock(
            return_value={},
        )
        await validate_meraki_credentials(hass, "test-api-key", "test-org-id")


@pytest.mark.asyncio
async def test_validate_meraki_credentials_auth_failed(hass: HomeAssistant) -> None:
    """
    Test validate_meraki_credentials with auth failed.

    Args:
    ----
        hass: The Home Assistant instance.

    """
    metadata = {"tags": ["test"], "operation": "getOrganization"}
    response = MagicMock()
    response.status_code = 401
    response.json.return_value = {"errors": ["Invalid API key"]}
    error = APIError(metadata, response)

    with (
        patch(
            "custom_components.meraki_ha.core.api.create_api_client",
        ) as mock_create_client,
        pytest.raises(ConfigEntryAuthFailed),
    ):
        mock_client = AsyncMock()
        mock_create_client.return_value = mock_client
        mock_client.async_setup = AsyncMock()
        # Direct call to the organization endpoint which would be called by authentication
        mock_client.organization.get_organization = AsyncMock(
            side_effect=error,
        )
        await validate_meraki_credentials(hass, "test-api-key", "test-org-id")


@pytest.mark.asyncio
async def test_validate_meraki_credentials_no_dashboard(hass: HomeAssistant) -> None:
    """
    Test validate_meraki_credentials with no dashboard.

    Args:
    ----
        hass: The Home Assistant instance.

    """
    with (
        patch(
            "custom_components.meraki_ha.core.api.create_api_client",
        ) as mock_create_client,
        pytest.raises(MerakiConnectionError),
    ):
        mock_client = AsyncMock()
        mock_create_client.return_value = mock_client
        mock_client.async_setup = AsyncMock()
        mock_client.dashboard = None
        await validate_meraki_credentials(hass, "test-api-key", "test-org-id")
