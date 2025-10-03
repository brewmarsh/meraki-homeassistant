"""Tests for the appliance API endpoints."""

from unittest.mock import patch, MagicMock
import pytest
from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.api.endpoints.appliance import (
    ApplianceEndpoints,
)
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_dashboard():
    """Fixture for a mocked meraki.DashboardAPI instance."""
    with patch("meraki.DashboardAPI") as mock_dashboard_class:
        yield mock_dashboard_class.return_value


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
    with patch("meraki.DashboardAPI", return_value=mock_dashboard):
        client = MerakiAPIClient(
            hass=hass, api_key="test-key", org_id="test-org", coordinator=coordinator
        )
        yield client


@pytest.fixture
def appliance_endpoints(api_client, hass):
    """Fixture for an ApplianceEndpoints instance."""
    return ApplianceEndpoints(api_client, hass)


@pytest.mark.asyncio
async def test_get_network_vlans(appliance_endpoints, mock_dashboard):
    """Test get_network_vlans."""
    mock_dashboard.appliance.getNetworkApplianceVlans = MagicMock(return_value=[])
    await appliance_endpoints.get_network_vlans(MOCK_NETWORK["id"])
    mock_dashboard.appliance.getNetworkApplianceVlans.assert_called_once_with(
        networkId=MOCK_NETWORK["id"]
    )


@pytest.mark.asyncio
async def test_update_network_vlan(appliance_endpoints, mock_dashboard):
    """Test update_network_vlan."""
    mock_dashboard.appliance.updateNetworkApplianceVlan = MagicMock(
        return_value={}
    )
    await appliance_endpoints.update_network_vlan(
        MOCK_NETWORK["id"], "1", name="test"
    )
    mock_dashboard.appliance.updateNetworkApplianceVlan.assert_called_once_with(
        networkId=MOCK_NETWORK["id"], vlanId="1", name="test"
    )


@pytest.mark.asyncio
async def test_get_l3_firewall_rules(appliance_endpoints, mock_dashboard):
    """Test get_l3_firewall_rules."""
    mock_dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules = MagicMock(
        return_value={}
    )
    await appliance_endpoints.get_l3_firewall_rules(MOCK_NETWORK["id"])
    mock_dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules.assert_called_once_with(
        networkId=MOCK_NETWORK["id"]
    )


@pytest.mark.asyncio
async def test_update_l3_firewall_rules(appliance_endpoints, mock_dashboard):
    """Test update_l3_firewall_rules."""
    mock_dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules = MagicMock(
        return_value={}
    )
    await appliance_endpoints.update_l3_firewall_rules(
        MOCK_NETWORK["id"], rules=[]
    )
    mock_dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules.assert_called_once_with(
        networkId=MOCK_NETWORK["id"], rules=[]
    )


@pytest.mark.asyncio
async def test_get_traffic_shaping(appliance_endpoints, mock_dashboard):
    """Test get_traffic_shaping."""
    mock_dashboard.appliance.getNetworkApplianceTrafficShaping = MagicMock(
        return_value={}
    )
    await appliance_endpoints.get_traffic_shaping(MOCK_NETWORK["id"])
    mock_dashboard.appliance.getNetworkApplianceTrafficShaping.assert_called_once_with(
        networkId=MOCK_NETWORK["id"]
    )


@pytest.mark.asyncio
async def test_update_traffic_shaping(appliance_endpoints, mock_dashboard):
    """Test update_traffic_shaping."""
    mock_dashboard.appliance.updateNetworkApplianceTrafficShaping = MagicMock(
        return_value={}
    )
    await appliance_endpoints.update_traffic_shaping(
        MOCK_NETWORK["id"], enabled=True
    )
    mock_dashboard.appliance.updateNetworkApplianceTrafficShaping.assert_called_once_with(
        networkId=MOCK_NETWORK["id"], enabled=True
    )


@pytest.mark.asyncio
async def test_get_vpn_status(appliance_endpoints, mock_dashboard):
    """Test get_vpn_status."""
    mock_dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn = MagicMock(
        return_value={}
    )
    await appliance_endpoints.get_vpn_status(MOCK_NETWORK["id"])
    mock_dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn.assert_called_once_with(
        networkId=MOCK_NETWORK["id"]
    )


@pytest.mark.asyncio
async def test_update_vpn_status(appliance_endpoints, mock_dashboard):
    """Test update_vpn_status."""
    mock_dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn = MagicMock(
        return_value={}
    )
    await appliance_endpoints.update_vpn_status(MOCK_NETWORK["id"], mode="hub")
    mock_dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn.assert_called_once_with(
        networkId=MOCK_NETWORK["id"], mode="hub"
    )