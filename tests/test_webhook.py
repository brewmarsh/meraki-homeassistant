"""Tests for the Meraki webhook module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import web
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.core.errors import MerakiConnectionError
from custom_components.meraki_ha.webhook import (
    async_handle_webhook,
    async_register_webhook,
    async_unregister_webhook,
    get_webhook_url,
)


class TestGetWebhookUrl:
    """Tests for get_webhook_url function."""

    def test_with_entry_webhook_url(self) -> None:
        """Test get_webhook_url with a configured webhook URL."""
        hass = MagicMock(spec=HomeAssistant)
        result = get_webhook_url(hass, "webhook_123", "https://mysite.example.com")
        assert result == "https://mysite.example.com/api/webhook/webhook_123"

    def test_with_external_url_fallback(self) -> None:
        """Test get_webhook_url falling back to HA external URL."""
        hass = MagicMock(spec=HomeAssistant)
        with patch(
            "custom_components.meraki_ha.webhook.get_url",
            return_value="https://ha.example.com",
        ):
            result = get_webhook_url(hass, "webhook_123")
        assert result == "https://ha.example.com/api/webhook/webhook_123"

    def test_no_url_configured_raises_error(self) -> None:
        """Test get_webhook_url raises error when no URL configured."""
        hass = MagicMock(spec=HomeAssistant)
        with patch(
            "custom_components.meraki_ha.webhook.get_url",
            return_value=None,
        ):
            with pytest.raises(MerakiConnectionError) as exc_info:
                get_webhook_url(hass, "webhook_123")
        assert "No webhook URL configured" in str(exc_info.value)

    def test_http_url_raises_error(self) -> None:
        """Test get_webhook_url raises error for HTTP URL."""
        hass = MagicMock(spec=HomeAssistant)
        with pytest.raises(MerakiConnectionError) as exc_info:
            get_webhook_url(hass, "webhook_123", "http://example.com")
        assert "require HTTPS" in str(exc_info.value)

    def test_local_192_168_url_raises_error(self) -> None:
        """Test get_webhook_url raises error for 192.168.x.x URL."""
        hass = MagicMock(spec=HomeAssistant)
        with pytest.raises(MerakiConnectionError) as exc_info:
            get_webhook_url(hass, "webhook_123", "https://192.168.1.1")
        assert "public URL" in str(exc_info.value)

    def test_local_10_url_raises_error(self) -> None:
        """Test get_webhook_url raises error for 10.x.x.x URL."""
        hass = MagicMock(spec=HomeAssistant)
        with pytest.raises(MerakiConnectionError) as exc_info:
            get_webhook_url(hass, "webhook_123", "https://10.0.0.1")
        assert "public URL" in str(exc_info.value)

    def test_local_172_url_raises_error(self) -> None:
        """Test get_webhook_url raises error for 172.x.x.x URL."""
        hass = MagicMock(spec=HomeAssistant)
        with pytest.raises(MerakiConnectionError) as exc_info:
            get_webhook_url(hass, "webhook_123", "https://172.16.0.1")
        assert "public URL" in str(exc_info.value)

    def test_localhost_url_raises_error(self) -> None:
        """Test get_webhook_url raises error for localhost URL."""
        hass = MagicMock(spec=HomeAssistant)
        with pytest.raises(MerakiConnectionError) as exc_info:
            get_webhook_url(hass, "webhook_123", "https://localhost")
        assert "public URL" in str(exc_info.value)

    def test_local_domain_url_raises_error(self) -> None:
        """Test get_webhook_url raises error for .local domain URL."""
        hass = MagicMock(spec=HomeAssistant)
        with pytest.raises(MerakiConnectionError) as exc_info:
            get_webhook_url(hass, "webhook_123", "https://home.local")
        assert "public URL" in str(exc_info.value)

    def test_trailing_slash_removed(self) -> None:
        """Test get_webhook_url removes trailing slash."""
        hass = MagicMock(spec=HomeAssistant)
        result = get_webhook_url(hass, "webhook_123", "https://mysite.example.com/")
        assert result == "https://mysite.example.com/api/webhook/webhook_123"


class TestAsyncRegisterWebhook:
    """Tests for async_register_webhook function."""

    @pytest.mark.asyncio
    async def test_register_webhook_success(self) -> None:
        """Test successful webhook registration."""
        hass = MagicMock(spec=HomeAssistant)
        api_client = AsyncMock()
        entry = MagicMock()
        entry.data = {"webhook_url": "https://public.example.com"}

        with patch(
            "custom_components.meraki_ha.webhook.get_webhook_url",
            return_value="https://public.example.com/api/webhook/wh_123",
        ):
            await async_register_webhook(
                hass,
                "wh_123",
                "secret",
                api_client,
                entry=entry,
                config_entry_id="entry_id",
            )

        api_client.register_webhook.assert_called_once_with(
            "https://public.example.com/api/webhook/wh_123", "secret", "entry_id"
        )

    @pytest.mark.asyncio
    async def test_register_webhook_no_config_entry_id(self) -> None:
        """Test webhook registration skipped without config entry ID."""
        hass = MagicMock(spec=HomeAssistant)
        api_client = AsyncMock()
        entry = MagicMock()
        entry.data = {"webhook_url": "https://public.example.com"}

        with patch(
            "custom_components.meraki_ha.webhook.get_webhook_url",
            return_value="https://public.example.com/api/webhook/wh_123",
        ):
            await async_register_webhook(
                hass,
                "wh_123",
                "secret",
                api_client,
                entry=entry,
                config_entry_id=None,
            )

        api_client.register_webhook.assert_not_called()

    @pytest.mark.asyncio
    async def test_register_webhook_handles_error(self) -> None:
        """Test webhook registration handles errors gracefully."""
        hass = MagicMock(spec=HomeAssistant)
        api_client = AsyncMock()
        entry = MagicMock()
        entry.data = {}

        with patch(
            "custom_components.meraki_ha.webhook.get_webhook_url",
            side_effect=MerakiConnectionError("Test error"),
        ):
            # Should not raise
            await async_register_webhook(
                hass,
                "wh_123",
                "secret",
                api_client,
                entry=entry,
                config_entry_id="entry_id",
            )


class TestAsyncUnregisterWebhook:
    """Tests for async_unregister_webhook function."""

    @pytest.mark.asyncio
    async def test_unregister_webhook_success(self) -> None:
        """Test successful webhook unregistration."""
        hass = MagicMock(spec=HomeAssistant)
        api_client = AsyncMock()

        await async_unregister_webhook(hass, "entry_123", api_client)

        api_client.unregister_webhook.assert_called_once_with("entry_123")


class TestAsyncHandleWebhook:
    """Tests for async_handle_webhook function."""

    @pytest.fixture
    def mock_request(self) -> MagicMock:
        """Create a mock request."""
        request = MagicMock(spec=web.Request)
        return request

    @pytest.mark.asyncio
    async def test_handle_webhook_invalid_json(self, mock_request: MagicMock) -> None:
        """Test handling webhook with invalid JSON."""
        hass = MagicMock(spec=HomeAssistant)
        mock_request.json = AsyncMock(side_effect=ValueError("Invalid JSON"))

        # Should not raise
        await async_handle_webhook(hass, "wh_123", mock_request)

    @pytest.mark.asyncio
    async def test_handle_webhook_unknown_entry(self, mock_request: MagicMock) -> None:
        """Test handling webhook for unknown config entry."""
        hass = MagicMock(spec=HomeAssistant)
        hass.data = {}
        mock_request.json = AsyncMock(return_value={"alertType": "test"})

        # Should not raise
        await async_handle_webhook(hass, "wh_123", mock_request)

    @pytest.mark.asyncio
    async def test_handle_webhook_invalid_secret(self, mock_request: MagicMock) -> None:
        """Test handling webhook with invalid secret."""
        hass = MagicMock(spec=HomeAssistant)
        hass.data = {
            DOMAIN: {"wh_123": {"secret": "correct_secret", "coordinator": MagicMock()}}
        }
        mock_request.json = AsyncMock(
            return_value={"alertType": "test", "sharedSecret": "wrong_secret"}
        )

        # Should not raise
        await async_handle_webhook(hass, "wh_123", mock_request)

    @pytest.mark.asyncio
    async def test_handle_webhook_no_coordinator(self, mock_request: MagicMock) -> None:
        """Test handling webhook without coordinator."""
        hass = MagicMock(spec=HomeAssistant)
        hass.data = {DOMAIN: {"wh_123": {"secret": "secret"}}}
        mock_request.json = AsyncMock(
            return_value={"alertType": "test", "sharedSecret": "secret"}
        )

        # Should not raise
        await async_handle_webhook(hass, "wh_123", mock_request)

    @pytest.mark.asyncio
    async def test_handle_webhook_ap_down_alert(self, mock_request: MagicMock) -> None:
        """Test handling AP down alert webhook."""
        device = {"serial": "AP-1234", "status": "online"}
        coordinator = MagicMock()
        coordinator.data = {"devices": [device]}
        coordinator.devices_by_serial = {"AP-1234": device}
        coordinator.async_update_listeners = MagicMock()

        def _update_device_status(serial, is_online):
            device["status"] = "online" if is_online else "offline"

        coordinator._update_device_status_immediate.side_effect = _update_device_status

        config_entry = MagicMock()
        config_entry.options = {"webhook_shared_secret": "secret"}

        hass = MagicMock(spec=HomeAssistant)
        hass.data = {
            DOMAIN: {"wh_123": {"secret": "secret", "coordinator": coordinator}}
        }
        hass.config_entries.async_get_entry.return_value = config_entry

        mock_request.json = AsyncMock(
            return_value={
                "alertType": "APs went down",
                "deviceSerial": "AP-1234",
                "sharedSecret": "secret",
            }
        )

        await async_handle_webhook(hass, "wh_123", mock_request)

        assert device["status"] == "offline"
        coordinator.async_update_listeners.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_webhook_client_connectivity_changed(
        self, mock_request: MagicMock
    ) -> None:
        """Test handling client connectivity changed webhook."""
        client = {"mac": "AA:BB:CC:DD:EE:FF", "status": "Online"}
        coordinator = MagicMock()
        coordinator.data = {
            "devices": [],
            "clients": [client],
        }
        coordinator.async_update_listeners = MagicMock()

        def _update_client_status(mac, is_online):
            client["status"] = "Online" if is_online else "Offline"

        coordinator._update_client_status_immediate.side_effect = _update_client_status

        config_entry = MagicMock()
        config_entry.options = {"webhook_shared_secret": "secret"}

        hass = MagicMock(spec=HomeAssistant)
        hass.data = {
            DOMAIN: {"wh_123": {"secret": "secret", "coordinator": coordinator}}
        }
        hass.config_entries.async_get_entry.return_value = config_entry

        mock_request.json = AsyncMock(
            return_value={
                "alertType": "Client connectivity changed",
                "alertData": {"mac": "AA:BB:CC:DD:EE:FF", "connected": False},
                "sharedSecret": "secret",
            }
        )

        await async_handle_webhook(hass, "wh_123", mock_request)

        assert client["status"] == "Offline"
        coordinator.async_update_listeners.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_webhook_unknown_alert_type(
        self, mock_request: MagicMock
    ) -> None:
        """Test handling unknown alert type webhook."""
        coordinator = MagicMock()
        coordinator.data = {"devices": [], "clients": []}

        hass = MagicMock(spec=HomeAssistant)
        hass.data = {
            DOMAIN: {"wh_123": {"secret": "secret", "coordinator": coordinator}}
        }
        mock_request.json = AsyncMock(
            return_value={
                "alertType": "Unknown alert",
                "sharedSecret": "secret",
            }
        )

        # Should not raise, just log and ignore
        await async_handle_webhook(hass, "wh_123", mock_request)
