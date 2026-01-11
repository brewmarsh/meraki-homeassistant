"""Tests for the appliance API endpoints."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.api.endpoints.appliance import (
    ApplianceEndpoints,
)
from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_dashboard() -> MagicMock:
    """Fixture for a mocked meraki.aio.AsyncDashboardAPI instance."""
    return MagicMock()


@pytest.fixture
def hass() -> MagicMock:
    """Fixture for a mocked Home Assistant instance."""
    return MagicMock()


@pytest.fixture
def coordinator() -> MagicMock:
    """Fixture for a mocked coordinator."""
    mock = MagicMock(spec=MerakiDataCoordinator)
    mock.is_vlan_check_due.return_value = True
    mock.is_traffic_check_due.return_value = True
    return mock


@pytest.fixture
def api_client(hass: MagicMock, mock_dashboard: MagicMock) -> MerakiAPIClient:
    """Fixture for a MerakiAPIClient instance."""
    client = MerakiAPIClient(hass=hass, api_key="test-key", org_id="test-org")
    client.dashboard = mock_dashboard
    return client


@pytest.fixture
def appliance_endpoints(
    api_client: MerakiAPIClient, hass: MagicMock
) -> ApplianceEndpoints:
    """Fixture for an ApplianceEndpoints instance."""
    return ApplianceEndpoints(api_client, hass)


@pytest.mark.asyncio
async def test_get_network_vlans(
    appliance_endpoints: ApplianceEndpoints, mock_dashboard: MagicMock
) -> None:
    """Test get_network_vlans."""
    mock_dashboard.appliance.getNetworkApplianceVlans = AsyncMock(return_value=[])
    await appliance_endpoints.get_network_vlans(MOCK_NETWORK["id"])
    mock_dashboard.appliance.getNetworkApplianceVlans.assert_called_once_with(
        networkId=MOCK_NETWORK["id"]
    )


@pytest.mark.asyncio
async def test_update_network_vlan(
    appliance_endpoints: ApplianceEndpoints, mock_dashboard: MagicMock
) -> None:
    """Test update_network_vlan."""
    mock_dashboard.appliance.updateNetworkApplianceVlan = AsyncMock(return_value={})
    await appliance_endpoints.update_network_vlan(MOCK_NETWORK["id"], "1", name="test")
    mock_dashboard.appliance.updateNetworkApplianceVlan.assert_called_once_with(
        networkId=MOCK_NETWORK["id"], vlanId="1", name="test"
    )


@pytest.mark.asyncio
async def test_get_l3_firewall_rules(
    appliance_endpoints: ApplianceEndpoints, mock_dashboard: MagicMock
) -> None:
    """Test get_l3_firewall_rules."""
    mock_dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.get_l3_firewall_rules(MOCK_NETWORK["id"])
    (
        mock_dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules.assert_called_once_with(
            networkId=MOCK_NETWORK["id"]
        )
    )


@pytest.mark.asyncio
async def test_update_l3_firewall_rules(
    appliance_endpoints: ApplianceEndpoints, mock_dashboard: MagicMock
) -> None:
    """Test update_l3_firewall_rules."""
    mock_dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.update_l3_firewall_rules(MOCK_NETWORK["id"], rules=[])
    (
        mock_dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules.assert_called_once_with(
            networkId=MOCK_NETWORK["id"], rules=[]
        )
    )


@pytest.mark.asyncio
async def test_get_traffic_shaping(
    appliance_endpoints: ApplianceEndpoints, mock_dashboard: MagicMock
) -> None:
    """Test get_traffic_shaping."""
    mock_dashboard.appliance.getNetworkApplianceTrafficShaping = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.get_traffic_shaping(MOCK_NETWORK["id"])
    mock_dashboard.appliance.getNetworkApplianceTrafficShaping.assert_called_once_with(
        networkId=MOCK_NETWORK["id"]
    )


@pytest.mark.asyncio
async def test_update_traffic_shaping(
    appliance_endpoints: ApplianceEndpoints, mock_dashboard: MagicMock
) -> None:
    """Test update_traffic_shaping."""
    mock_dashboard.appliance.updateNetworkApplianceTrafficShaping = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.update_traffic_shaping(MOCK_NETWORK["id"], enabled=True)
    (
        mock_dashboard.appliance.updateNetworkApplianceTrafficShaping.assert_called_once_with(
            networkId=MOCK_NETWORK["id"], enabled=True
        )
    )


@pytest.mark.asyncio
async def test_get_vpn_status(
    appliance_endpoints: ApplianceEndpoints, mock_dashboard: MagicMock
) -> None:
    """Test get_vpn_status."""
    mock_dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.get_vpn_status(MOCK_NETWORK["id"])
    (
        mock_dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn.assert_called_once_with(
            networkId=MOCK_NETWORK["id"]
        )
    )


@pytest.mark.asyncio
async def test_update_vpn_status(
    appliance_endpoints: ApplianceEndpoints, mock_dashboard: MagicMock
) -> None:
    """Test update_vpn_status."""
    mock_dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn = AsyncMock(
        return_value={}
    )
    await appliance_endpoints.update_vpn_status(MOCK_NETWORK["id"], mode="hub")
    (
        mock_dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn.assert_called_once_with(
            networkId=MOCK_NETWORK["id"], mode="hub"
        )
    )
