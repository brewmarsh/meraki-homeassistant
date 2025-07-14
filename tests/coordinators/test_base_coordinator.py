"""Tests for the Meraki base coordinator."""
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.coordinators.base_coordinator import (
    MerakiDataUpdateCoordinator,
)


async def test_meraki_data_update_coordinator(
    hass: HomeAssistant,
) -> None:
    """Test the Meraki data update coordinator."""
    api_fetcher = MagicMock()
    data_processor = MagicMock()
    data_aggregator = MagicMock()
    coordinator = MerakiDataUpdateCoordinator(
        hass, "api_key", "org_id", 300, MagicMock()
    )
    coordinator.api_fetcher = api_fetcher
    coordinator.data_processor = data_processor
    coordinator.data_aggregator = data_aggregator
    api_fetcher.fetch_all_data.return_value = {
        "devices": [],
        "networks": [],
        "ssids": [],
        "clients": [],
    }
    await coordinator._async_update_data()
    assert coordinator.data is not None
