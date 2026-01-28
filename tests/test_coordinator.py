"""Tests for the Meraki data coordinator."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)
from custom_components.meraki_ha.coordinator import (
    MerakiDataUpdateCoordinator as MerakiDataCoordinator,
)
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.get_all_data = AsyncMock()
    return client


@pytest.fixture
def coordinator(hass, mock_api_client):
    """Fixture for a MerakiDataCoordinator instance."""
    entry = MagicMock()
    entry.options = {}
    entry.data = {CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"}
    with patch(
        "custom_components.meraki_ha.coordinator.ApiClient",
        return_value=mock_api_client,
    ):
        yield MerakiDataCoordinator(hass=hass, entry=entry)


@pytest.mark.asyncio
async def test_update_data_handles_errors(coordinator, mock_api_client):
    """Test that _async_update_data handles disabled features."""
    # Arrange
    mock_api_client.get_all_data.return_value = {
        "networks": [MOCK_NETWORK],
        "devices": [],
        "appliance_traffic": {
            MOCK_NETWORK["id"]: {
                "error": "disabled",
                "reason": "Traffic analysis is not enabled",
            }
        },
        "vlans": {MOCK_NETWORK["id"]: []},
    }
    coordinator.add_network_status_message = MagicMock()
    coordinator.mark_traffic_check_done = MagicMock()
    coordinator.mark_vlan_check_done = MagicMock()

    # Act
    await coordinator._async_update_data()

    # Assert
    coordinator.add_network_status_message.assert_any_call(
        MOCK_NETWORK["id"], "Traffic Analysis is not enabled for this network."
    )
    coordinator.mark_traffic_check_done.assert_called_once_with(MOCK_NETWORK["id"])
    coordinator.add_network_status_message.assert_any_call(
        MOCK_NETWORK["id"], "VLANs are not enabled for this network."
    )
    coordinator.mark_vlan_check_done.assert_called_once_with(MOCK_NETWORK["id"])
