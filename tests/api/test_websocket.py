"""Tests for the WebSocket API module."""

from unittest.mock import MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.api.websocket import (
    async_setup_websocket_api,
    ws_subscribe_meraki_data,
)
from custom_components.meraki_ha.const import DOMAIN


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock hass instance."""
    hass = MagicMock(spec=HomeAssistant)
    hass.data = {DOMAIN: {}}
    return hass


@pytest.fixture
def mock_connection() -> MagicMock:
    """Create a mock websocket connection."""
    connection = MagicMock()
    connection.subscriptions = {}
    return connection


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = {"networks": [], "devices": []}
    coordinator.async_add_listener = MagicMock(return_value=MagicMock())
    return coordinator


class TestAsyncSetupWebsocketApi:
    """Tests for async_setup_websocket_api function."""

    def test_setup_registers_command(self, mock_hass: MagicMock) -> None:
        """Test that setup registers the websocket command."""
        from homeassistant.components import websocket_api

        original_register = websocket_api.async_register_command

        calls = []

        def mock_register(hass, handler):
            calls.append((hass, handler))

        websocket_api.async_register_command = mock_register

        try:
            async_setup_websocket_api(mock_hass)
            assert len(calls) == 1
            assert calls[0][0] is mock_hass
        finally:
            websocket_api.async_register_command = original_register


class TestWsSubscribeMerakiData:
    """Tests for ws_subscribe_meraki_data function."""

    def test_config_entry_not_found(
        self, mock_hass: MagicMock, mock_connection: MagicMock
    ) -> None:
        """Test error response when config entry not found."""
        msg = {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": "nonexistent_entry",
        }

        ws_subscribe_meraki_data(mock_hass, mock_connection, msg)

        mock_connection.send_error.assert_called_once_with(
            1, "not_found", "Config entry not found"
        )

    def test_subscribe_success(
        self,
        mock_hass: MagicMock,
        mock_connection: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test successful subscription to Meraki data."""
        mock_hass.data[DOMAIN]["test_entry_id"] = {"coordinator": mock_coordinator}
        msg = {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": "test_entry_id",
        }

        ws_subscribe_meraki_data(mock_hass, mock_connection, msg)

        # Should send initial data
        mock_connection.send_result.assert_called_once_with(1, mock_coordinator.data)

        # Should register listener
        mock_coordinator.async_add_listener.assert_called_once()

        # Should add subscription to connection
        assert 1 in mock_connection.subscriptions

    def test_subscribe_registers_update_listener(
        self,
        mock_hass: MagicMock,
        mock_connection: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test that subscription registers update listener."""
        cancel_func = MagicMock()
        mock_coordinator.async_add_listener.return_value = cancel_func
        mock_hass.data[DOMAIN]["test_entry_id"] = {"coordinator": mock_coordinator}
        msg = {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": "test_entry_id",
        }

        ws_subscribe_meraki_data(mock_hass, mock_connection, msg)

        # Verify cancel function is stored in subscriptions
        assert mock_connection.subscriptions[1] is cancel_func

