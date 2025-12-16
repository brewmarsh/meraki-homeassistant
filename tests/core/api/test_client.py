"""Tests for the Meraki API client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator
from tests.const import MOCK_DEVICE, MOCK_NETWORK


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
    mock = MagicMock(spec=MerakiDataCoordinator)
    mock.is_vlan_check_due.return_value = True
    mock.is_traffic_check_due.return_value = True
    return mock


@pytest.fixture
def api_client(hass, mock_dashboard, coordinator):
    """Fixture for a MerakiAPIClient instance."""
    client = MerakiAPIClient(api_key="test-key", org_id="test-org")
    # Mock the internal endpoint handlers to avoid real API calls and semaphore issues
    # during unit testing of _build_detail_tasks and logic flow.
    # We use MagicMock for the classes, but we need instances.
    # The client initializes them in __init__. We replace them here.
    client.wireless = MagicMock()
    client.switch = MagicMock()
    client.camera = MagicMock()
    client.appliance = MagicMock()
    client.network = MagicMock()
    client.devices = MagicMock()
    client.organization = MagicMock()
    client.sensor = MagicMock()

    # Mock methods to return Coroutines/Awaitables as expected by _run_with_semaphore.
    client.wireless.get_network_ssids = AsyncMock(return_value=[])
    client.wireless.get_network_wireless_settings = AsyncMock(return_value={})
    client.wireless.get_network_wireless_rf_profiles = AsyncMock(return_value=[])

    client.switch.get_device_switch_ports_statuses = AsyncMock(return_value=[])

    client.camera.get_camera_video_settings = AsyncMock(return_value={})
    client.camera.get_camera_sense_settings = AsyncMock(return_value={})

    client.appliance.get_network_vlans = AsyncMock(return_value=[])
    client.appliance.get_l3_firewall_rules = AsyncMock(return_value=[])
    client.appliance.get_traffic_shaping = AsyncMock(return_value={})
    client.appliance.get_vpn_status = AsyncMock(return_value={})
    client.appliance.get_network_appliance_content_filtering = AsyncMock(
        return_value={}
    )
    client.appliance.get_network_appliance_settings = AsyncMock(return_value={})

    client.network.get_network_traffic = AsyncMock(return_value={})

    client._dashboard = MagicMock()
    return client


@pytest.mark.asyncio
async def test_get_all_data_orchestration(api_client):
    """Test that get_all_data correctly orchestrates helper methods."""
    # Arrange
    api_client._async_fetch_initial_data = AsyncMock(return_value=())
    api_client._process_initial_data = MagicMock(
        return_value={
            "networks": [MOCK_NETWORK],
            "devices": [MOCK_DEVICE],
            "appliance_uplink_statuses": [],
        }
    )
    api_client._async_fetch_network_clients = AsyncMock(return_value=[])
    api_client._async_fetch_device_clients = AsyncMock(return_value={})
    api_client._build_detail_tasks = MagicMock(return_value={})
    api_client._process_detailed_data = MagicMock(return_value={})

    # Act
    await api_client.get_all_data()

    # Assert
    api_client._async_fetch_initial_data.assert_awaited_once()
    api_client._process_initial_data.assert_called_once()
    api_client._async_fetch_network_clients.assert_awaited_once_with([MOCK_NETWORK])
    api_client._async_fetch_device_clients.assert_awaited_once_with([MOCK_DEVICE])
    api_client._build_detail_tasks.assert_called_once_with(
        [MOCK_NETWORK], [MOCK_DEVICE]
    )
    api_client._process_detailed_data.assert_called_once()


def test_process_initial_data_merges_availability(api_client):
    """Test that _process_initial_data merges device availability."""
    # Arrange
    device_with_status = MOCK_DEVICE.copy()
    availabilities = [{"serial": MOCK_DEVICE["serial"], "status": "online"}]
    results = {
        "networks": [MOCK_NETWORK],
        "devices": [device_with_status],
        "devices_availabilities": availabilities,
        "appliance_uplink_statuses": [],
    }

    # Act
    data = api_client._process_initial_data(results)

    # Assert
    assert data["devices"][0]["status"] == "online"


def test_process_initial_data_handles_errors(api_client, caplog):
    """Test that _process_initial_data handles API errors gracefully."""
    # Arrange
    results = {
        "networks": Exception("Network error"),
        "devices": Exception("Device error"),
        "devices_availabilities": [],
        "appliance_uplink_statuses": [],
    }

    # Act
    data = api_client._process_initial_data(results)

    # Assert
    assert data["networks"] == []
    assert data["devices"] == []
    assert "Could not fetch Meraki networks" in caplog.text
    assert "Could not fetch Meraki devices" in caplog.text


def test_build_detail_tasks_for_wireless_device(api_client):
    """Test that _build_detail_tasks creates the correct tasks for a wireless device."""
    # Arrange
    devices = [MOCK_DEVICE]
    networks = [MOCK_NETWORK]

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"ssids_{MOCK_NETWORK['id']}" in tasks
    # assert f"wireless_settings_{MOCK_NETWORK['id']}" in tasks
    # assert f"rf_profiles_{MOCK_NETWORK['id']}" in tasks


def test_build_detail_tasks_for_switch_device(api_client):
    """Test that _build_detail_tasks creates the correct tasks for a switch device."""
    # Arrange
    switch_device = {"serial": "s123", "productType": "switch"}
    devices = [switch_device]
    networks = []

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"ports_statuses_{switch_device['serial']}" in tasks


def test_build_detail_tasks_for_camera_device(api_client):
    """Test that _build_detail_tasks creates the correct tasks for a camera device."""
    # Arrange
    camera_device = {"serial": "c123", "productType": "camera"}
    devices = [camera_device]
    networks = []

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"video_settings_{camera_device['serial']}" in tasks
    assert f"sense_settings_{camera_device['serial']}" in tasks


def test_build_detail_tasks_for_appliance_device(api_client):
    """Test that _build_detail_tasks creates tasks for an appliance device."""
    # Arrange
    appliance_device = {
        "serial": "a123",
        "productType": "appliance",
        "networkId": "N_123",
    }
    network_with_appliance = {"id": "N_123", "productTypes": ["appliance"]}
    devices = [appliance_device]
    networks = [network_with_appliance]

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"appliance_settings_{appliance_device['serial']}" in tasks
    assert f"traffic_{network_with_appliance['id']}" in tasks
    assert f"vlans_{network_with_appliance['id']}" in tasks


def test_process_detailed_data_merges_device_info(api_client):
    """Test that _process_detailed_data merges details into device objects."""
    # Arrange
    device = {"serial": "c123", "productType": "camera"}
    video_settings = {"rtsp_url": "rtsp://test"}
    detail_data = {f"video_settings_{device['serial']}": video_settings}

    # Act
    api_client._process_detailed_data(detail_data, [], [device], previous_data={})

    # Assert
    assert "video_settings" in device
    assert device["video_settings"] == video_settings
    assert device["rtsp_url"] == "rtsp://test"


@pytest.mark.asyncio
async def test_get_network_events_filters_none(api_client):
    """Test that get_network_events filters out None values from arguments."""
    # Arrange
    api_client._dashboard.networks.getNetworkEvents.return_value = {"events": []}
    network_id = "N_123"

    # Act
    await api_client.get_network_events(network_id)

    # Assert
    api_client._dashboard.networks.getNetworkEvents.assert_called_once()
    args, kwargs = api_client._dashboard.networks.getNetworkEvents.call_args
    assert kwargs.get("networkId") == network_id
    # Ensure no None values in kwargs
    for key, value in kwargs.items():
        assert value is not None, f"Found None value for key: {key}"
    # Specifically check that productType is not in kwargs (since it defaults to None)
    assert "productType" not in kwargs


@pytest.mark.asyncio
async def test_get_network_events_passes_values(api_client):
    """Test that get_network_events passes non-None values correctly."""
    # Arrange
    api_client._dashboard.networks.getNetworkEvents.return_value = {"events": []}
    network_id = "N_123"
    product_type = "appliance"

    # Act
    await api_client.get_network_events(network_id, productType=product_type)

    # Assert
    api_client._dashboard.networks.getNetworkEvents.assert_called_once()
    args, kwargs = api_client._dashboard.networks.getNetworkEvents.call_args
    assert kwargs.get("productType") == product_type
