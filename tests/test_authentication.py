"""Tests for the Meraki authentication."""

from unittest.mock import patch, AsyncMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from custom_components.meraki_ha.authentication import (
    validate_meraki_credentials,
)
from custom_components.meraki_ha.meraki_api.exceptions import MerakiApiError


@pytest.mark.asyncio
async def test_validate_meraki_credentials(hass: HomeAssistant) -> None:
    """Test validate_meraki_credentials."""
    with patch(
        "custom_components.meraki_ha.authentication.MerakiAPIClient"
    ) as mock_client:
        mock_client.return_value.organizations.getOrganizations = AsyncMock(
            return_value=[{"id": "test-org-id", "name": "Test Org"}]
        )
        mock_client.return_value.close = AsyncMock()
        result = await validate_meraki_credentials("test-api-key", "test-org-id")
        assert result == {"org_name": "Test Org", "valid": True}


@pytest.mark.asyncio
async def test_validate_meraki_credentials_invalid_org(hass: HomeAssistant) -> None:
    """Test validate_meraki_credentials with invalid org."""
    with patch(
        "custom_components.meraki_ha.authentication.MerakiAPIClient"
    ) as mock_client:
        mock_client.return_value.organizations.getOrganizations = AsyncMock(
            return_value=[{"id": "other-org-id", "name": "Other Org"}]
        )
        mock_client.return_value.close = AsyncMock()
        with pytest.raises(ValueError):
            await validate_meraki_credentials("test-api-key", "test-org-id")


@pytest.mark.asyncio
async def test_validate_meraki_credentials_auth_failed(hass: HomeAssistant) -> None:
    """Test validate_meraki_credentials with auth failed."""
    with patch(
        "custom_components.meraki_ha.authentication.MerakiAPIClient"
    ) as mock_client:
        mock_client.return_value.organizations.getOrganizations = AsyncMock(
            side_effect=MerakiApiError("test")
        )
        mock_client.return_value.close = AsyncMock()
        with pytest.raises(ConfigEntryAuthFailed):
            await validate_meraki_credentials("test-api-key", "test-org-id")
