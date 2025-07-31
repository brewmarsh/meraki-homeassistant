"""Tests for the Meraki device coordinator."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from custom_components.meraki_ha.core.coordinators.device import MerakiDeviceCoordinator

@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.get_devices = AsyncMock(return_value=[
        {'serial': 'dev1', 'model': 'MR52', 'networkId': 'net1'},
        {'serial': 'dev2', 'model': 'MS220-8P', 'networkId': 'net1'},
    ])
    client.get_organization_device_statuses = AsyncMock(return_value=[
        {'serial': 'dev1', 'status': 'online'},
        {'serial': 'dev2', 'status': 'offline'},
    ])
    client.get_appliance_ports = AsyncMock(return_value=[{'number': 1}])
    client.get_device_uplink_stats = AsyncMock(return_value=[{'interface': 'WAN 1'}])
    client.get_organization_firmware_upgrades = AsyncMock(return_value=[])
    return client

@pytest.fixture
async def device_coordinator(mock_api_client):
    """Fixture for a MerakiDeviceCoordinator with a mocked API client."""
    coordinator = MerakiDeviceCoordinator(
        hass=MagicMock(),
        api_client=mock_api_client,
        name='device_coordinator',
        update_interval=MagicMock(),
    )
    await coordinator.async_config_entry_first_refresh()
    return coordinator

async def test_device_coordinator_data(device_coordinator):
    """Test that the device coordinator fetches and processes data correctly."""
    assert device_coordinator.data is not None
    assert len(device_coordinator.data['devices']) == 2
    assert device_coordinator.data['devices'][0]['serial'] == 'dev1'
    assert device_coordinator.data['devices'][0]['productType'] == 'wireless'
    assert device_coordinator.data['devices'][0]['status'] == 'online'
    assert device_coordinator.data['devices'][1]['serial'] == 'dev2'
    assert device_coordinator.data['devices'][1]['productType'] == 'switch'
    assert device_coordinator.data['devices'][1]['status'] == 'offline'

async def test_get_device_by_serial(device_coordinator):
    """Test getting a device by its serial number."""
    device = device_coordinator.get_device_by_serial('dev1')
    assert device is not None
    assert device['serial'] == 'dev1'
    assert device_coordinator.get_device_by_serial('dev3') is None
