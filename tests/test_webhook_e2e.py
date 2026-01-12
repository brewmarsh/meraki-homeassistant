"""End-to-end integration tests for webhook flow."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import web
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.webhook import async_handle_webhook


class CoroutineConsumingMock(MagicMock):
    """A MagicMock that properly consumes coroutines passed to it.

    This prevents 'coroutine was never awaited' warnings when mocking
    async_create_task or schedule_debounced_refresh, which receive coroutines
    but don't schedule them in the test environment.
    """

    def __call__(self, *args: Any, **kwargs: Any) -> MagicMock:
        """Consume any coroutine passed in the arguments."""
        for arg in args:
            if asyncio.iscoroutine(arg):
                arg.close()
        for value in kwargs.values():
            if asyncio.iscoroutine(value):
                value.close()
        return super().__call__(*args, **kwargs)


def create_sync_mock_for_async() -> MagicMock:
    """Create a mock that returns a completed future instead of a coroutine.

    This avoids 'coroutine was never awaited' warnings when the mock's return
    value is passed to async_create_task instead of being awaited directly.
    """
    future: asyncio.Future[None] = asyncio.Future()
    future.set_result(None)
    mock = MagicMock(return_value=future)
    return mock


class TestWebhookE2EFlow:
    """End-to-end tests for complete webhook flow."""

    @pytest.fixture
    def mock_coordinator(self) -> MagicMock:
        """Create a fully-configured mock coordinator."""
        coordinator = MagicMock()
        coordinator.hass = MagicMock(spec=HomeAssistant)
        coordinator.hass.bus = MagicMock()
        coordinator.hass.bus.async_fire = MagicMock()
        # Consume coroutines passed to async_create_task
        coordinator.hass.async_create_task = CoroutineConsumingMock()

        # Mock data structures
        coordinator.data = {
            "devices": [
                {
                    "serial": "Q2XX-TEST-1234",
                    "name": "Test AP",
                    "status": "online",
                    "networkId": "N_123456",
                }
            ],
            "clients": [
                {
                    "mac": "00:11:22:33:44:55",
                    "description": "Test Client",
                    "networkId": "N_123456",
                    "status": "online",
                }
            ],
        }

        coordinator.devices_by_serial = {
            "Q2XX-TEST-1234": coordinator.data["devices"][0]
        }

        # Mock methods
        coordinator._update_device_status_immediate = MagicMock()
        coordinator._update_client_status_immediate = MagicMock()
        coordinator.async_update_listeners = MagicMock()
        coordinator.mark_webhook_received = MagicMock(return_value=True)
        # Consume coroutines passed to schedule_debounced_refresh
        coordinator.schedule_debounced_refresh = CoroutineConsumingMock()
        # Return a Future instead of coroutine to avoid 'never awaited' warnings
        coordinator._targeted_device_refresh = create_sync_mock_for_async()
        coordinator._targeted_client_refresh = create_sync_mock_for_async()

        # Mock config entry
        coordinator.config_entry = MagicMock(spec=ConfigEntry)
        coordinator.config_entry.options = {"webhook_shared_secret": "test_secret"}

        # Mock API client
        coordinator.api = MagicMock()
        coordinator.api.network = MagicMock()
        coordinator.api.network.provision_network_clients = AsyncMock()

        # Webhook tracking
        coordinator._last_webhook_received = None
        coordinator._webhook_received_count = 0

        return coordinator

    @pytest.fixture
    def mock_request(self) -> MagicMock:
        """Create a mock aiohttp request."""
        request = MagicMock(spec=web.Request)
        return request

    @pytest.mark.asyncio
    async def test_e2e_device_down_webhook_flow(
        self,
        mock_coordinator: MagicMock,
        mock_request: MagicMock,
    ) -> None:
        """Test complete flow: webhook received → state update → targeted refresh."""
        # Setup Home Assistant
        hass = MagicMock(spec=HomeAssistant)
        config_entry = MagicMock()
        config_entry.options = {"webhook_shared_secret": "test_secret"}

        hass.data = {
            DOMAIN: {
                "wh_test": {
                    "coordinator": mock_coordinator,
                }
            }
        }
        hass.config_entries.async_get_entry.return_value = config_entry

        # Setup webhook payload
        webhook_payload = {
            "alertType": "APs went down",
            "alertId": "alert_12345",
            "deviceSerial": "Q2XX-TEST-1234",
            "deviceName": "Test AP",
            "networkId": "N_123456",
            "networkName": "Test Network",
            "occurredAt": "2026-01-12T10:00:00Z",
            "sharedSecret": "test_secret",
        }
        mock_request.json = AsyncMock(return_value=webhook_payload)

        # Execute webhook handler
        response = await async_handle_webhook(hass, "wh_test", mock_request)

        # Verify response
        assert response.status == 200

        # Verify immediate state update was called
        mock_coordinator._update_device_status_immediate.assert_called_once_with(
            "Q2XX-TEST-1234", False
        )

        # Verify listeners were notified
        mock_coordinator.async_update_listeners.assert_called()

        # Verify webhook was tracked for polling reduction
        mock_coordinator.mark_webhook_received.assert_called_once()

        # Verify targeted refresh was scheduled
        assert mock_coordinator.hass.async_create_task.called

    @pytest.mark.asyncio
    async def test_e2e_client_connectivity_webhook_flow(
        self,
        mock_coordinator: MagicMock,
        mock_request: MagicMock,
    ) -> None:
        """Test complete flow for client connectivity change."""
        # Setup Home Assistant
        hass = MagicMock(spec=HomeAssistant)
        config_entry = MagicMock()
        config_entry.options = {
            "webhook_shared_secret": "test_secret",
            "sync_on_new_client": False,  # Disable auto-sync for this test
        }

        hass.data = {
            DOMAIN: {
                "wh_test": {
                    "coordinator": mock_coordinator,
                }
            }
        }
        hass.config_entries.async_get_entry.return_value = config_entry

        # Setup webhook payload
        webhook_payload = {
            "alertType": "Client connectivity changed",
            "alertId": "alert_67890",
            "alertData": {
                "mac": "00:11:22:33:44:55",
                "clientMac": "00:11:22:33:44:55",
            },
            "networkId": "N_123456",
            "networkName": "Test Network",
            "occurredAt": "2026-01-12T10:05:00Z",
            "sharedSecret": "test_secret",
        }
        mock_request.json = AsyncMock(return_value=webhook_payload)

        # Execute webhook handler
        response = await async_handle_webhook(hass, "wh_test", mock_request)

        # Verify response
        assert response.status == 200

        # Verify immediate state update
        mock_coordinator._update_client_status_immediate.assert_called()

        # Verify debounced refresh was scheduled
        mock_coordinator.schedule_debounced_refresh.assert_called()

        # Verify listeners were notified
        mock_coordinator.async_update_listeners.assert_called()

    @pytest.mark.asyncio
    async def test_e2e_duplicate_webhook_deduplication(
        self,
        mock_coordinator: MagicMock,
        mock_request: MagicMock,
    ) -> None:
        """Test that duplicate webhooks are properly deduplicated."""
        # Setup Home Assistant
        hass = MagicMock(spec=HomeAssistant)
        config_entry = MagicMock()
        config_entry.options = {"webhook_shared_secret": "test_secret"}

        hass.data = {
            DOMAIN: {
                "wh_test": {
                    "coordinator": mock_coordinator,
                }
            }
        }
        hass.config_entries.async_get_entry.return_value = config_entry

        # Setup webhook payload
        webhook_payload = {
            "alertType": "Switches went down",
            "alertId": "alert_duplicate_test",
            "deviceSerial": "Q2XX-TEST-1234",
            "sharedSecret": "test_secret",
        }
        mock_request.json = AsyncMock(return_value=webhook_payload)

        # First webhook - should be processed
        mock_coordinator.mark_webhook_received.return_value = True
        response1 = await async_handle_webhook(hass, "wh_test", mock_request)
        assert response1.status == 200

        # Get call counts after first webhook
        first_update_count = mock_coordinator._update_device_status_immediate.call_count

        # Second webhook with same alertId - should be deduplicated
        mock_coordinator.mark_webhook_received.return_value = False
        response2 = await async_handle_webhook(hass, "wh_test", mock_request)
        assert response2.status == 200

        # Verify second webhook didn't trigger additional processing
        assert (
            mock_coordinator._update_device_status_immediate.call_count
            == first_update_count
        )

    @pytest.mark.asyncio
    async def test_e2e_ssid_settings_changed_webhook(
        self,
        mock_coordinator: MagicMock,
        mock_request: MagicMock,
    ) -> None:
        """Test SSID settings change webhook triggers network refresh."""
        # Setup Home Assistant
        hass = MagicMock(spec=HomeAssistant)
        config_entry = MagicMock()
        config_entry.options = {"webhook_shared_secret": "test_secret"}

        hass.data = {
            DOMAIN: {
                "wh_test": {
                    "coordinator": mock_coordinator,
                }
            }
        }
        hass.config_entries.async_get_entry.return_value = config_entry

        # Mock targeted SSID refresh
        mock_coordinator._targeted_ssid_refresh = AsyncMock()

        # Setup webhook payload
        webhook_payload = {
            "alertType": "SSID settings changed",
            "alertId": "alert_ssid_change",
            "networkId": "N_123456",
            "networkName": "Test Network",
            "sharedSecret": "test_secret",
        }
        mock_request.json = AsyncMock(return_value=webhook_payload)

        # Execute webhook handler
        response = await async_handle_webhook(hass, "wh_test", mock_request)

        # Verify response
        assert response.status == 200

        # Verify debounced SSID refresh was scheduled
        mock_coordinator.schedule_debounced_refresh.assert_called()
        call_args = mock_coordinator.schedule_debounced_refresh.call_args
        assert "ssid:N_123456" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_e2e_security_alert_event_fired(
        self,
        mock_coordinator: MagicMock,
        mock_request: MagicMock,
    ) -> None:
        """Test security alerts fire Home Assistant events."""
        # Setup Home Assistant
        hass = MagicMock(spec=HomeAssistant)
        config_entry = MagicMock()
        config_entry.options = {"webhook_shared_secret": "test_secret"}

        hass.data = {
            DOMAIN: {
                "wh_test": {
                    "coordinator": mock_coordinator,
                }
            }
        }
        hass.config_entries.async_get_entry.return_value = config_entry

        # Setup webhook payload
        webhook_payload = {
            "alertType": "Rogue AP detected",
            "alertId": "alert_security_123",
            "deviceSerial": "Q2XX-ROGUE-AP",
            "alertData": {
                "ssid": "Suspicious-Network",
                "bssid": "AA:BB:CC:DD:EE:FF",
            },
            "networkId": "N_123456",
            "sharedSecret": "test_secret",
        }
        mock_request.json = AsyncMock(return_value=webhook_payload)

        # Execute webhook handler
        response = await async_handle_webhook(hass, "wh_test", mock_request)

        # Verify response
        assert response.status == 200

        # Verify HA event was fired
        mock_coordinator.hass.bus.async_fire.assert_called()
        event_call = mock_coordinator.hass.bus.async_fire.call_args
        assert "meraki_ha_security_alert" in event_call[0][0]

    @pytest.mark.asyncio
    async def test_e2e_webhook_with_invalid_payload(
        self,
        mock_coordinator: MagicMock,
        mock_request: MagicMock,
    ) -> None:
        """Test webhook with missing required fields is handled gracefully."""
        # Setup Home Assistant
        hass = MagicMock(spec=HomeAssistant)
        config_entry = MagicMock()
        config_entry.options = {"webhook_shared_secret": "test_secret"}

        hass.data = {
            DOMAIN: {
                "wh_test": {
                    "coordinator": mock_coordinator,
                }
            }
        }
        hass.config_entries.async_get_entry.return_value = config_entry

        # Setup webhook payload with missing deviceSerial
        webhook_payload = {
            "alertType": "APs went down",
            "alertId": "alert_invalid",
            # Missing deviceSerial - required for device alerts
            "networkId": "N_123456",
            "sharedSecret": "test_secret",
        }
        mock_request.json = AsyncMock(return_value=webhook_payload)

        # Execute webhook handler - should not raise
        response = await async_handle_webhook(hass, "wh_test", mock_request)

        # Verify response (still 200, but no processing occurred)
        assert response.status == 200

        # Verify immediate state update was NOT called (missing serial)
        mock_coordinator._update_device_status_immediate.assert_not_called()

    @pytest.mark.asyncio
    async def test_e2e_polling_reduction_after_webhook(
        self,
        mock_coordinator: MagicMock,
        mock_request: MagicMock,
    ) -> None:
        """Test that polling reduction is enabled after webhook reception."""
        # Setup Home Assistant
        hass = MagicMock(spec=HomeAssistant)
        config_entry = MagicMock()
        config_entry.options = {
            "webhook_shared_secret": "test_secret",
            "webhook_polling_reduction": True,
        }

        hass.data = {
            DOMAIN: {
                "wh_test": {
                    "coordinator": mock_coordinator,
                }
            }
        }
        hass.config_entries.async_get_entry.return_value = config_entry

        # Initially, no webhooks received
        assert mock_coordinator._last_webhook_received is None

        # Setup and send webhook
        webhook_payload = {
            "alertType": "Cameras came up",
            "alertId": "alert_camera_up",
            "deviceSerial": "Q2XX-CAM-001",
            "sharedSecret": "test_secret",
        }
        mock_request.json = AsyncMock(return_value=webhook_payload)

        # Mock mark_webhook_received to simulate coordinator behavior
        def mark_received(alert_type: str, alert_id: str | None) -> bool:
            mock_coordinator._last_webhook_received = datetime.now()
            mock_coordinator._webhook_received_count += 1
            return True

        mock_coordinator.mark_webhook_received.side_effect = mark_received

        # Execute webhook handler
        response = await async_handle_webhook(hass, "wh_test", mock_request)

        # Verify response
        assert response.status == 200

        # Verify webhook tracking was updated
        assert mock_coordinator._last_webhook_received is not None
        assert mock_coordinator._webhook_received_count == 1
