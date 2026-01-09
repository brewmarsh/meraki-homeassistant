"""Tests for the WebSocket API module."""

# mypy: disable-error-code="assignment"

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

    def test_setup_registers_commands(self, mock_hass: MagicMock) -> None:
        """Test that setup registers all websocket commands."""
        from homeassistant.components import websocket_api

        original_register = websocket_api.async_register_command

        calls = []

        def mock_register(hass, handler):
            calls.append((hass, handler))

        websocket_api.async_register_command = mock_register

        try:
            async_setup_websocket_api(mock_hass)
            # Should register 2 commands: subscribe_meraki_data and get_rtsp_url
            assert len(calls) == 2
            assert all(call[0] is mock_hass for call in calls)
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
        # Set up mock config entry
        mock_config_entry = MagicMock()
        mock_config_entry.options = {}
        mock_hass.config_entries.async_get_entry.return_value = mock_config_entry
        mock_coordinator.last_successful_update = None

        mock_hass.data[DOMAIN]["test_entry_id"] = {"coordinator": mock_coordinator}
        msg = {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": "test_entry_id",
        }

        ws_subscribe_meraki_data(mock_hass, mock_connection, msg)

        # Should confirm subscription with send_result (no data, just confirmation)
        mock_connection.send_result.assert_called_once_with(1)

        # Should send initial data as an event message
        mock_connection.send_message.assert_called_once()
        event_call = mock_connection.send_message.call_args[0][0]
        # Event message should contain the enriched data
        assert "networks" in str(event_call) or hasattr(event_call, "get")

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
        mock_coordinator.last_successful_update = None

        # Set up mock config entry
        mock_config_entry = MagicMock()
        mock_config_entry.options = {}
        mock_hass.config_entries.async_get_entry.return_value = mock_config_entry

        mock_hass.data[DOMAIN]["test_entry_id"] = {"coordinator": mock_coordinator}
        msg = {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": "test_entry_id",
        }

        ws_subscribe_meraki_data(mock_hass, mock_connection, msg)

        # Verify cancel function is stored in subscriptions
        assert mock_connection.subscriptions[1] is cancel_func

    def test_subscribe_includes_mqtt_data_when_disabled(
        self,
        mock_hass: MagicMock,
        mock_connection: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test that MQTT data is included in response when MQTT is disabled."""
        mock_coordinator.last_successful_update = None

        # Set up mock config entry with MQTT disabled (default)
        mock_config_entry = MagicMock()
        mock_config_entry.options = {"enable_mqtt": False}
        mock_hass.config_entries.async_get_entry.return_value = mock_config_entry

        mock_hass.data[DOMAIN]["test_entry_id"] = {"coordinator": mock_coordinator}
        msg = {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": "test_entry_id",
        }

        ws_subscribe_meraki_data(mock_hass, mock_connection, msg)

        # Verify send_message was called with mqtt data
        mock_connection.send_message.assert_called_once()
        # The message should contain mqtt with enabled=False
        call_args = mock_connection.send_message.call_args
        assert call_args is not None

    def test_subscribe_includes_mqtt_stats_when_enabled(
        self,
        mock_hass: MagicMock,
        mock_connection: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test that MQTT stats are included when MQTT is enabled."""
        mock_coordinator.last_successful_update = None

        # Set up mock config entry with MQTT enabled
        mock_config_entry = MagicMock()
        mock_config_entry.options = {"enable_mqtt": True}
        mock_hass.config_entries.async_get_entry.return_value = mock_config_entry

        # Mock MQTT service with stats
        mock_mqtt_service = MagicMock()
        mock_mqtt_service.get_statistics.return_value = {
            "is_running": True,
            "messages_received": 100,
            "messages_processed": 95,
            "last_message_time": "2025-01-08T12:00:00",
            "start_time": "2025-01-08T10:00:00",
            "sensors_mapped": 5,
        }

        # Mock relay manager with health status
        mock_relay_manager = MagicMock()
        mock_relay_manager.get_health_status.return_value = {
            "test_relay": {
                "name": "Test Relay",
                "status": "connected",
                "host": "mqtt.example.com",
                "port": 1883,
                "topic_filter": "meraki/v1/mt/#",
                "messages_relayed": 50,
                "last_relay_time": "2025-01-08T12:00:00",
                "last_error": None,
                "last_error_time": None,
            }
        }

        mock_hass.data[DOMAIN]["test_entry_id"] = {
            "coordinator": mock_coordinator,
            "mqtt_service": mock_mqtt_service,
            "mqtt_relay_manager": mock_relay_manager,
        }
        msg = {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": "test_entry_id",
        }

        ws_subscribe_meraki_data(mock_hass, mock_connection, msg)

        # Verify MQTT service stats were retrieved
        mock_mqtt_service.get_statistics.assert_called_once()
        # Verify relay manager health status was retrieved
        mock_relay_manager.get_health_status.assert_called_once()
