"""Test SwitchFetchStrategy."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.core.fetch_strategies.switch import (
    SwitchFetchStrategy,
)
from custom_components.meraki_ha.core.models.device import MerakiDevice


@pytest.fixture
def mock_client():
    """Fixture for a mock Meraki API client."""
    client = MagicMock()
    # Mock run_with_semaphore to just return the coroutine/call
    client.run_with_semaphore.side_effect = lambda x: x
    return client


@pytest.fixture
def disabled_features():
    """Fixture for the disabled features set."""
    return set()


@pytest.fixture
def strategy(mock_client, disabled_features):
    """Fixture for the SwitchFetchStrategy."""
    return SwitchFetchStrategy(
        client=mock_client,
        _disabled_features=disabled_features,
    )


def test_build_device_tasks(strategy):
    """Test that build_device_tasks adds switch-specific tasks."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    tasks = {}

    strategy.build_device_tasks(mock_device, tasks, capabilities=["switch_ports"])

    assert f"ports_statuses_{mock_device.serial}" in tasks


def test_build_device_tasks_skips_if_in_detail_data(strategy):
    """Test that build_device_tasks skips tasks if already in detail_data."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    tasks = {}
    detail_data = {f"ports_statuses_{mock_device.serial}": [{"portId": "1"}]}

    strategy.build_device_tasks(
        mock_device, tasks, capabilities=["switch_ports"], detail_data=detail_data
    )

    assert f"ports_statuses_{mock_device.serial}" not in tasks


def test_process_device_details(strategy):
    """Test processing device details for switch ports statuses."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    key = f"ports_statuses_{mock_device.serial}"
    detail_data = {
        key: [{"portId": "1", "status": "Connected"}]
    }

    strategy.process_device_details(mock_device, detail_data, None)

    assert mock_device.ports_statuses == detail_data[key]


def test_process_device_details_fallback_to_prev(strategy):
    """Test processing device details falls back to previous data."""
    mock_device = MagicMock()
    mock_device.serial = "SERIAL1"
    detail_data = {}
    prev_device = MerakiDevice(
        serial="SERIAL1",
        ports_statuses=[{"portId": "1", "status": "Disconnected"}]
    )

    strategy.process_device_details(mock_device, detail_data, prev_device)

    assert mock_device.ports_statuses == prev_device.ports_statuses
