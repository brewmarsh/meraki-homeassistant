"""Tests for the Meraki SSID Content Filtering select entity."""

import pytest
from unittest.mock import MagicMock, AsyncMock

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.select.meraki_content_filtering import (
    MerakiSsidContentFilteringSelect,
)
from custom_components.meraki_ha.core.coordinators.ssid_content_filtering_coordinator import (
    SsidContentFilteringCoordinator,
)

NETWORK_ID = "N_12345"
SSID_NUMBER = 0
MOCK_SSID_DATA = {
    "networkId": NETWORK_ID,
    "number": SSID_NUMBER,
    "name": "Test SSID",
    "contentFiltering": {"settings": "high"},
}


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked SsidContentFilteringCoordinator."""
    coordinator = MagicMock(spec=SsidContentFilteringCoordinator)
    coordinator.data = MOCK_SSID_DATA
    coordinator.async_update_content_filtering = AsyncMock()
    return coordinator


@pytest.mark.asyncio
async def test_select_entity_properties(hass: HomeAssistant, mock_coordinator):
    """Test the properties of the select entity."""
    config_entry = MockConfigEntry()
    entity = MerakiSsidContentFilteringSelect(
        coordinator=mock_coordinator,
        config_entry=config_entry,
        ssid_data=MOCK_SSID_DATA,
    )

    assert (
        entity.unique_id
        == f"meraki-ssid-{NETWORK_ID}-{SSID_NUMBER}-content-filtering"
    )
    assert entity.name == "Content Filtering Policy"
    assert entity.current_option == "high"
    assert entity.options == ["high", "moderate", "low", "approved"]


@pytest.mark.asyncio
async def test_select_option(hass: HomeAssistant, mock_coordinator):
    """Test that selecting an option calls the coordinator."""
    config_entry = MockConfigEntry()
    entity = MerakiSsidContentFilteringSelect(
        coordinator=mock_coordinator,
        config_entry=config_entry,
        ssid_data=MOCK_SSID_DATA,
    )

    await entity.async_select_option("low")

    mock_coordinator.async_update_content_filtering.assert_called_once_with(
        settings="low"
    )
