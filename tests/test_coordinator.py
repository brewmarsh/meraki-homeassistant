"""Tests for the Meraki data coordinator."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    DOMAIN,
)
from custom_components.meraki_ha.coordinator import (
    MerakiDataUpdateCoordinator as MerakiDataCoordinator,
)
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    # client.get_all_data is no longer used directly
    return client


@pytest.fixture
def mock_data_fetch_manager():
    """Fixture for a mocked DataFetchManager."""
    manager = MagicMock()
    manager.get_all_data = AsyncMock()
    return manager


@pytest.fixture
def coordinator(hass, mock_api_client, mock_data_fetch_manager):
    """Fixture for a MerakiDataCoordinator instance."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
        options={},
    )
    entry.add_to_hass(hass)
    with patch(
        "custom_components.meraki_ha.coordinator.ApiClient",
        return_value=mock_api_client,
    ), patch(
        "custom_components.meraki_ha.coordinator.DataFetchManager",
        return_value=mock_data_fetch_manager,
    ):
        yield MerakiDataCoordinator(hass=hass, entry=entry)


@pytest.mark.asyncio
async def test_update_data_handles_errors(coordinator, mock_data_fetch_manager):
    """Test that _async_update_data handles disabled features."""
    # Arrange
    mock_data_fetch_manager.get_all_data.return_value = {
        "networks": [MOCK_NETWORK],
        "devices": [],
        "appliance_traffic": {
            MOCK_NETWORK.id: {
                "error": "disabled",
                "reason": "Traffic analysis is not enabled",
            }
        },
        "vlans": {MOCK_NETWORK.id: []},
    }
    coordinator.add_network_status_message = MagicMock()
    coordinator.mark_traffic_check_done = MagicMock()
    coordinator.mark_vlan_check_done = MagicMock()

    # Act
    data = await coordinator._async_update_data()

    # Assert
    assert data["appliance_traffic"][MOCK_NETWORK.id]["error"] == "disabled"
    assert (
        data["appliance_traffic"][MOCK_NETWORK.id]["reason"]
        == "Traffic analysis is not enabled"
    )
