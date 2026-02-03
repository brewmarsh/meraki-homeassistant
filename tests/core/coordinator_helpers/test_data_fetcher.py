"""Tests for the Meraki DataFetchManager."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork
from tests.const import MOCK_DEVICE, MOCK_DEVICE_INIT, MOCK_NETWORK, MOCK_NETWORK_INIT


@pytest.fixture
def mock_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock(spec=MerakiAPIClient)
    client.wireless = AsyncMock()
    client.switch = AsyncMock()
    client.camera = AsyncMock()
    client.appliance = AsyncMock()
    client.network = AsyncMock()
    client.organization = AsyncMock()
    client.devices = AsyncMock()
    client.sensor = AsyncMock()

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
    client.appliance.get_organization_appliance_uplink_statuses = AsyncMock(
        return_value=[]
    )

    client.network.get_network_traffic = AsyncMock(return_value={})

    client.sensor.get_organization_sensor_readings_latest = AsyncMock(return_value=[])

    client.dashboard = MagicMock()

    # Mock run_with_semaphore to execute the coroutine
    async def run_with_semaphore_side_effect(coro):
        return await coro

    client.run_with_semaphore = AsyncMock(side_effect=run_with_semaphore_side_effect)

    return client


@pytest.fixture
def data_fetch_manager(mock_client):
    """Fixture for a DataFetchManager instance."""
    return DataFetchManager(client=mock_client)


@pytest.mark.asyncio
async def test_get_all_data_orchestration(data_fetch_manager):
    """Test that get_all_data correctly orchestrates helper methods."""
    # Arrange
    data_fetch_manager._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [MOCK_NETWORK_INIT],
        }
    )
    data_fetch_manager.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={"devices": [MOCK_DEVICE], "battery_readings": None}
    )
    data_fetch_manager.client_fetcher.async_fetch_network_clients = AsyncMock(
        return_value=[]
    )
    data_fetch_manager.client_fetcher.async_fetch_device_clients = AsyncMock(
        return_value={}
    )
    data_fetch_manager._build_detail_tasks = MagicMock(return_value={})

    with (
        patch("custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_appliance_data"),
        patch("custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_sensor_data"),
    ):
        # Act
        await data_fetch_manager.get_all_data()

    # Assert
    data_fetch_manager._async_fetch_initial_data.assert_awaited_once()
    data_fetch_manager.device_fetcher.async_fetch_devices.assert_awaited_once()
    data_fetch_manager.client_fetcher.async_fetch_network_clients.assert_awaited_once()
    data_fetch_manager.client_fetcher.async_fetch_device_clients.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_data_handles_api_errors(data_fetch_manager, caplog):
    """Test that get_all_data handles API errors gracefully."""
    # Arrange
    data_fetch_manager._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": Exception("Network error"),
        }
    )
    data_fetch_manager.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={"devices": [], "battery_readings": None}
    )
    data_fetch_manager.client_fetcher.async_fetch_network_clients = AsyncMock(
        side_effect=Exception("Client fetch error")
    )
    data_fetch_manager.client_fetcher.async_fetch_device_clients = AsyncMock(
        side_effect=Exception("Device client fetch error")
    )

    # Act
    data = await data_fetch_manager.get_all_data()

    # Assert
    assert data["networks"] == []
    assert data["devices"] == []
    assert "Could not fetch networks" in caplog.text


@pytest.mark.asyncio
async def test_get_all_data_handles_informational_errors(data_fetch_manager):
    """Test that get_all_data handles informational API errors."""
    # Arrange
    data_fetch_manager._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [MOCK_NETWORK_INIT],
            "devices": [MOCK_DEVICE_INIT],
            "device_statuses": [],
        }
    )
    data_fetch_manager.client_fetcher.async_fetch_network_clients = AsyncMock(
        return_value=[]
    )
    data_fetch_manager.client_fetcher.async_fetch_device_clients = AsyncMock(
        return_value={}
    )

    async def coro():
        from custom_components.meraki_ha.core.errors import MerakiTrafficAnalysisError

        return MerakiTrafficAnalysisError("Traffic analysis is not enabled")

    data_fetch_manager._build_detail_tasks = MagicMock(
        return_value={f"traffic_{MOCK_NETWORK_INIT['id']}": coro()}
    )

    with (
        patch("custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_appliance_data"),
        patch("custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_sensor_data"),
    ):
        # Act
        data = await data_fetch_manager.get_all_data()

    # Assert
    assert data["appliance_traffic"][MOCK_NETWORK_INIT["id"]]["error"] == "disabled"
    assert (
        data["appliance_traffic"][MOCK_NETWORK_INIT["id"]]["reason"]
        == "Traffic analysis is not enabled"
    )


@pytest.mark.asyncio
async def test_build_detail_tasks_for_wireless_device(data_fetch_manager, mock_client):
    """Test that _build_detail_tasks creates the correct tasks for a wireless device."""
    # Arrange
    devices = [MOCK_DEVICE]
    networks = [MOCK_NETWORK]

    # Act
    tasks = data_fetch_manager._build_detail_tasks(networks, devices)

    # Assert
    assert f"ssids_{MOCK_NETWORK.id}" in tasks
    assert f"rf_profiles_{MOCK_NETWORK.id}" in tasks

    # Clean up coroutines to avoid warnings
    for task in tasks.values():
        await task


@pytest.mark.asyncio
async def test_get_all_data_includes_switch_ports(data_fetch_manager, mock_client):
    """Test that get_all_data returns switch ports statuses."""
    # Arrange
    switch_device = MerakiDevice.from_dict({"serial": "Q123", "productType": "switch"})
    data_fetch_manager._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [],
            "devices": [],
        }
    )
    # Ensure device_fetcher returns our switch device
    data_fetch_manager.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={"devices": [switch_device], "battery_readings": None}
    )
    data_fetch_manager.client_fetcher.async_fetch_network_clients = AsyncMock(
        return_value=[]
    )
    data_fetch_manager.client_fetcher.async_fetch_device_clients = AsyncMock(
        return_value={}
    )

    # Simulate detailed switch ports response
    async def coro():
        return [{"portId": "1", "status": "Connected"}]

    data_fetch_manager._build_detail_tasks = MagicMock(
        return_value={"ports_statuses_Q123": coro()}
    )

    with (
        patch("custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_appliance_data"),
        patch("custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_sensor_data"),
    ):
        # Act
        await data_fetch_manager.get_all_data()

    # Assert
    assert switch_device.ports_statuses == [{"portId": "1", "status": "Connected"}]


@pytest.mark.asyncio
async def test_build_detail_tasks_for_switch_device(data_fetch_manager, mock_client):
    """Test that _build_detail_tasks creates the correct tasks for a switch device."""
    # Arrange
    switch_device = MerakiDevice.from_dict({"serial": "s123", "productType": "switch"})
    devices = [switch_device]
    networks = []

    # Mock endpoints and semaphore wrapper to avoid unawaited coroutine warnings
    mock_client.switch.get_device_switch_ports_statuses.return_value = (
        "mock_switch_coro"
    )
    mock_client.run_with_semaphore = MagicMock(side_effect=lambda x: x)

    # Act
    tasks = data_fetch_manager._build_detail_tasks(networks, devices)

    # Assert
    assert f"ports_statuses_{switch_device.serial}" in tasks
    # Clean up coroutines to avoid warnings
    for task in tasks.values():
        await task
    mock_client.switch.get_device_switch_ports_statuses.assert_called_once_with("s123")


@pytest.mark.asyncio
async def test_build_detail_tasks_for_camera_device(data_fetch_manager, mock_client):
    """Test that _build_detail_tasks creates the correct tasks for a camera device."""
    # Arrange
    camera_device = MerakiDevice.from_dict({"serial": "c123", "productType": "camera"})
    devices = [camera_device]
    networks = []

    # Mock dependencies to avoid unawaited coroutine warnings
    mock_client.run_with_semaphore = MagicMock(side_effect=lambda x: x)

    # Act
    tasks = data_fetch_manager._build_detail_tasks(networks, devices)

    # Assert
    assert f"video_settings_{camera_device.serial}" in tasks
    assert f"sense_settings_{camera_device.serial}" in tasks

    # Clean up coroutines to avoid warnings
    for task in tasks.values():
        await task

    mock_client.camera.get_camera_video_settings.assert_called_once_with("c123")
    mock_client.camera.get_camera_sense_settings.assert_called_once_with("c123")


@pytest.mark.asyncio
async def test_build_detail_tasks_for_appliance_device(data_fetch_manager, mock_client):
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

    # Enable VPN management to trigger vpn_status task
    data_fetch_manager.enable_vpn_management = True

    # Mock run_with_semaphore to return the input immediately (pass-through)
    mock_client.run_with_semaphore = MagicMock(side_effect=lambda x: x)

    # Mock endpoint methods to return dummy task objects
    mock_client.network.get_network_traffic = MagicMock(return_value="task_traffic")
    mock_client.appliance.get_network_vlans = MagicMock(return_value="task_vlans")
    mock_client.appliance.get_l3_firewall_rules = MagicMock(
        return_value="task_firewall"
    )
    mock_client.appliance.get_traffic_shaping = MagicMock(return_value="task_shaping")
    mock_client.appliance.get_vpn_status = MagicMock(return_value="task_vpn")
    mock_client.appliance.get_network_appliance_content_filtering = MagicMock(
        return_value="task_filtering"
    )
    mock_client.appliance.get_network_appliance_settings = MagicMock(
        return_value="task_settings"
    )
    mock_client.appliance.get_appliance_ports = MagicMock(return_value="task_ports")

    # Act
    with patch("asyncio.create_task", side_effect=lambda x: x):
        tasks = data_fetch_manager._build_detail_tasks(networks, devices)

    # Assert
    # Check network tasks
    assert tasks[f"traffic_{network_with_appliance.id}"] == "task_traffic"
    assert tasks[f"vlans_{network_with_appliance.id}"] == "task_vlans"
    assert tasks[f"l3_firewall_rules_{network_with_appliance.id}"] == "task_firewall"
    assert tasks[f"traffic_shaping_{network_with_appliance.id}"] == "task_shaping"
    assert tasks[f"vpn_status_{network_with_appliance.id}"] == "task_vpn"
    assert tasks[f"appliance_ports_{network_with_appliance.id}"] == "task_ports"
    assert tasks[f"content_filtering_{network_with_appliance.id}"] == "task_filtering"

    # Check device tasks
    assert tasks[f"appliance_settings_{appliance_device.serial}"] == "task_settings"


def test_process_detailed_data_merges_device_info(data_fetch_manager):
    """Test that _process_detailed_data merges details into device objects."""
    # Arrange
    device = MerakiDevice(serial="c123", product_type="camera")
    video_settings = {"rtsp_url": "rtsp://test", "rtspServerEnabled": True}
    detail_data = {f"video_settings_{device.serial}": video_settings}

    # Act
    data_fetch_manager._process_detailed_data(
        detail_data, [], [device], previous_data={}
    )

    # Assert
    assert device.video_settings == video_settings
    assert device.rtsp_url == "rtsp://test"

@pytest.mark.asyncio
async def test_vpn_status_not_fetched_when_disabled(mock_client):
    """Test that VPN status is not fetched when enable_vpn_management is False."""
    manager = DataFetchManager(client=mock_client, enable_vpn_management=False)

    # Mock helpers
    manager._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [{"id": "N_123", "productTypes": ["appliance"]}],
        }
    )
    manager.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={"devices": [], "battery_readings": None}
    )
    manager.client_fetcher.async_fetch_network_clients = AsyncMock(return_value=[])
    manager.client_fetcher.async_fetch_device_clients = AsyncMock(return_value={})

    mock_client.appliance.get_vpn_status = AsyncMock()
    mock_client.run_with_semaphore = MagicMock(side_effect=lambda x: x)

    with (
        patch("custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_appliance_data"),
        patch("custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_sensor_data"),
    ):
        # Run get_all_data
        await manager.get_all_data()

    # Verify get_vpn_status was NOT called
    mock_client.appliance.get_vpn_status.assert_not_called()

@pytest.mark.asyncio
async def test_vpn_status_fetched_when_enabled(mock_client):
    """Test that VPN status is fetched when enable_vpn_management is True."""
    manager = DataFetchManager(client=mock_client, enable_vpn_management=True)

    # Mock helpers
    manager._async_fetch_initial_data = AsyncMock(
        return_value={
            "networks": [{"id": "N_123", "productTypes": ["appliance"]}],
        }
    )
    manager.device_fetcher.async_fetch_devices = AsyncMock(
        return_value={"devices": [], "battery_readings": None}
    )
    manager.client_fetcher.async_fetch_network_clients = AsyncMock(return_value=[])
    manager.client_fetcher.async_fetch_device_clients = AsyncMock(return_value={})

    mock_client.appliance.get_vpn_status = MagicMock(return_value="task_vpn")
    mock_client.run_with_semaphore = AsyncMock(side_effect=lambda x: x)
    mock_client.appliance.get_network_vlans = MagicMock(return_value="task_vlans")
    mock_client.network.get_network_traffic = MagicMock(return_value="task_traffic")
    mock_client.appliance.get_l3_firewall_rules = MagicMock(return_value="task_fw")
    mock_client.appliance.get_traffic_shaping = MagicMock(return_value="task_shaping")
    mock_client.appliance.get_appliance_ports = MagicMock(return_value="task_ports")
    mock_client.appliance.get_network_appliance_content_filtering = MagicMock(
        return_value="task_content"
    )


    with (
        patch("asyncio.create_task", side_effect=lambda x: x),
        patch("custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_appliance_data"),
        patch("custom_components.meraki_ha.core.coordinator_helpers.data_fetcher.parse_sensor_data"),
    ):
         await manager.get_all_data()

    # Verify get_vpn_status WAS called
    mock_client.appliance.get_vpn_status.assert_called_once_with("N_123")
