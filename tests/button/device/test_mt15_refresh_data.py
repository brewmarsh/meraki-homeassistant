"""Tests for the Meraki MT15 refresh data button."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.button.device.mt15_refresh_data import (
    MerakiMt15RefreshDataButton,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.last_update_success = True
    coordinator.data = {
        "devices": [
            {
                "serial": "mt15-1",
                "name": "MT15 Sensor",
                "model": "MT15",
                "productType": "sensor",
            },
        ]
    }
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.data = {
        "api_key": "test_key",
        "org_id": "test_org",
    }
    entry.options = {}
    return entry


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.sensor.create_device_sensor_command = AsyncMock()
    return client


def test_mt15_button_creation(mock_coordinator, mock_config_entry, mock_meraki_client):
    """Test the creation of the MT15 refresh data button."""
    device_info = mock_coordinator.data["devices"][0]
    button = MerakiMt15RefreshDataButton(
        mock_coordinator, device_info, mock_config_entry, mock_meraki_client
    )

    assert button.unique_id == "mt15-1-refresh"
    assert button.name == "MT15 Sensor Refresh Data"
    assert button.available is True


@pytest.mark.asyncio
async def test_mt15_button_press(
    mock_coordinator, mock_config_entry, mock_meraki_client
):
    """Test pressing the MT15 refresh data button."""
    device_info = mock_coordinator.data["devices"][0]
    button = MerakiMt15RefreshDataButton(
        mock_coordinator, device_info, mock_config_entry, mock_meraki_client
    )

    await button.async_press()

    mock_meraki_client.sensor.create_device_sensor_command.assert_called_once_with(
        serial="mt15-1",
        operation="refreshData",
    )
