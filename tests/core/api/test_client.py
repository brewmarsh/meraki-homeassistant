"""Tests for the Meraki API client."""

from unittest.mock import AsyncMock, MagicMock, patch
from dataclasses import asdict
import pytest

from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.errors import MerakiInformationalError
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork
from tests.const import MOCK_DEVICE, MOCK_NETWORK, MOCK_DEVICE_INIT, MOCK_NETWORK_INIT


@pytest.fixture
def mock_dashboard():
    """Fixture for a mocked meraki.DashboardAPI."""
    with patch("meraki.DashboardAPI") as mock_dashboard_api:
        yield mock_dashboard_api


@pytest.fixture
def hass():
    """Fixture for a mocked Home Assistant instance."""
    return MagicMock()


@pytest.fixture
def coordinator():
    """Fixture for a mocked coordinator."""
    mock = MagicMock(spec=MerakiDataUpdateCoordinator)
    mock.is_vlan_check_due.return_value = True
    mock.is_traffic_check_due.return_value = True
    return mock


@pytest.fixture
def api_client(hass, mock_dashboard, coordinator):
    """Fixture for a MerakiAPIClient instance."""
    return MerakiAPIClient(
        hass=hass, api_key="test-key", org_id="test-org", coordinator=coordinator
    )


@pytest.mark.asyncio
async def test_get_all_data_orchestration(api_client):
    """Test that get_all_data correctly orchestrates helper methods."""
    # Arrange
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [MOCK_NETWORK_INIT],
            "devices": [MOCK_DEVICE_INIT],
        }
    )
    api_client._async_fetch_network_clients = AsyncMock(return_value=[])
    api_client._async_fetch_device_clients = AsyncMock(return_value={})
    api_client._build_detail_tasks = MagicMock(return_value={})

    # Act
    await api_client.get_all_data()

    # Assert
    api_client._async_fetch_initial_data.assert_awaited_once()

    assert api_client._async_fetch_network_clients.await_args[0][0][0].id == MOCK_NETWORK.id
    assert api_client._async_fetch_device_clients.await_args[0][0][0].serial == MOCK_DEVICE.serial
    api_client._build_detail_tasks.assert_called_once()
    assert api_client._build_detail_tasks.call_args[0][0][0].id == MOCK_NETWORK.id
    assert api_client._build_detail_tasks.call_args[0][1][0].serial == MOCK_DEVICE.serial


@pytest.mark.asyncio
async def test_get_all_data_handles_api_errors(api_client, caplog):
    """Test that get_all_data handles API errors gracefully."""
    # Arrange
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": Exception("Network error"),
            "devices": Exception("Device error"),
            "device_statuses": Exception("Device status error"),
        }
    )

    # Act
    data = await api_client.get_all_data()

    # Assert
    assert data["networks"] == []
    assert data["devices"] == []
    assert "Could not fetch networks" in caplog.text
    assert "Could not fetch devices" in caplog.text
    assert "Could not fetch device statuses" in caplog.text


@pytest.mark.asyncio
async def test_get_all_data_merges_availability(api_client):
    """Test that get_all_data merges device availability."""
    # Arrange
    availabilities = [{"serial": MOCK_DEVICE.serial, "status": "online"}]
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [MOCK_NETWORK_INIT],
            "devices": [MOCK_DEVICE_INIT],
            "devices_availabilities": availabilities,
        }
    )
    api_client._async_fetch_network_clients = AsyncMock(return_value=[])
    api_client._async_fetch_device_clients = AsyncMock(return_value={})
    api_client._build_detail_tasks = MagicMock(return_value={})

    # Act
    data = await api_client.get_all_data()

    # Assert
    assert data["devices"][0].status == "online"


@pytest.mark.asyncio
async def test_get_all_data_handles_informational_errors(api_client):
    """Test that get_all_data handles informational API errors."""
    # Arrange
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [MOCK_NETWORK_INIT],
            "devices": [MOCK_DEVICE_INIT],
            "device_statuses": [],
        }
    )
    api_client._async_fetch_network_clients = AsyncMock(return_value=[])
    api_client._async_fetch_device_clients = AsyncMock(return_value={})

    async def coro():
        return MerakiInformationalError("Traffic analysis is not enabled")

    api_client._build_detail_tasks = MagicMock(
        return_value={f"traffic_{MOCK_NETWORK.id}": coro()}
    )

    # Act
    data = await api_client.get_all_data()

    # Assert
    assert data["appliance_traffic"][MOCK_NETWORK.id]["error"] == "disabled"
    assert (
        data["appliance_traffic"][MOCK_NETWORK.id]["reason"]
        == "Traffic analysis is not enabled"
    )


@pytest.mark.asyncio
async def test_build_detail_tasks_for_wireless_device(api_client):
    """Test that _build_detail_tasks creates the correct tasks for a wireless device."""
    # Arrange
    devices = [MOCK_DEVICE]
    networks = [MOCK_NETWORK]

    # Mock _run_with_semaphore to return the task directly so we can close it
    async def side_effect(coro):
        return await coro

    api_client._run_with_semaphore = MagicMock(side_effect=side_effect)

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"ssids_{MOCK_NETWORK.id}" in tasks
    assert f"rf_profiles_{MOCK_NETWORK.id}" in tasks

    # Clean up coroutines to avoid warnings
    for task in tasks.values():
        await task


@pytest.mark.asyncio
async def test_get_all_data_includes_switch_ports(api_client):
    """Test that get_all_data returns switch ports statuses."""
    # Arrange
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [],
            "devices": [],
        }
    )
    api_client._async_fetch_network_clients = AsyncMock(return_value=[])
    api_client._async_fetch_device_clients = AsyncMock(return_value={})

    # Simulate detailed switch ports response
    async def coro():
        return [{"portId": "1", "status": "Connected"}]

    api_client._build_detail_tasks = MagicMock(
        return_value={"ports_statuses_Q123": coro()}
    )

    # Act
    data = await api_client.get_all_data()

    # Assert
    assert "switch_ports_statuses" in data
    assert data["switch_ports_statuses"]["Q123"] == [
        {"portId": "1", "status": "Connected"}
    ]


@pytest.mark.asyncio
async def test_build_detail_tasks_for_switch_device(api_client):
    """Test that _build_detail_tasks creates the correct tasks for a switch device."""
    # Arrange
    switch_device = MerakiDevice.from_dict({"serial": "s123", "productType": "switch"})
    devices = [switch_device]
    networks = []

    # Mock _run_with_semaphore to return the task directly so we can close it
    async def side_effect(coro):
        return await coro

    api_client._run_with_semaphore = MagicMock(side_effect=side_effect)

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"ports_statuses_{switch_device.serial}" in tasks

    # Clean up coroutines to avoid warnings
    for task in tasks.values():
        await task


@pytest.mark.asyncio
async def test_build_detail_tasks_for_camera_device(api_client):
    """Test that _build_detail_tasks creates the correct tasks for a camera device."""
    # Arrange
    camera_device = MerakiDevice.from_dict({"serial": "c123", "productType": "camera"})
    devices = [camera_device]
    networks = []

    # Mock _run_with_semaphore to return the task directly so we can close it
    async def side_effect(coro):
        return await coro

    api_client._run_with_semaphore = MagicMock(side_effect=side_effect)

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"video_settings_{camera_device.serial}" in tasks
    assert f"sense_settings_{camera_device.serial}" in tasks

    # Clean up coroutines to avoid warnings
    for task in tasks.values():
        await task


@pytest.mark.asyncio
async def test_build_detail_tasks_for_appliance_device(api_client):
    """Test that _build_detail_tasks creates tasks for an appliance device."""
    # Arrange
    appliance_device = MerakiDevice.from_dict({
        "serial": "a123",
        "productType": "appliance",
        "networkId": "N_123",
    })
    network_with_appliance = MerakiNetwork.from_dict({"id": "N_123", "productTypes": ["appliance"]})
    devices = [appliance_device]
    networks = [network_with_appliance]

    # Mock _run_with_semaphore to return the task directly so we can close it
    async def side_effect(coro):
        return await coro

    api_client._run_with_semaphore = MagicMock(side_effect=side_effect)

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"appliance_settings_{appliance_device.serial}" in tasks
    assert f"traffic_{network_with_appliance.id}" in tasks
    assert f"vlans_{network_with_appliance.id}" in tasks

    # Clean up coroutines to avoid warnings
    for task in tasks.values():
        await task
