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
    client = MerakiAPIClient(hass=hass, api_key="test-key", org_id="test-org")
    # Mock endpoint classes to prevent real API calls or errors
    client.appliance = MagicMock()
    client.camera = MagicMock()
    client.devices = MagicMock()
    client.network = MagicMock()
    client.organization = MagicMock()
    client.switch = MagicMock()
    client.wireless = MagicMock()
    client.sensor = MagicMock()
    return client


@pytest.mark.asyncio
async def test_get_all_data_orchestration(api_client):
    """Test that get_all_data correctly orchestrates helper methods."""
    # Arrange
    api_client._async_fetch_initial_data = AsyncMock(return_value={
        "networks": [MOCK_NETWORK],
        "devices": [MOCK_DEVICE],
        "appliance_uplink_statuses": [],
    })
    api_client._process_initial_data = MagicMock(
        return_value={
            "networks": [MOCK_NETWORK],
            "devices": [MOCK_DEVICE],
            "appliance_uplink_statuses": [],
            "vpn_statuses_by_network": {},
            "rf_profiles_by_network": {},
            "switch_ports_by_serial": {},
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
    """
    Test that _build_detail_tasks creates the correct tasks for a wireless device.

    Updated: Wireless RF profiles are now bulk fetched, so should NOT be in tasks.
    Wireless Settings are fetched per network.
    SSIDs are fetched per network.
    """
    # Arrange
    devices = [MOCK_DEVICE]
    networks = [MOCK_NETWORK]

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"ssids_{MOCK_NETWORK['id']}" in tasks
    assert f"wireless_settings_{MOCK_NETWORK['id']}" in tasks
    # rf_profiles should NOT be here anymore as it is bulk fetched
    assert f"rf_profiles_{MOCK_NETWORK['id']}" not in tasks


def test_build_detail_tasks_for_switch_device(api_client):
    """
    Test that _build_detail_tasks creates the correct tasks for a switch device.

    Updated: Switch ports statuses are now bulk fetched, so should NOT be in tasks.
    """
    # Arrange
    switch_device = {"serial": "s123", "productType": "switch"}
    devices = [switch_device]
    networks = []

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    # ports_statuses should NOT be here anymore as it is bulk fetched
    assert f"ports_statuses_{switch_device['serial']}" not in tasks


def test_build_detail_tasks_for_camera_device(api_client):
    """Test that _build_detail_tasks creates the correct tasks for a camera device."""
    # Arrange
    camera_device = {"serial": "c123", "productType": "camera"}
    devices = [camera_device]
    networks = []

    # Mock coroutines to prevent unawaited warnings
    api_client.camera.get_camera_video_settings.return_value = AsyncMock()
    api_client.camera.get_camera_sense_settings.return_value = AsyncMock()
    api_client._run_with_semaphore = AsyncMock()

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"video_settings_{camera_device['serial']}" in tasks
    assert f"sense_settings_{camera_device['serial']}" in tasks


def test_build_detail_tasks_for_appliance_device(api_client):
    """
    Test that _build_detail_tasks creates tasks for an appliance device.

    Updated: VPN status is bulk fetched, so should not be in tasks.
    """
    # Arrange
    appliance_device = {
        "serial": "a123",
        "productType": "appliance",
        "networkId": "N_123",
    }
    network_with_appliance = {"id": "N_123", "productTypes": ["appliance"]}
    devices = [appliance_device]
    networks = [network_with_appliance]

    # Mock coroutines
    api_client.appliance.get_network_appliance_settings.return_value = AsyncMock()
    api_client.network.get_network_traffic.return_value = AsyncMock()
    api_client.appliance.get_network_vlans.return_value = AsyncMock()
    api_client.appliance.get_l3_firewall_rules.return_value = AsyncMock()
    api_client.appliance.get_traffic_shaping.return_value = AsyncMock()
    api_client.appliance.get_network_appliance_content_filtering.return_value = AsyncMock()
    api_client._run_with_semaphore = AsyncMock()

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"appliance_settings_{appliance_device['serial']}" in tasks
    assert f"traffic_{network_with_appliance['id']}" in tasks
    assert f"vlans_{network_with_appliance['id']}" in tasks
    # vpn_status should NOT be here anymore
    assert f"vpn_status_{network_with_appliance['id']}" not in tasks


def test_process_detailed_data_merges_bulk_data(api_client):
    """Test that _process_detailed_data merges bulk data."""
    # Arrange
    device = MOCK_DEVICE.copy()
    device["serial"] = "S_123"
    device["productType"] = "switch"

    switch_ports = [{"portId": "1", "status": "Connected"}]

    bulk_data = {
        "switch_ports_by_serial": {
            "S_123": switch_ports
        },
        "vpn_statuses_by_network": {
            "N_123": {"status": "enabled"}
        },
        "rf_profiles_by_network": {
            "N_123": [{"name": "Profile1"}]
        }
    }

    networks = [{"id": "N_123"}]
    devices = [device]

    # Act
    result = api_client._process_detailed_data({}, networks, devices, {}, bulk_data)

    # Assert
    assert device["ports_statuses"] == switch_ports
    assert result["vpn_status"]["N_123"] == {"status": "enabled"}
    assert result["rf_profiles"]["N_123"] == [{"name": "Profile1"}]
