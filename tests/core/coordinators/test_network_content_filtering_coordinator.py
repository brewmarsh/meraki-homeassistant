"""Tests for the Meraki network content filtering coordinator."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.core.coordinators.network_content_filtering_coordinator import (
    NetworkContentFilteringCoordinator,
)

NETWORK_ID = "N_12345"
MOCK_CONTENT_FILTERING_DATA = {"settings": "high"}


@pytest.mark.asyncio
async def test_fetch_data(hass: HomeAssistant):
    """Test that the coordinator fetches content filtering data correctly."""
    mock_api_client = MagicMock()
    mock_api_client.appliance.get_network_appliance_content_filtering = AsyncMock(
        return_value=MOCK_CONTENT_FILTERING_DATA
    )

    coordinator = NetworkContentFilteringCoordinator(
        hass, mock_api_client, 60, NETWORK_ID
    )

    data = await coordinator._async_update_data()

    assert data == MOCK_CONTENT_FILTERING_DATA
    mock_api_client.appliance.get_network_appliance_content_filtering.assert_called_once_with(
        network_id=NETWORK_ID
    )


@pytest.mark.asyncio
async def test_update_data(hass: HomeAssistant):
    """Test that the update method calls the API client correctly."""
    mock_api_client = MagicMock()
    mock_api_client.appliance.update_network_appliance_content_filtering = AsyncMock()

    coordinator = NetworkContentFilteringCoordinator(
        hass, mock_api_client, 60, NETWORK_ID
    )
    coordinator.data = MOCK_CONTENT_FILTERING_DATA

    await coordinator.async_update_content_filtering(settings="low")

    expected_update_data = {"settings": "low"}

    expected_full_data = {**MOCK_CONTENT_FILTERING_DATA, **expected_update_data}

    mock_api_client.appliance.update_network_appliance_content_filtering.assert_called_once_with(
        network_id=NETWORK_ID, **expected_full_data
    )
