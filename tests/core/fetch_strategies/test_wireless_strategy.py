"""Test WirelessFetchStrategy."""

from unittest.mock import MagicMock, patch

import pytest

from custom_components.meraki_ha.core.fetch_strategies.wireless import (
    WirelessFetchStrategy,
)


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
    """Fixture for the WirelessFetchStrategy."""
    return WirelessFetchStrategy(
        client=mock_client,
        _disabled_features=disabled_features,
    )


def test_build_network_tasks(strategy, mock_client):
    """Test that build_network_tasks calls the correct client methods."""
    network_id = "net1"
    product_types = ["wireless"]
    tasks = {}
    mock_client.wireless.get_network_detail_tasks.return_value = {"task1": "coro1"}

    strategy.build_network_tasks(network_id, product_types, tasks)

    mock_client.wireless.get_network_detail_tasks.assert_called_once_with(
        network_id, product_types
    )
    assert "task1" in tasks


@patch("custom_components.meraki_ha.core.fetch_strategies.wireless.parse_wireless_data")
def test_process_network_data(mock_parse, strategy):
    """Test that process_network_data calls parse_wireless_data and updates results."""
    network_id = "net1"
    detail_data = {"clients": [{"id": "c1"}]}
    previous_data = {}
    processed_data = {}

    mock_parse.return_value = {
        "ssids": [{"name": "SSID1"}],
        "wireless_settings": {"setting1": "val1"},
        "rf_profiles": {"profile1": "data1"},
    }

    strategy.process_network_data(
        network_id, detail_data, previous_data, processed_data
    )

    assert processed_data["ssids"] == [{"name": "SSID1"}]
    assert processed_data["wireless_settings"] == {"setting1": "val1"}
    assert processed_data["rf_profiles"] == {"profile1": "data1"}
