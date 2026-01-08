"""Extended tests for webhook.py module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.errors import MerakiConnectionError
from custom_components.meraki_ha.webhook import (
    async_handle_webhook,
    async_register_webhook,
    async_unregister_webhook,
    get_webhook_url,
)


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock hass instance."""
    hass = MagicMock()
    hass.bus = MagicMock()
    hass.bus.async_fire = MagicMock()
    hass.data = {}
    return hass


@pytest.fixture
def mock_api_client() -> MagicMock:
    """Create a mock API client."""
    client = MagicMock()
    client.register_webhook = AsyncMock()
    client.unregister_webhook = AsyncMock()
    return client


def test_get_webhook_url_with_external_url() -> None:
    """Test getting webhook URL with external URL override."""
    hass = MagicMock()
    webhook_id = "test_webhook_id"
    external_url = "https://external.example.com"

    url = get_webhook_url(hass, webhook_id, entry_webhook_url=external_url)

    assert url == f"https://external.example.com/api/webhook/{webhook_id}"


def test_get_webhook_url_from_ha_external_url() -> None:
    """Test getting webhook URL from Home Assistant's external URL."""
    hass = MagicMock()
    webhook_id = "test_webhook_id"

    with patch(
        "custom_components.meraki_ha.webhook.get_url",
        return_value="https://ha.example.com",
    ):
        url = get_webhook_url(hass, webhook_id)

    assert url == "https://ha.example.com/api/webhook/test_webhook_id"


def test_get_webhook_url_requires_https() -> None:
    """Test that get_webhook_url requires HTTPS."""
    hass = MagicMock()

    with patch(
        "custom_components.meraki_ha.webhook.get_url",
        return_value="http://insecure.example.com",
    ):
        with pytest.raises(MerakiConnectionError, match="HTTPS"):
            get_webhook_url(hass, "webhook_id")


def test_get_webhook_url_rejects_local_url() -> None:
    """Test that get_webhook_url rejects local URLs."""
    hass = MagicMock()

    with patch(
        "custom_components.meraki_ha.webhook.get_url",
        return_value="https://192.168.1.100",
    ):
        with pytest.raises(MerakiConnectionError, match="public URL"):
            get_webhook_url(hass, "webhook_id")


def test_get_webhook_url_no_url_configured() -> None:
    """Test that get_webhook_url raises when no URL is configured."""
    hass = MagicMock()

    with patch(
        "custom_components.meraki_ha.webhook.get_url",
        return_value=None,
    ):
        with pytest.raises(MerakiConnectionError, match="No webhook URL configured"):
            get_webhook_url(hass, "webhook_id")


@pytest.mark.asyncio
async def test_async_register_webhook(
    mock_hass: MagicMock,
    mock_api_client: MagicMock,
) -> None:
    """Test webhook registration."""
    mock_entry = MagicMock()
    mock_entry.data = {"webhook_url": "https://external.example.com"}

    await async_register_webhook(
        mock_hass,
        "webhook_123",
        "secret_abc",
        mock_api_client,
        entry=mock_entry,
        config_entry_id="entry_123",
    )

    mock_api_client.register_webhook.assert_called_once()


@pytest.mark.asyncio
async def test_async_unregister_webhook(
    mock_hass: MagicMock,
    mock_api_client: MagicMock,
) -> None:
    """Test webhook unregistration."""
    await async_unregister_webhook(mock_hass, "config_entry_123", mock_api_client)

    mock_api_client.unregister_webhook.assert_called_once_with("config_entry_123")


@pytest.mark.asyncio
async def test_async_handle_webhook_invalid_json(
    mock_hass: MagicMock,
) -> None:
    """Test handling webhook with invalid JSON."""
    mock_request = MagicMock()
    mock_request.json = AsyncMock(side_effect=ValueError("Invalid JSON"))

    # Should handle error gracefully without raising
    await async_handle_webhook(mock_hass, "test_webhook", mock_request)
