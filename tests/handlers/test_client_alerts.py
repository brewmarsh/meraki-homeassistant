"""Tests for client alerts handler."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.handlers.client_alerts import (
    _maybe_auto_sync_client,
    async_handle_client_alert,
)


class TaskCaptureMock(MagicMock):
    """Mock that captures and closes coroutines to avoid warnings."""

    def __init__(self, *args, **kwargs):
        """Initialize with task tracking."""
        super().__init__(*args, **kwargs)
        self._captured_tasks = []

    def __call__(self, *args, **kwargs):
        """Capture and close any coroutines in the arguments."""
        super().__call__(*args, **kwargs)
        # Close any coroutines passed as arguments
        for arg in args:
            if hasattr(arg, "close"):
                arg.close()
                self._captured_tasks.append(arg)
        return None


@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.hass = MagicMock()
    coordinator.hass.bus = MagicMock()
    coordinator.hass.bus.async_fire = MagicMock()
    # Use TaskCaptureMock to capture and close coroutines properly
    coordinator.hass.async_create_task = TaskCaptureMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}
    coordinator._update_client_status_immediate = MagicMock()
    coordinator.async_update_listeners = MagicMock()
    coordinator._targeted_client_refresh = AsyncMock()
    # Mock schedule_debounced_refresh to capture and close coroutines
    coordinator.schedule_debounced_refresh = TaskCaptureMock()
    coordinator.api = MagicMock()
    coordinator.api.network = MagicMock()
    coordinator.api.network.provision_network_clients = AsyncMock()
    return coordinator


class TestClientAlerts:
    """Test client alerts handler."""

    @pytest.mark.asyncio
    async def test_new_client_connected(self, mock_coordinator):
        """Test handling new client connected alert."""
        data = {
            "networkId": "N_123",
            "networkName": "Test Network",
            "alertData": {
                "mac": "AA:BB:CC:DD:EE:FF",
                "name": "New Device",
            },
        }

        await async_handle_client_alert(mock_coordinator, "New client connected", data)

        # Should fire event
        mock_coordinator.hass.bus.async_fire.assert_called_once()
        call_args = mock_coordinator.hass.bus.async_fire.call_args
        assert "meraki_ha_new_client" in call_args[0][0]

        # Should schedule debounced refresh
        mock_coordinator.schedule_debounced_refresh.assert_called()

    @pytest.mark.asyncio
    async def test_client_blocked(self, mock_coordinator):
        """Test handling client blocked alert."""
        data = {
            "networkId": "N_123",
            "networkName": "Test Network",
            "alertData": {
                "mac": "AA:BB:CC:DD:EE:FF",
            },
        }

        await async_handle_client_alert(mock_coordinator, "Client blocked", data)

        # Should fire event
        mock_coordinator.hass.bus.async_fire.assert_called_once()
        call_args = mock_coordinator.hass.bus.async_fire.call_args
        assert "meraki_ha_client_blocked" in call_args[0][0]

        # Should update client status
        mock_coordinator._update_client_status_immediate.assert_called_once_with(
            "AA:BB:CC:DD:EE:FF", False
        )

    @pytest.mark.asyncio
    async def test_client_connectivity_changed(self, mock_coordinator):
        """Test handling client connectivity changed alert."""
        data = {
            "networkId": "N_123",
            "alertData": {
                "mac": "AA:BB:CC:DD:EE:FF",
                "connected": True,
            },
        }

        await async_handle_client_alert(
            mock_coordinator, "Client connectivity changed", data
        )

        mock_coordinator._update_client_status_immediate.assert_called_once_with(
            "AA:BB:CC:DD:EE:FF", True
        )
        mock_coordinator.async_update_listeners.assert_called_once()

    @pytest.mark.asyncio
    async def test_client_alert_missing_mac(self, mock_coordinator):
        """Test that alerts without MAC are handled gracefully."""
        data = {
            "networkId": "N_123",
            "alertData": {},  # No MAC
        }

        # Should not raise
        await async_handle_client_alert(
            mock_coordinator, "Client connectivity changed", data
        )

        # Should not update anything
        mock_coordinator._update_client_status_immediate.assert_not_called()


class TestAutoSyncClient:
    """Test auto-sync functionality."""

    @pytest.mark.asyncio
    async def test_auto_sync_disabled(self, mock_coordinator):
        """Test that auto-sync doesn't run when disabled."""
        mock_coordinator.config_entry.options = {"sync_on_new_client": False}

        await _maybe_auto_sync_client(mock_coordinator, "AA:BB:CC:DD:EE:FF", "N_123")

        mock_coordinator.api.network.provision_network_clients.assert_not_called()

    @pytest.mark.asyncio
    async def test_auto_sync_no_network_id(self, mock_coordinator):
        """Test that auto-sync handles missing network ID."""
        mock_coordinator.config_entry.options = {"sync_on_new_client": True}

        await _maybe_auto_sync_client(mock_coordinator, "AA:BB:CC:DD:EE:FF", None)

        mock_coordinator.api.network.provision_network_clients.assert_not_called()
