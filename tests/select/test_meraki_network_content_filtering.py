"""Tests for the Meraki Network Content Filtering select entity."""

import pytest
from unittest.mock import MagicMock, AsyncMock

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.select.meraki_network_content_filtering import (
    MerakiNetworkContentFilteringSelect,
)
from custom_components.meraki_ha.core.coordinators.network_content_filtering_coordinator import (
    NetworkContentFilteringCoordinator,
)

NETWORK_ID = "N_12345"
NETWORK_DATA = {"id": NETWORK_ID, "name": "Test Network"}
MOCK_CONTENT_FILTERING_DATA = {"settings": "high"}


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked NetworkContentFilteringCoordinator."""
    coordinator = MagicMock(spec=NetworkContentFilteringCoordinator)
    coordinator.data = MOCK_CONTENT_FILTERING_DATA
    coordinator.async_update_content_filtering = AsyncMock()
    return coordinator


@pytest.mark.asyncio
async def test_select_entity_properties(hass: HomeAssistant, mock_coordinator):
    """Test the properties of the select entity."""
    config_entry = MockConfigEntry()
    entity = MerakiNetworkContentFilteringSelect(
        coordinator=mock_coordinator,
        config_entry=config_entry,
        network_data=NETWORK_DATA,
    )

    assert entity.unique_id == f"meraki-network-{NETWORK_ID}-content-filtering"
    assert entity.name == "Content Filtering Policy"
    assert entity.current_option == "high"
    assert entity.options == ["high", "moderate", "low", "approved"]


@pytest.mark.asyncio
async def test_select_option(hass: HomeAssistant, mock_coordinator):
    """Test that selecting an option calls the coordinator."""
    config_entry = MockConfigEntry()
    entity = MerakiNetworkContentFilteringSelect(
        coordinator=mock_coordinator,
        config_entry=config_entry,
        network_data=NETWORK_DATA,
    )

    await entity.async_select_option("low")

    mock_coordinator.async_update_content_filtering.assert_called_once_with(
        settings="low"
    )
