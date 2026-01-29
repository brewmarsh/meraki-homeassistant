"""Tests for Meraki webhook registration."""
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.webhook import async_register_webhook


@pytest.fixture
def mock_api_client():
    """Mock the Meraki API client."""
    client = AsyncMock()
    client.register_webhook = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_register_webhook_call(hass: HomeAssistant, mock_api_client):
    """Test that register_webhook is called correctly."""
    entry = MockConfigEntry(
        domain="meraki_ha",
        data={"webhook_url": "https://example.com/api/webhook/test"},
        entry_id="test_entry_id",
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.meraki_ha.webhook.get_webhook_url",
        return_value="https://example.com/api/webhook/test",
    ):
        await async_register_webhook(
            hass, "test_webhook_id", "test_secret", mock_api_client, entry=entry
        )

    # This assertion validates that the fix correctly extracts config_entry_id from
    # entry
    mock_api_client.register_webhook.assert_called_once_with(
        "https://example.com/api/webhook/test", "test_secret", "test_entry_id"
    )
