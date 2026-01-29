"""Tests for the Meraki API client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import asyncio
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.errors import (
    MerakiInformationalError,
    MerakiTrafficAnalysisError,
)
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork
from tests.const import MOCK_DEVICE, MOCK_DEVICE_INIT, MOCK_NETWORK, MOCK_NETWORK_INIT


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
    client = MerakiAPIClient(hass=hass, api_key="test-key", org_id="test-org")
    # Mock the internal endpoint handlers to avoid real API calls and semaphore issues
    client.wireless = MagicMock()
    client.switch = MagicMock()
    client.camera = MagicMock()
    client.appliance = MagicMock()
    client.network = MagicMock()
    client.organization = MagicMock()
    client.devices = MagicMock()
    client.sensor = MagicMock()

    # Mock methods to return Coroutines/Awaitables as expected by _run_with_semaphore.
    client.wireless.get_network_ssids = AsyncMock(return_value=[])
    client.wireless.get_network_wireless_settings = AsyncMock(return_value={})
    client.wireless.get_network_wireless_rf_profiles = AsyncMock(return_value=[])

    client.switch.get_device_switch_ports_statuses = AsyncMock(return_value=[])

    client.camera.get_camera_video_settings = AsyncMock(return_value={})
    client.camera.get_camera_sense_settings = AsyncMock(return_value={})
    client.camera.get_device_camera_analytics_recent = AsyncMock(return_value=[])

    client.appliance.get_network_vlans = AsyncMock(return_value=[])
    client.appliance.get_l3_firewall_rules = AsyncMock(return_value=[])
    client.appliance.get_traffic_shaping = AsyncMock(return_value={})
    client.appliance.get_vpn_status = AsyncMock(return_value={})
    client.appliance.get_network_appliance_content_filtering = AsyncMock(
        return_value={}
    )
    client.appliance.get_network_appliance_settings = AsyncMock(return_value={})

    client.network.get_network_traffic = AsyncMock(return_value={})

    client.dashboard = MagicMock()
    return client


@pytest.mark.asyncio
async def test_get_all_data_orchestration(api_client):
    """Test that get_all_data correctly orchestrates helper methods."""
    # Arrange
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [MOCK_NETWORK_INIT],
        }
    )
    api_client.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={"devices": [MOCK_DEVICE], "battery_readings": None}
    )
    api_client.client_fetcher.async_fetch_network_clients = AsyncMock(return_value=[])
    api_client.client_fetcher.async_fetch_device_clients = AsyncMock(return_value={})
    api_client._build_detail_tasks = MagicMock(return_value={})

    # Act
    await api_client.get_all_data()

    # Assert
    api_client._async_fetch_initial_data.assert_awaited_once()
    api_client.device_fetcher.async_fetch_devices.assert_awaited_once()
    api_client.client_fetcher.async_fetch_network_clients.assert_awaited_once()
    api_client.client_fetcher.async_fetch_device_clients.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_data_handles_api_errors(api_client, caplog):
    """Test that get_all_data handles API errors gracefully."""
    # Arrange
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": Exception("Network error"),
        }
    )
    api_client.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={"devices": [], "battery_readings": None}
    )
    api_client.client_fetcher.async_fetch_network_clients = AsyncMock(
        side_effect=Exception("Client fetch error")
    )
    api_client.client_fetcher.async_fetch_device_clients = AsyncMock(
        side_effect=Exception("Device client fetch error")
    )

    # Act
    data = await api_client.get_all_data()

    # Assert
    assert data["networks"] == []
    assert data["devices"] == []
    assert "Could not fetch networks" in caplog.text


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
    api_client.client_fetcher.async_fetch_network_clients = AsyncMock(return_value=[])
    api_client.client_fetcher.async_fetch_device_clients = AsyncMock(return_value={})
    api_client.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={
            "devices": [MerakiDevice.from_dict(MOCK_DEVICE_INIT)],
            "battery_readings": None,
        }
    )

    async def coro():
        return MerakiTrafficAnalysisError("Traffic analysis is not enabled")

    # Use a consistent mock network ID from MOCK_NETWORK_INIT
    network_id = MOCK_NETWORK_INIT["id"]
    api_client._build_detail_tasks = MagicMock(
        return_value={f"traffic_{network_id}": coro()}
    )

    # Act
    data = await api_client.get_all_data()

    # Assert
    assert data["appliance_traffic"][network_id]["error"] == "disabled"
    assert (
        data["appliance_traffic"][network_id]["reason"]
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
    """Test that get_all_data populates switch ports statuses on the device object."""
    # Arrange
    mock_switch = MerakiDevice(serial="Q123", product_type="switch")
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [],
        }
    )
    api_client.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={"devices": [mock_switch], "battery_readings": None}
    )
    api_client.client_fetcher.async_fetch_network_clients = AsyncMock(return_value=[])
    api_client.client_fetcher.async_fetch_device_clients = AsyncMock(return_value={})

    # Simulate detailed switch ports response
    async def coro():
        return [{"portId": "1", "status": "Connected"}]

    api_client._build_detail_tasks = MagicMock(
        return_value={"ports_statuses_Q123": coro()}
    )

    # Act
    data = await api_client.get_all_data()

    # Assert
    # The ports statuses should be on the device object in the devices list
    device = next(d for d in data["devices"] if d.serial == "Q123")
    assert device.ports_statuses == [{"portId": "1", "status": "Connected"}]


@pytest.mark.asyncio
async def test_build_detail_tasks_for_switch_device(api_client):
    """Test that _build_detail_tasks creates the correct tasks for a switch device."""
    # Arrange
    switch_device = MerakiDevice.from_dict({"serial": "s123", "productType": "switch"})
    devices = [switch_device]
    networks = []

    # Mock endpoints and semaphore wrapper to avoid unawaited coroutine warnings
    api_client.switch = AsyncMock()
    api_client.switch.get_device_switch_ports_statuses.return_value = "mock_switch_coro"
    api_client._run_with_semaphore = AsyncMock(side_effect=lambda x: x)

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"ports_statuses_{switch_device.serial}" in tasks
    # Clean up coroutines to avoid warnings
    for task in tasks.values():
        await task
    api_client.switch.get_device_switch_ports_statuses.assert_called_once_with("s123")


@pytest.mark.asyncio
async def test_build_detail_tasks_for_camera_device(api_client):
    """Test that _build_detail_tasks creates the correct tasks for a camera device."""
    # Arrange
    camera_device = MerakiDevice.from_dict({"serial": "c123", "productType": "camera"})
    devices = [camera_device]
    networks = []

    # Mock dependencies to avoid unawaited coroutine warnings
    api_client.camera = AsyncMock()
    api_client._run_with_semaphore = AsyncMock()

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"video_settings_{camera_device.serial}" in tasks
    assert f"sense_settings_{camera_device.serial}" in tasks

    # Clean up coroutines to avoid warnings
    for task in tasks.values():
        await task

    api_client.camera.get_camera_video_settings.assert_called_once_with("c123")
    api_client.camera.get_camera_sense_settings.assert_called_once_with("c123")


@pytest.mark.asyncio
async def test_build_detail_tasks_for_appliance_device(api_client):
    """Test that _build_detail_tasks creates tasks for an appliance device."""
    # Arrange
    appliance_device = MerakiDevice.from_dict(
        {
            "serial": "a123",
            "productType": "appliance",
            "networkId": "N_123",
        }
    )
    network_with_appliance = MerakiNetwork.from_dict(
        {"id": "N_123", "productTypes": ["appliance"]}
    )
    devices = [appliance_device]
    networks = [network_with_appliance]

    # Mock _run_with_semaphore to return the input immediately (pass-through)
    async def side_effect(coro):
        return await coro

    api_client._run_with_semaphore = MagicMock(side_effect=side_effect)

    # Enable VPN management to ensure vpn_status task is created
    api_client._enable_vpn_management = True

    # Mock endpoint methods to return awaitable mock objects
    api_client.network.get_network_traffic = AsyncMock(return_value="task_traffic")
    api_client.appliance.get_network_vlans = AsyncMock(return_value="task_vlans")
    api_client.appliance.get_l3_firewall_rules = AsyncMock(return_value="task_firewall")
    api_client.appliance.get_traffic_shaping = AsyncMock(return_value="task_shaping")
    api_client.appliance.get_vpn_status = AsyncMock(return_value="task_vpn")
    api_client.appliance.get_network_appliance_content_filtering = AsyncMock(
        return_value="task_filtering"
    )
    api_client.appliance.get_network_appliance_settings = AsyncMock(
        return_value="task_settings"
    )

    # Act
    # Patch create_task to simply return the coroutine so we can inspect the result
    with patch("asyncio.create_task", side_effect=lambda x: x):
        tasks = api_client._build_detail_tasks(networks, devices)

    # Await all tasks to ensure coroutines are executed and prevent warnings
    results = {k: await v for k, v in tasks.items()}

    # Assert
    # Verify values
    assert results[f"traffic_{network_with_appliance.id}"] == "task_traffic"
    assert results[f"vlans_{network_with_appliance.id}"] == "task_vlans"
    assert results[f"l3_firewall_rules_{network_with_appliance.id}"] == "task_firewall"
    assert results[f"traffic_shaping_{network_with_appliance.id}"] == "task_shaping"
    assert results[f"vpn_status_{network_with_appliance.id}"] == "task_vpn"
    assert (
        results[f"content_filtering_{network_with_appliance.id}"] == "task_filtering"
    )

    # Check device tasks
    assert results[f"appliance_settings_{appliance_device.serial}"] == "task_settings"


def test_process_detailed_data_merges_device_info(api_client):
    """Test that _process_detailed_data merges details into device objects."""
    # Arrange
    device = MerakiDevice(serial="c123", product_type="camera")
    video_settings = {"rtsp_url": "rtsp://test", "rtspServerEnabled": True}
    detail_data = {f"video_settings_{device.serial}": video_settings}

    # Act
    api_client._process_detailed_data(detail_data, [], [device], previous_data={})

    # Assert
    assert device.video_settings == video_settings
    assert device.rtsp_url == "rtsp://test"


@pytest.mark.asyncio
async def test_get_network_events_filters_none(api_client):
    """Test that get_network_events filters out None values from arguments."""
    # Arrange
    api_client.dashboard.networks.getNetworkEvents.return_value = {"events": []}
    network_id = "N_123"

    # Act
    await api_client.get_network_events(network_id)

    # Assert
    api_client.dashboard.networks.getNetworkEvents.assert_called_once()
    args, kwargs = api_client.dashboard.networks.getNetworkEvents.call_args
    assert network_id in args
    # Ensure no None values in kwargs
    for key, value in kwargs.items():
        assert value is not None, f"Found None value for key: {key}"
    # Specifically check that productType is not in kwargs (since it defaults to None)
    assert "productType" not in kwargs


@pytest.mark.asyncio
async def test_get_network_events_passes_values(api_client):
    """Test that get_network_events passes non-None values correctly."""
    # Arrange
    api_client.dashboard.networks.getNetworkEvents.return_value = {"events": []}
    network_id = "N_123"
    product_type = "appliance"

    # Act
    await api_client.get_network_events(network_id, product_type=product_type)

    # Assert
    api_client.dashboard.networks.getNetworkEvents.assert_called_once()
    args, kwargs = api_client.dashboard.networks.getNetworkEvents.call_args
    assert kwargs.get("productType") == product_type
