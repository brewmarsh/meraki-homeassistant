"""Tests for the Meraki API client."""

import dataclasses
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.errors import MerakiInformationalError
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork
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
            "networks": [MOCK_NETWORK],
            "devices": [MOCK_DEVICE],
        }
    )
    api_client._async_fetch_network_clients = AsyncMock(return_value=[])
    api_client._async_fetch_device_clients = AsyncMock(return_value={})
    api_client._build_detail_tasks = MagicMock(return_value={})

    # Act
    await api_client.get_all_data()

    # Assert
    api_client._async_fetch_initial_data.assert_awaited_once()
    mock_network = MerakiNetwork(organization_id="test-org", **MOCK_NETWORK)
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
<<<<<<< HEAD
    api_client._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": Exception("Network error"),
            "devices": Exception("Device error"),
            "device_statuses": Exception("Device status error"),
        }
    )

    # Act
    data = await api_client.get_all_data()
=======
    device_with_status = dataclasses.replace(MOCK_DEVICE)
    device_with_status.status = None

    availabilities = [{"serial": MOCK_DEVICE.serial, "status": "online"}]
    results = {
        "networks": [MOCK_NETWORK],
        "devices": [device_with_status],
        "devices_availabilities": availabilities,
        "appliance_uplink_statuses": [],
        "sensor_readings": [],
    }

    # Act
    data = api_client._process_initial_data(results)

    # Assert
    assert data["devices"][0].status == "online"


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
>>>>>>> 651bc8a (Refactor MerakiDevice to Dataclass)

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
