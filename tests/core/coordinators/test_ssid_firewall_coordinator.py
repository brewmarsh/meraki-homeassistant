"""Tests for SSID firewall coordinator."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.meraki_ha.core.coordinators.ssid_firewall_coordinator import (
    SsidFirewallCoordinator,
)


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock hass instance."""
    return MagicMock()


@pytest.fixture
def mock_api_client() -> MagicMock:
    """Create a mock API client."""
    client = MagicMock()
    client.wireless = MagicMock()
    client.wireless.get_network_wireless_ssid_l7_firewall_rules = AsyncMock(
        return_value={"rules": []}
    )
    return client


def test_coordinator_initialization(
    mock_hass: MagicMock,
    mock_api_client: MagicMock,
) -> None:
    """Test coordinator initializes correctly."""
    coordinator = SsidFirewallCoordinator(
        hass=mock_hass,
        api_client=mock_api_client,
        network_id="N_123",
        ssid_number=0,
    )

    assert coordinator.network_id == "N_123"
    assert coordinator.ssid_number == 0
    assert coordinator.api_client is mock_api_client


def test_coordinator_initialization_with_update_interval(
    mock_hass: MagicMock,
    mock_api_client: MagicMock,
) -> None:
    """Test coordinator uses update_interval when provided."""
    coordinator = SsidFirewallCoordinator(
        hass=mock_hass,
        api_client=mock_api_client,
        network_id="N_123",
        ssid_number=0,
        update_interval=120,
    )

    assert coordinator.network_id == "N_123"


@pytest.mark.asyncio
async def test_async_update_data(
    mock_hass: MagicMock,
    mock_api_client: MagicMock,
) -> None:
    """Test update fetches firewall rules."""
    mock_api_client.wireless.get_network_wireless_ssid_l7_firewall_rules.return_value = [
        {"policy": "deny", "type": "ipRange", "value": "192.168.1.100"},
    ]

    coordinator = SsidFirewallCoordinator(
        hass=mock_hass,
        api_client=mock_api_client,
        network_id="N_123",
        ssid_number=0,
    )

    result = await coordinator._async_update_data()

    assert "rules" in result
    mock_api_client.wireless.get_network_wireless_ssid_l7_firewall_rules.assert_called_once_with(
        network_id="N_123",
        number="0",
    )


@pytest.mark.asyncio
async def test_async_update_data_error(
    mock_hass: MagicMock,
    mock_api_client: MagicMock,
) -> None:
    """Test update raises UpdateFailed on error."""
    mock_api_client.wireless.get_network_wireless_ssid_l7_firewall_rules.side_effect = (
        Exception("API Error")
    )

    coordinator = SsidFirewallCoordinator(
        hass=mock_hass,
        api_client=mock_api_client,
        network_id="N_123",
        ssid_number=0,
    )

    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()
