"""Tests for the UpdateProcessor."""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from custom_components.meraki_ha.core.coordinator_helpers.update_processor import UpdateProcessor

@pytest.fixture
def mock_hass():
    """Mock HomeAssistant."""
    return MagicMock()

@pytest.fixture
def mock_config_entry():
    """Mock ConfigEntry."""
    return MagicMock()

@pytest.fixture
def mock_polling_manager():
    """Mock PollingManager."""
    manager = MagicMock()
    manager.record_success.return_value = False
    manager.update_interval = "30s"
    manager.get_success_rate.return_value = 100.0
    return manager

@pytest.fixture
def mock_config():
    """Mock CoordinatorConfig."""
    config = MagicMock()
    config.ignored_networks = []
    return config

@pytest.fixture
def update_processor(mock_hass, mock_config_entry, mock_polling_manager, mock_config):
    """Fixture for UpdateProcessor."""
    processor = UpdateProcessor(mock_hass, mock_config_entry, mock_polling_manager, mock_config)
    # Mock data_processor
    processor.data_processor = AsyncMock()
    return processor

@pytest.mark.asyncio
async def test_process_success_orchestration(update_processor):
    """Test that process_success calls the expected private methods."""
    data = {"networks": [], "ssids": []}
    current_data = {"key": " value "}

    # Mock _process_data_result to be async
    with (
        patch.object(update_processor, "_ensure_registries") as mock_ensure,
        patch.object(update_processor, "_handle_interval_recovery", return_value=True) as mock_handle,
        patch.object(update_processor, "_sanitize_current_data") as mock_sanitize,
        patch.object(update_processor, "_process_data_result", new_callable=AsyncMock) as mock_process,
    ):
        mock_process.return_value = ({}, {}, {})

        result = await update_processor.process_success(data, current_data)

        mock_ensure.assert_called_once_with(data)
        mock_handle.assert_called_once()
        mock_sanitize.assert_called_once_with(current_data)
        mock_process.assert_awaited_once_with(data)

        assert result == ({}, {}, {}, True)

def test_ensure_registries(update_processor):
    """Test _ensure_registries calls external helpers."""
    data = {"networks": [{"id": "n1"}], "ssids": [{"id": "s1"}]}

    with (
        patch("custom_components.meraki_ha.core.coordinator_helpers.update_processor.async_ensure_network_devices_exist") as mock_net,
        patch("custom_components.meraki_ha.core.coordinator_helpers.update_processor.async_ensure_ssid_devices_exist") as mock_ssid,
    ):
        update_processor._ensure_registries(data)
        mock_net.assert_called_once()
        mock_ssid.assert_called_once_with(update_processor.hass, update_processor.config_entry, data["ssids"])

def test_handle_interval_recovery(update_processor, mock_polling_manager):
    """Test _handle_interval_recovery logic."""
    # Case 1: Recovery occurs
    mock_polling_manager.record_success.return_value = True
    assert update_processor._handle_interval_recovery() is True

    # Case 2: No recovery
    mock_polling_manager.record_success.return_value = False
    assert update_processor._handle_interval_recovery() is False

def test_sanitize_current_data(update_processor):
    """Test _sanitize_current_data strips strings."""
    current_data = {"key1": "  value1  ", "key2": 123, "key3": "value3"}
    update_processor._sanitize_current_data(current_data)
    assert current_data == {"key1": "value1", "key2": 123, "key3": "value3"}

@pytest.mark.asyncio
async def test_process_data_result(update_processor):
    """Test _process_data_result calls external helpers."""
    data = {"networks": []}

    # Setup mock return value for async_process
    update_processor.data_processor.async_process.return_value = {
        "devices_by_serial": {"d": 1},
        "networks_by_id": {"n": 2},
        "ssids_by_network_and_number": {"s": 3}
    }

    result = await update_processor._process_data_result(data)

    update_processor.data_processor.async_process.assert_awaited_once_with(data)
    assert result == ({"d": 1}, {"n": 2}, {"s": 3})
