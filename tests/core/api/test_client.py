"""Tests for the Meraki API client."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.meraki_ha.core.api.client import MerakiAPIClient

@pytest.fixture
def mock_dashboard():
    """Fixture for a mocked meraki.DashboardAPI."""
    return MagicMock()

@pytest.fixture
def api_client(mock_dashboard):
    """Fixture for a MerakiAPIClient with a mocked dashboard."""
    with patch('meraki.DashboardAPI', return_value=mock_dashboard):
        client = MerakiAPIClient(api_key='test_key', org_id='test_org')
        yield client

async def test_get_networks(api_client, mock_dashboard):
    """Test getting networks."""
    mock_dashboard.organizations.getOrganizationNetworks = AsyncMock(return_value=[{'id': 'net1'}])
    networks = await api_client.get_networks()
    assert networks == [{'id': 'net1'}]
    mock_dashboard.organizations.getOrganizationNetworks.assert_called_once_with(organizationId='test_org')

async def test_get_devices(api_client, mock_dashboard):
    """Test getting devices."""
    mock_dashboard.organizations.getOrganizationDevices = AsyncMock(return_value=[{'serial': 'dev1'}])
    devices = await api_client.get_devices()
    assert devices == [{'serial': 'dev1'}]
    mock_dashboard.organizations.getOrganizationDevices.assert_called_once_with(organizationId='test_org')

async def test_get_device_statuses(api_client, mock_dashboard):
    """Test getting device statuses."""
    mock_dashboard.organizations.getOrganizationDeviceStatuses = AsyncMock(return_value=[{'serial': 'dev1', 'status': 'online'}])
    statuses = await api_client.get_organization_device_statuses()
    assert statuses == [{'serial': 'dev1', 'status': 'online'}]
    mock_dashboard.organizations.getOrganizationDeviceStatuses.assert_called_once_with(organizationId='test_org')

async def test_get_appliance_ports(api_client, mock_dashboard):
    """Test getting appliance ports."""
    mock_dashboard.appliance.getNetworkAppliancePorts = AsyncMock(return_value=[{'number': 1}])
    ports = await api_client.get_appliance_ports(network_id='net1')
    assert ports == [{'number': 1}]
    mock_dashboard.appliance.getNetworkAppliancePorts.assert_called_once_with(networkId='net1')

async def test_get_device_uplink(api_client, mock_dashboard):
    """Test getting device uplink."""
    mock_dashboard.devices.getDeviceUplinkStats = AsyncMock(return_value=[{'interface': 'WAN 1'}])
    uplink = await api_client.get_device_uplink_stats(serial='dev1')
    assert uplink == [{'interface': 'WAN 1'}]
    mock_dashboard.devices.getDeviceUplinkStats.assert_called_once_with(serial='dev1')

async def test_get_ssids(api_client, mock_dashboard):
    """Test getting SSIDs."""
    mock_dashboard.wireless.getNetworkWirelessSsids = AsyncMock(return_value=[{'number': 0}])
    ssids = await api_client.get_ssids(network_id='net1')
    assert ssids == [{'number': 0}]
    mock_dashboard.wireless.getNetworkWirelessSsids.assert_called_once_with(networkId='net1')

async def test_update_network_wireless_ssid(api_client, mock_dashboard):
    """Test updating an SSID."""
    mock_dashboard.wireless.updateNetworkWirelessSsid = AsyncMock()
    await api_client.update_network_wireless_ssid(network_id='net1', number='0', name='New Name')
    mock_dashboard.wireless.updateNetworkWirelessSsid.assert_called_once_with(networkId='net1', number='0', name='New Name')

async def test_get_camera_video_settings(api_client, mock_dashboard):
    """Test getting camera video settings."""
    mock_dashboard.camera.getDeviceCameraVideoSettings = AsyncMock(return_value={'rtspUrl': 'rtsp://...'})
    settings = await api_client.get_camera_video_settings(serial='cam1')
    assert settings == {'rtspUrl': 'rtsp://...'}
    mock_dashboard.camera.getDeviceCameraVideoSettings.assert_called_once_with(serial='cam1')

async def test_update_camera_video_settings(api_client, mock_dashboard):
    """Test updating camera video settings."""
    mock_dashboard.camera.updateDeviceCameraVideoSettings = AsyncMock()
    await api_client.update_camera_video_settings(serial='cam1', rtsp_server_enabled=True)
    mock_dashboard.camera.updateDeviceCameraVideoSettings.assert_called_once_with(serial='cam1', rtsp_server_enabled=True)
