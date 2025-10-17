"""Tests for the Meraki authentication."""

from unittest.mock import patch, AsyncMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from custom_components.meraki_ha.authentication import (
    validate_meraki_credentials,
)
from custom_components.meraki_ha.core.errors import MerakiAuthenticationError


@pytest.mark.asyncio
async def test_validate_meraki_credentials(hass: HomeAssistant) -> None:
    """Test validate_meraki_credentials."""
    with patch(
        "custom_components.meraki_ha.authentication.MerakiAPIClient"
    ) as mock_client:
        mock_client.return_value.organization.get_organizations = AsyncMock(
            return_value=[{"id": "test-org-id", "name": "Test Org"}]
        )
        result = await validate_meraki_credentials(hass, "test-api-key", "test-org-id")
        assert result == {"org_name": "Test Org", "valid": True}


@pytest.mark.asyncio
async def test_validate_meraki_credentials_invalid_org(hass: HomeAssistant) -> None:
    """Test validate_meraki_credentials with invalid org."""
    with patch(
        "custom_components.meraki_ha.authentication.MerakiAPIClient"
    ) as mock_client:
        mock_client.return_value.organization.get_organizations = AsyncMock(
            return_value=[{"id": "other-org-id", "name": "Other Org"}]
        )
        with pytest.raises(ValueError):
            await validate_meraki_credentials(hass, "test-api-key", "test-org-id")


@pytest.mark.asyncio
async def test_validate_meraki_credentials_auth_failed(hass: HomeAssistant) -> None:
    """Test validate_meraki_credentials with auth failed."""
    with patch(
        "custom_components.meraki_ha.authentication.MerakiAPIClient"
    ) as mock_client:
        mock_client.return_value.organization.get_organizations = AsyncMock(
            side_effect=MerakiAuthenticationError("test")
        )
        with pytest.raises(ConfigEntryAuthFailed):
            await validate_meraki_credentials(hass, "test-api-key", "test-org-id")
