"""Tests for the Meraki data coordinator."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.const.integration import DOMAIN
from custom_components.meraki_ha.const_conf import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)

# Resolved: Using the centralized coordinator path from the 2.3.0-beta.120 refactor
from custom_components.meraki_ha.coordinators import (
    MerakiMainCoordinator as MerakiDataCoordinator,
)
from homeassistant.helpers.update_coordinator import UpdateFailed
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiApiClientProtocol."""
    client = MagicMock()
    return client


@pytest.fixture
def mock_data_fetch_manager():
    """Fixture for a mocked DataFetchManager."""
    manager = MagicMock()
    manager.get_all_data = AsyncMock()
    manager.get_all_data = AsyncMock()
    manager.get_device_data = AsyncMock()
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
    # Patched to reflect the new internal module structure for base components
    with (
        patch(
            "custom_components.meraki_ha.coordinators.base.DataFetchManager",
            return_value=mock_data_fetch_manager,
        ),
    ):
        yield MerakiDataCoordinator(hass=hass, entry=entry, api_client=mock_api_client)


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

    # Act
    data = await coordinator._async_update_data()

    # Assert
    assert data["appliance_traffic"][MOCK_NETWORK.id]["error"] == "disabled"
    assert (
        data["appliance_traffic"][MOCK_NETWORK.id]["reason"]
        == "Traffic analysis is not enabled"
    )


@pytest.mark.asyncio
async def test_update_data_handles_timeout(coordinator, mock_data_fetch_manager):
    """Test that _async_update_data handles timeout."""
    # Arrange
    mock_data_fetch_manager.get_all_data.side_effect = TimeoutError()

    # Act & Assert

    # 1. Test with stale data (should return stale data after logging error)
    coordinator.last_successful_data = {"test": "data"}
    data = await coordinator._async_update_data()
    assert data == {"test": "data"}

    # 2. Test without stale data (should raise UpdateFailed)
    coordinator.last_successful_data = {}
    with pytest.raises(UpdateFailed, match="API Timeout"):
        await coordinator._async_update_data()
