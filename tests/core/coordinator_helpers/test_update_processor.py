"""Tests for the UpdateProcessor."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest
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
    # Mock the internal data_processor to isolate UpdateProcessor logic
    processor.data_processor = AsyncMock()
    return processor

@pytest.mark.asyncio
async def test_process_success_orchestration(update_processor):
    """Test that process_success calls the expected methods and returns the correct tuple."""
    data = {"networks": [], "ssids": []}
    current_data = {"key": " value "}

    processed_return = {
        "devices_by_serial": {"d": 1},
        "networks_by_id": {"n": 2},
        "ssids_by_network_and_number": {"s": 3}
    }

    # Setup the mock DataProcessor to return our sample data
    update_processor.data_processor.async_process = AsyncMock(return_value=processed_return)

    with patch.object(update_processor, "_handle_interval_recovery", return_value=True) as mock_handle:
        result = await update_processor.process_success(data, current_data)

        # Verify orchestrator called its recovery helper
        mock_handle.assert_called_once()
        
        # Verify orchestration delegated to DataProcessor correctly
        update_processor.data_processor.async_process.assert_awaited_once_with(data, current_data)

        # Verify the final unpacked result matches expectations
        assert result == ({"d": 1}, {"n": 2}, {"s": 3}, True)

def test_handle_interval_recovery(update_processor, mock_polling_manager):
    """Test _handle_interval_recovery logic based on PollingManager feedback."""
    # Case 1: Recovery occurs (PollingManager signals a state change)
    mock_polling_manager.record_success.return_value = True
    assert update_processor._handle_interval_recovery() is True

    # Case 2: No recovery (State remains stable)
    mock_polling_manager.record_success.return_value = False
    assert update_processor._handle_interval_recovery() is False