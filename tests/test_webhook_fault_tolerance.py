"""Tests for Meraki webhook registration fault tolerance."""

from unittest.mock import AsyncMock, patch

import pytest

from custom_components.meraki_ha.webhook import async_register_webhook
from homeassistant.core import HomeAssistant


@pytest.fixture
def mock_api_client():
    """Mock the Meraki API client."""
    client = AsyncMock()
    client.register_webhook = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_async_register_webhook_fault_tolerance(
    hass: HomeAssistant, mock_api_client
):
    """Test that async_register_webhook does not raise exceptions."""
    mock_api_client.register_webhook.side_effect = Exception("API Error")

    with patch("homeassistant.components.webhook.async_register") as mock_ha_register:
        # This should not raise despite the side_effect
        await async_register_webhook(
            hass, "test_webhook_id", "test_secret", mock_api_client
        )

    assert mock_ha_register.called
    # It should have caught the exception and logged it
    # (we can't easily check logs here without more setup)
