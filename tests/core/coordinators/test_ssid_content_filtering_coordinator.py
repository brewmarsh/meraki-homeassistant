"""Tests for the Meraki SSID content filtering coordinator."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.core.coordinators.ssid_content_filtering_coordinator import (
    SsidContentFilteringCoordinator,
)

NETWORK_ID = "N_12345"
SSID_NUMBER = 0
MOCK_SSID_DATA = {
    "networkId": NETWORK_ID,
    "number": SSID_NUMBER,
    "name": "Test SSID",
    "contentFiltering": {
        "settings": "high",
        "blockedUrlCategories": [
            {"id": "meraki:contentFiltering/category/1", "name": "Adult and Pornography"},
            {"id": "meraki:contentFiltering/category/2", "name": "Gambling"},
        ],
    },
    "blocked_categories_names": ["Adult and Pornography", "Gambling"],
}


@pytest.mark.asyncio
async def test_fetch_data(hass: HomeAssistant):
    """Test that the coordinator fetches SSID data correctly."""
    mock_api_client = MagicMock()
    mock_api_client.wireless.get_network_wireless_ssid = AsyncMock(
        return_value=MOCK_SSID_DATA
    )

    coordinator = SsidContentFilteringCoordinator(
        hass, mock_api_client, 60, NETWORK_ID, SSID_NUMBER
    )

    data = await coordinator._async_update_data()

    assert data == MOCK_SSID_DATA
    assert data["blocked_categories_names"] == ["Adult and Pornography", "Gambling"]
    mock_api_client.wireless.get_network_wireless_ssid.assert_called_once_with(
        network_id=NETWORK_ID, number=SSID_NUMBER
    )


@pytest.mark.asyncio
async def test_update_data(hass: HomeAssistant):
    """Test that the update method calls the API client correctly."""
    mock_api_client = MagicMock()
    mock_api_client.wireless.update_network_wireless_ssid = AsyncMock()

    coordinator = SsidContentFilteringCoordinator(
        hass, mock_api_client, 60, NETWORK_ID, SSID_NUMBER
    )
    coordinator.data = MOCK_SSID_DATA

    await coordinator.async_update_content_filtering(settings="low")

    expected_kwargs = {
        "name": "Test SSID",
        "contentFiltering": {
            "settings": "low",
            "blockedUrlCategories": [
                {"id": "meraki:contentFiltering/category/1", "name": "Adult and Pornography"},
                {"id": "meraki:contentFiltering/category/2", "name": "Gambling"},
            ],
        },
        "blocked_categories_names": ["Adult and Pornography", "Gambling"],
    }

    mock_api_client.wireless.update_network_wireless_ssid.assert_called_once_with(
        network_id=NETWORK_ID,
        number=SSID_NUMBER,
        **expected_kwargs,
    )
