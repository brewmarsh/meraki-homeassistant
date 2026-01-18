"""Tests for the Meraki API client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

<<<<<<< HEAD
from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator
=======
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.errors import MerakiInformationalError
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork
>>>>>>> origin/beta
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
<<<<<<< HEAD
    mock = MagicMock(spec=MerakiDataCoordinator)
=======
    mock = MagicMock(spec=MerakiDataUpdateCoordinator)
>>>>>>> origin/beta
    mock.is_vlan_check_due.return_value = True
    mock.is_traffic_check_due.return_value = True
    return mock


@pytest.fixture
def api_client(hass, mock_dashboard, coordinator):
    """Fixture for a MerakiAPIClient instance."""
<<<<<<< HEAD
    return MerakiAPIClient(hass=hass, api_key="test-key", org_id="test-org")
=======
    return MerakiAPIClient(
        hass=hass, api_key="test-key", org_id="test-org", coordinator=coordinator
    )
>>>>>>> origin/beta


@pytest.mark.asyncio
async def test_get_all_data_orchestration(api_client):
    """Test that get_all_data correctly orchestrates helper methods."""
    # Arrange
<<<<<<< HEAD
    api_client._async_fetch_initial_data = AsyncMock(return_value=())
    api_client._process_initial_data = MagicMock(
        return_value={
            "networks": [MOCK_NETWORK],
            "devices": [MOCK_DEVICE],
            "appliance_uplink_statuses": [],
=======
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [MOCK_NETWORK],
            "devices": [MOCK_DEVICE],
>>>>>>> origin/beta
        }
    )
    api_client._async_fetch_network_clients = AsyncMock(return_value=[])
    api_client._async_fetch_device_clients = AsyncMock(return_value={})
    api_client._build_detail_tasks = MagicMock(return_value={})
<<<<<<< HEAD
    api_client._process_detailed_data = MagicMock(return_value={})
=======
>>>>>>> origin/beta

    # Act
    await api_client.get_all_data()

    # Assert
    api_client._async_fetch_initial_data.assert_awaited_once()
<<<<<<< HEAD
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
=======
    mock_network = MerakiNetwork(**MOCK_NETWORK)
    mock_device = MerakiDevice(**MOCK_DEVICE)

    api_client._async_fetch_network_clients.assert_awaited_once_with([mock_network])
    api_client._async_fetch_device_clients.assert_awaited_once_with([mock_device])
    api_client._build_detail_tasks.assert_called_once_with(
        [mock_network], [mock_device]
    )


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
>>>>>>> origin/beta

    # Assert
    assert data["networks"] == []
    assert data["devices"] == []
<<<<<<< HEAD
    assert "Could not fetch Meraki networks" in caplog.text
    assert "Could not fetch Meraki devices" in caplog.text
=======
    assert "Could not fetch networks" in caplog.text
    assert "Could not fetch devices" in caplog.text
    assert "Could not fetch device statuses" in caplog.text


@pytest.mark.asyncio
async def test_get_all_data_merges_availability(api_client):
    """Test that get_all_data merges device availability."""
    # Arrange
    device_with_status = MOCK_DEVICE.copy()
    availabilities = [{"serial": MOCK_DEVICE["serial"], "status": "online"}]
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [MOCK_NETWORK],
            "devices": [device_with_status],
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
            "networks": [MOCK_NETWORK],
            "devices": [MOCK_DEVICE],
            "device_statuses": [],
        }
    )
    api_client._async_fetch_network_clients = AsyncMock(return_value=[])
    api_client._async_fetch_device_clients = AsyncMock(return_value={})
    async def coro():
        return MerakiInformationalError("Traffic analysis is not enabled")

    api_client._build_detail_tasks = MagicMock(
        return_value={f"traffic_{MOCK_NETWORK['id']}": coro()}
    )

    # Act
    data = await api_client.get_all_data()

    # Assert
    assert data["appliance_traffic"][MOCK_NETWORK["id"]]["error"] == "disabled"
    assert (
        data["appliance_traffic"][MOCK_NETWORK["id"]]["reason"]
        == "Traffic analysis is not enabled"
    )
>>>>>>> origin/beta


@pytest.mark.skip(reason="TODO: Fix this test")
def test_build_detail_tasks_for_wireless_device(api_client):
    """Test that _build_detail_tasks creates the correct tasks for a wireless device."""
    # Arrange
    devices = [MOCK_DEVICE]
    networks = [MOCK_NETWORK]

    # Act
    tasks = api_client._build_detail_tasks(networks, devices)

    # Assert
    assert f"ssids_{MOCK_NETWORK['id']}" in tasks
    assert f"wireless_settings_{MOCK_DEVICE['serial']}" in tasks
    assert f"rf_profiles_{MOCK_NETWORK['id']}" in tasks


@pytest.mark.skip(reason="TODO: Fix this test")
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


@pytest.mark.skip(reason="TODO: Fix this test")
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


@pytest.mark.skip(reason="TODO: Fix this test")
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
<<<<<<< HEAD


@pytest.mark.skip(reason="TODO: Fix this test")
def test_process_detailed_data_merges_device_info(api_client):
    """Test that _process_detailed_data merges details into device objects."""
    # Arrange
    device = MOCK_DEVICE.copy()
    radio_settings = {"five_ghz_settings": {"channel": 149}}
    detail_data = {f"wireless_settings_{device['serial']}": radio_settings}

    # Act
    api_client._process_detailed_data(detail_data, [], [device], previous_data={})

    # Assert
    assert "radio_settings" in device
    assert device["radio_settings"]["five_ghz_settings"]["channel"] == 149
=======
>>>>>>> origin/beta
