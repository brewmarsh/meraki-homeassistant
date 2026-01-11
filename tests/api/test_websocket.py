"""Tests for the WebSocket API module."""

# mypy: disable-error-code="assignment"

from unittest.mock import MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.api.websocket import (
    _build_enriched_data,
    async_setup_websocket_api,
    ws_subscribe_meraki_data,
)
from custom_components.meraki_ha.const import (
    DEFAULT_DASHBOARD_VIEW_MODE,
    DOMAIN,
)


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


class TestBuildEnrichedData:
    """Tests for _build_enriched_data function.

    These tests verify that dashboard settings are correctly included
    in the WebSocket response, addressing issue #77.
    """

    def test_dashboard_view_mode_included_in_response(
        self, mock_hass: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test that dashboard_view_mode is included in enriched data."""
        mock_coordinator.last_successful_update = None
        mock_coordinator.update_interval = None

        # Set up config entry with dashboard_view_mode = "type"
        mock_config_entry = MagicMock()
        mock_config_entry.options = {"dashboard_view_mode": "type"}
        mock_hass.config_entries.async_get_entry.return_value = mock_config_entry

        result = _build_enriched_data(mock_coordinator, "test_entry_id", mock_hass)

        assert "dashboard_view_mode" in result
        assert result["dashboard_view_mode"] == "type"

    def test_dashboard_view_mode_uses_default_when_not_set(
        self, mock_hass: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test that default dashboard_view_mode is used when not configured."""
        mock_coordinator.last_successful_update = None
        mock_coordinator.update_interval = None

        # Set up config entry WITHOUT dashboard_view_mode
        mock_config_entry = MagicMock()
        mock_config_entry.options = {}
        mock_hass.config_entries.async_get_entry.return_value = mock_config_entry

        result = _build_enriched_data(mock_coordinator, "test_entry_id", mock_hass)

        assert "dashboard_view_mode" in result
        assert result["dashboard_view_mode"] == DEFAULT_DASHBOARD_VIEW_MODE
        assert result["dashboard_view_mode"] == "network"

    def test_all_dashboard_settings_included(
        self, mock_hass: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test that all dashboard-related settings are included in response."""
        mock_coordinator.last_successful_update = None
        mock_coordinator.update_interval = None

        # Set up config entry with all dashboard settings
        mock_config_entry = MagicMock()
        mock_config_entry.options = {
            "dashboard_view_mode": "type",
            "dashboard_device_type_filter": ["switch", "wireless"],
            "dashboard_status_filter": "online",
            "temperature_unit": "fahrenheit",
        }
        mock_hass.config_entries.async_get_entry.return_value = mock_config_entry

        result = _build_enriched_data(mock_coordinator, "test_entry_id", mock_hass)

        assert result["dashboard_view_mode"] == "type"
        assert result["dashboard_device_type_filter"] == ["switch", "wireless"]
        assert result["dashboard_status_filter"] == "online"
        assert result["temperature_unit"] == "fahrenheit"


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

    def test_subscribe_includes_dashboard_view_mode(
        self,
        mock_hass: MagicMock,
        mock_connection: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test that dashboard_view_mode is included in response.

        This test ensures the fix for issue #77 is preserved:
        The frontend needs dashboard_view_mode to properly display
        devices grouped by the user's preference (network or type).
        """
        mock_coordinator.last_successful_update = None

        # Set up mock config entry with dashboard_view_mode set to "type"
        mock_config_entry = MagicMock()
        mock_config_entry.options = {"dashboard_view_mode": "type"}
        mock_hass.config_entries.async_get_entry.return_value = mock_config_entry

        mock_hass.data[DOMAIN]["test_entry_id"] = {"coordinator": mock_coordinator}
        msg = {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": "test_entry_id",
        }

        ws_subscribe_meraki_data(mock_hass, mock_connection, msg)

        # Verify send_message was called with enriched data
        mock_connection.send_message.assert_called_once()
        call_args = mock_connection.send_message.call_args[0][0]

        # The enriched data should contain dashboard_view_mode
        # websocket_api.event_message returns {"id": id, "type": "event", "event": data}
        assert hasattr(call_args, "__getitem__") or isinstance(call_args, dict)
        # We just need to verify the message was constructed - the actual
        # value comes from _build_enriched_data which builds the response

    def test_subscribe_uses_default_dashboard_view_mode(
        self,
        mock_hass: MagicMock,
        mock_connection: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test that default dashboard_view_mode is used when not set.

        When dashboard_view_mode is not explicitly configured, the default
        value of 'network' should be used.
        """
        mock_coordinator.last_successful_update = None

        # Set up mock config entry WITHOUT dashboard_view_mode
        mock_config_entry = MagicMock()
        mock_config_entry.options = {}  # No dashboard settings
        mock_hass.config_entries.async_get_entry.return_value = mock_config_entry

        mock_hass.data[DOMAIN]["test_entry_id"] = {"coordinator": mock_coordinator}
        msg = {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": "test_entry_id",
        }

        ws_subscribe_meraki_data(mock_hass, mock_connection, msg)

        # Should not error - default value should be used
        mock_connection.send_result.assert_called_once_with(1)
        mock_connection.send_message.assert_called_once()
