"""Tests for the Meraki MT15 refresh data button."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.button.device.mt15_refresh_data import (
    MerakiMt15RefreshDataButton,
)


@pytest.fixture
def mock_coordinator_mt15(mock_coordinator: MagicMock) -> MagicMock:
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataUpdateCoordinator with MT15 data."""
=======
    """Fixture for a mocked MerakiDataCoordinator with MT15 data."""
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
    mock_coordinator.data = {
        "devices": [
            {
                "serial": "mt15-1",
                "name": "MT15 Sensor",
                "model": "MT15",
                "productType": "sensor",
            },
        ]
    }
    mock_coordinator.last_update_success = True
    return mock_coordinator


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.sensor.create_device_sensor_command = AsyncMock()
    return client


def test_mt15_button_creation(
    mock_coordinator_mt15: MagicMock,
    mock_config_entry: MagicMock,
    mock_meraki_client: MagicMock,
):
    """Test the creation of the MT15 refresh data button."""
    device_info = mock_coordinator_mt15.data["devices"][0]
    button = MerakiMt15RefreshDataButton(
        mock_coordinator_mt15, device_info, mock_config_entry, mock_meraki_client
    )

    assert button.unique_id == "mt15-1-refresh"
    assert button.name == "MT15 Sensor Refresh Data"
    assert button.available is True


@pytest.mark.asyncio
async def test_mt15_button_press(
    mock_coordinator_mt15: MagicMock,
    mock_config_entry: MagicMock,
    mock_meraki_client: MagicMock,
):
    """Test pressing the MT15 refresh data button."""
    device_info = mock_coordinator_mt15.data["devices"][0]
    button = MerakiMt15RefreshDataButton(
        mock_coordinator_mt15, device_info, mock_config_entry, mock_meraki_client
    )

    await button.async_press()

    mock_meraki_client.sensor.create_device_sensor_command.assert_called_once_with(
        serial="mt15-1",
        operation="refreshData",
    )
