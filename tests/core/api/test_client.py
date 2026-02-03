"""Tests for the Meraki API client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.api.client import MerakiAPIClient


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
def api_client(hass, mock_dashboard):
    """Fixture for a MerakiAPIClient instance."""
    client = MerakiAPIClient(hass=hass, api_key="test-key", org_id="test-org")
    # Mock the internal endpoint handlers to avoid real API calls
    client.wireless = AsyncMock()
    client.switch = AsyncMock()
    client.camera = AsyncMock()
    client.appliance = AsyncMock()
    client.network = AsyncMock()
    client.organization = AsyncMock()
    client.devices = AsyncMock()
    client.sensor = AsyncMock()

    client.dashboard = MagicMock()
    return client


@pytest.mark.asyncio
async def test_get_network_events_filters_none(api_client):
    """Test that get_network_events filters out None values from arguments."""
    # Arrange
    api_client.dashboard.networks.getNetworkEvents.return_value = {"events": []}
    network_id = "N_123"

    # Act
    await api_client.get_network_events(network_id)

    # Assert
    api_client.dashboard.networks.getNetworkEvents.assert_called_once()
    args, kwargs = api_client.dashboard.networks.getNetworkEvents.call_args
    assert network_id in args
    # Ensure no None values in kwargs
    for key, value in kwargs.items():
        assert value is not None, f"Found None value for key: {key}"
    # Specifically check that productType is not in kwargs (since it defaults to None)
    assert "productType" not in kwargs


@pytest.mark.asyncio
async def test_get_network_events_passes_values(api_client):
    """Test that get_network_events passes non-None values correctly."""
    # Arrange
    api_client.dashboard.networks.getNetworkEvents.return_value = {"events": []}
    network_id = "N_123"
    product_type = "appliance"

    # Act
    await api_client.get_network_events(network_id, product_type=product_type)

    # Assert
    api_client.dashboard.networks.getNetworkEvents.assert_called_once()
    args, kwargs = api_client.dashboard.networks.getNetworkEvents.call_args
    assert kwargs.get("productType") == product_type
