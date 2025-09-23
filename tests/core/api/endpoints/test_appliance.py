"""Tests for the appliance API endpoints."""

from unittest.mock import AsyncMock, patch
import pytest
from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.api.endpoints.appliance import (
    ApplianceEndpoints,
)
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_dashboard():
    """Fixture for a mocked meraki.DashboardAPI instance."""
    with patch("meraki.DashboardAPI") as mock_dashboard_class:
        yield mock_dashboard_class.return_value


@pytest.fixture
def api_client(mock_dashboard):
    """Fixture for a MerakiAPIClient instance."""
    return MerakiAPIClient(api_key="test-key", org_id="test-org")


@pytest.fixture
def appliance_endpoints(api_client):
    """Fixture for an ApplianceEndpoints instance."""
    return ApplianceEndpoints(api_client)


@pytest.mark.asyncio
async def test_get_network_vlans(appliance_endpoints, mock_dashboard):
    """Test get_network_vlans."""
    mock_dashboard.appliance.get_network_appliance_vlans = AsyncMock(return_value=[])
    await appliance_endpoints.get_network_vlans(MOCK_NETWORK["id"])
    mock_dashboard.appliance.get_network_appliance_vlans.assert_called_once_with(
        networkId=MOCK_NETWORK["id"]
    )


@pytest.mark.asyncio
async def test_update_network_vlan(appliance_endpoints, mock_dashboard):
    """Test update_network_vlan."""
    mock_dashboard.appliance.update_network_appliance_vlan = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.update_network_vlan(
        MOCK_NETWORK["id"], "1", name="test"
    )
    mock_dashboard.appliance.update_network_appliance_vlan.assert_called_once_with(
        networkId=MOCK_NETWORK["id"], vlanId="1", name="test"
    )


@pytest.mark.asyncio
async def test_get_l3_firewall_rules(appliance_endpoints, mock_dashboard):
    """Test get_l3_firewall_rules."""
    mock_dashboard.appliance.get_network_appliance_firewall_l3_firewall_rules = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.get_l3_firewall_rules(MOCK_NETWORK["id"])
    mock_dashboard.appliance.get_network_appliance_firewall_l3_firewall_rules.assert_called_once_with(
        networkId=MOCK_NETWORK["id"]
    )


@pytest.mark.asyncio
async def test_update_l3_firewall_rules(appliance_endpoints, mock_dashboard):
    """Test update_l3_firewall_rules."""
    mock_dashboard.appliance.update_network_appliance_firewall_l3_firewall_rules = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.update_l3_firewall_rules(
        MOCK_NETWORK["id"], rules=[]
    )
    mock_dashboard.appliance.update_network_appliance_firewall_l3_firewall_rules.assert_called_once_with(
        networkId=MOCK_NETWORK["id"], rules=[]
    )


@pytest.mark.asyncio
async def test_get_traffic_shaping(appliance_endpoints, mock_dashboard):
    """Test get_traffic_shaping."""
    mock_dashboard.appliance.get_network_appliance_traffic_shaping = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.get_traffic_shaping(MOCK_NETWORK["id"])
    mock_dashboard.appliance.get_network_appliance_traffic_shaping.assert_called_once_with(
        networkId=MOCK_NETWORK["id"]
    )


@pytest.mark.asyncio
async def test_update_traffic_shaping(appliance_endpoints, mock_dashboard):
    """Test update_traffic_shaping."""
    mock_dashboard.appliance.update_network_appliance_traffic_shaping = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.update_traffic_shaping(
        MOCK_NETWORK["id"], enabled=True
    )
    mock_dashboard.appliance.update_network_appliance_traffic_shaping.assert_called_once_with(
        networkId=MOCK_NETWORK["id"], enabled=True
    )


@pytest.mark.asyncio
async def test_get_vpn_status(appliance_endpoints, mock_dashboard):
    """Test get_vpn_status."""
    mock_dashboard.appliance.get_network_appliance_vpn_site_to_site_vpn = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.get_vpn_status(MOCK_NETWORK["id"])
    mock_dashboard.appliance.get_network_appliance_vpn_site_to_site_vpn.assert_called_once_with(
        networkId=MOCK_NETWORK["id"]
    )


@pytest.mark.asyncio
async def test_update_vpn_status(appliance_endpoints, mock_dashboard):
    """Test update_vpn_status."""
    mock_dashboard.appliance.update_network_appliance_vpn_site_to_site_vpn = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.update_vpn_status(MOCK_NETWORK["id"], mode="hub")
    mock_dashboard.appliance.update_network_appliance_vpn_site_to_site_vpn.assert_called_once_with(
        networkId=MOCK_NETWORK["id"], mode="hub"
    )
