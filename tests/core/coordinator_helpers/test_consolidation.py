"""Tests for the Data Consolidation logic."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)


@pytest.fixture
def mock_client():
    """Mock the Meraki API client."""
    client = MagicMock()
    client._disabled_features = set()
    client.has_dashboard = True

    # Mock run_with_semaphore to return an awaitable that returns its input
    # if it was a coro or just returns a mock result.
    async def mock_run(coro_or_val):
        if hasattr(coro_or_val, "__await__"):
            return await coro_or_val
        return coro_or_val

    client.run_with_semaphore = AsyncMock(side_effect=mock_run)
    return client


@pytest.fixture
def data_fetch_manager(mock_client):
    """Fixture for DataFetchManager."""
    return DataFetchManager(mock_client)


@pytest.mark.asyncio
async def test_consolidation_switch_ports(data_fetch_manager, mock_client):
    """Test that switch ports are batch loaded and per-device calls are skipped."""
    # 1. Setup mock data
    switch_serial = "Q123"
    switch_ports = [{"portId": "1", "status": "Connected"}]

    # Mock initial data to include switch ports statuses
    mock_initial = {
        "organization": {"name": "Test Org"},
        "networks": [],
        "devices": [{"serial": switch_serial, "productType": "switch"}],
        "appliance_uplink_statuses": [],
        "sensor_readings": [],
        "switch_ports_statuses": [{"serial": switch_serial, "ports": switch_ports}],
    }
    data_fetch_manager._async_fetch_initial_data = AsyncMock(return_value=mock_initial)
    data_fetch_manager.client_fetcher.async_fetch_network_clients = AsyncMock(
        return_value=[]
    )

    # Spy on strategy.build_device_tasks
    strategy_spy = MagicMock(
        wraps=data_fetch_manager.switch_strategy.build_device_tasks
    )
    data_fetch_manager.switch_strategy.build_device_tasks = strategy_spy

    # 2. Execute get_all_data
    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_network_data",
        return_value={"appliance_traffic": {}, "vlans": {}},
    ):
        result = await data_fetch_manager.get_all_data()

    # 3. Assertions
    # Ensure build_device_tasks was called with the batch data
    strategy_spy.assert_called()
    call_args = strategy_spy.call_args
    # detail_data (4th arg) should contain unpacked statuses
    assert f"ports_statuses_{switch_serial}" in call_args[0][3]

    # Ensure the device has the ports statuses
    assert result["devices"][0].ports_statuses == switch_ports


@pytest.mark.asyncio
async def test_consolidation_clients(data_fetch_manager, mock_client):
    """Test that device clients are derived from network clients."""
    # 1. Setup mock data
    device_serial = "Q789"
    mock_clients = [
        {"mac": "AA:BB:CC:DD:EE:FF", "recentDeviceSerial": device_serial},
        {"mac": "11:22:33:44:55:66", "recentDeviceSerial": "OTHER_SERIAL"},
    ]

    mock_initial = {
        "organization": {"name": "Test Org"},
        "networks": [{"id": "N123", "name": "Net 1"}],
        "devices": [{"serial": device_serial, "productType": "wireless"}],
        "appliance_uplink_statuses": [],
        "sensor_readings": [],
        "switch_ports_statuses": [],
    }
    data_fetch_manager._async_fetch_initial_data = AsyncMock(return_value=mock_initial)

    # Mock network client fetch
    data_fetch_manager.client_fetcher.async_fetch_network_clients = AsyncMock(
        return_value=mock_clients
    )

    # Spy on derive_device_clients
    derive_spy = MagicMock(
        wraps=data_fetch_manager.client_fetcher.derive_device_clients
    )
    data_fetch_manager.client_fetcher.derive_device_clients = derive_spy

    # 2. Execute
    with patch(
        "custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_network_data",
        return_value={"appliance_traffic": {}, "vlans": {}},
    ):
        result = await data_fetch_manager.get_all_data()

    # 3. Assertions
    derive_spy.assert_called_once_with(mock_clients, result["devices"])
    assert result["clients_by_serial"][device_serial] == [mock_clients[0]]
    # OTHER_SERIAL should NOT be in the result because it's not in devices_list
    assert "OTHER_SERIAL" not in result["clients_by_serial"]
