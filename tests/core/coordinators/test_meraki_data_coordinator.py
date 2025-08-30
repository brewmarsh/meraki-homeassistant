"""Tests for the Meraki data coordinator."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry
import copy

from custom_components.meraki_ha.core.coordinators.meraki_data_coordinator import (
    MerakiDataCoordinator,
)
from datetime import datetime, timedelta
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_IGNORED_NETWORKS,
    CONF_HIDE_UNCONFIGURED_SSIDS,
    CONF_USE_STALE_DATA,
    CONF_STALE_DATA_THRESHOLD,
)

BASE_MOCK_DATA = {
    "networks": [
        {"id": "N_1", "name": "Network To Keep"},
        {"id": "N_2", "name": "Network To Ignore"},
    ],
    "ssids": [
        {"id": "s_1", "name": "Enabled SSID", "enabled": True},
        {"id": "s_2", "name": "Disabled SSID", "enabled": False},
    ],
}

@pytest.fixture
def mock_api_client():
    """Fixture for a mocked API client."""
    client = MagicMock()
    client.get_all_data = AsyncMock(return_value=copy.deepcopy(BASE_MOCK_DATA))
    return client

@pytest.mark.asyncio
async def test_async_update_data_orchestration(hass: HomeAssistant, mock_api_client):
    """Test that _async_update_data calls the API and filter methods."""
    # Arrange
    config_entry = MockConfigEntry(domain=DOMAIN, options={})
    coordinator = MerakiDataCoordinator(hass, mock_api_client, 60, config_entry)
    coordinator.api.get_all_data = AsyncMock(return_value=copy.deepcopy(BASE_MOCK_DATA))
    coordinator._filter_ignored_networks = MagicMock()
    coordinator._filter_unconfigured_ssids = MagicMock()

    # Act
    await coordinator._async_update_data()

    # Assert
    coordinator.api.get_all_data.assert_awaited_once()
    coordinator._filter_ignored_networks.assert_called_once()
    coordinator._filter_unconfigured_ssids.assert_called_once()


def test_ignored_networks_filter(hass: HomeAssistant, mock_api_client):
    """Test that networks are filtered based on the ignored_networks option."""
    # Arrange
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        options={
            CONF_IGNORED_NETWORKS: "Network To Ignore, Some Other Network",
        },
    )
    coordinator = MerakiDataCoordinator(hass, mock_api_client, 60, config_entry)
    data = copy.deepcopy(BASE_MOCK_DATA)

    # Act
    coordinator._filter_ignored_networks(data)

    # Assert
    assert len(data["networks"]) == 1
    assert data["networks"][0]["name"] == "Network To Keep"


def test_hide_unconfigured_ssids_filter(hass: HomeAssistant, mock_api_client):
    """Test that SSIDs are filtered when hide_unconfigured_ssids is true."""
    # Arrange
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        options={
            CONF_HIDE_UNCONFIGURED_SSIDS: True,
        },
    )
    coordinator = MerakiDataCoordinator(hass, mock_api_client, 60, config_entry)
    data = copy.deepcopy(BASE_MOCK_DATA)

    # Act
    coordinator._filter_unconfigured_ssids(data)

    # Assert
    assert len(data["ssids"]) == 1
    assert data["ssids"][0]["name"] == "Enabled SSID"


@pytest.mark.asyncio
async def test_stale_data_on_api_failure(hass: HomeAssistant, mock_api_client):
    """Test that stale data is returned if the API fails but the data is recent."""
    # Arrange
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        options={
            CONF_USE_STALE_DATA: True,
            CONF_STALE_DATA_THRESHOLD: 15,  # 15 minutes
        },
    )
    coordinator = MerakiDataCoordinator(hass, mock_api_client, 60, config_entry)

    # --- First, a successful run to populate the data ---
    await coordinator._async_update_data()
    assert coordinator.data["networks"][0]["name"] == "Network To Keep"
    assert coordinator.last_successful_update is not None

    # --- Now, simulate an API failure ---
    mock_api_client.get_all_data.side_effect = Exception("API has exploded")

    # Act: The API call fails, but the data is not yet stale
    stale_data = await coordinator._async_update_data()

    # Assert: The coordinator should return the old data and not raise UpdateFailed
    assert stale_data["networks"][0]["name"] == "Network To Keep"

    # --- Now, simulate time passing beyond the threshold ---
    # Manually set the last successful update time to be in the past
    coordinator.last_successful_update = datetime.now() - timedelta(minutes=20)

    # Act & Assert: This time, the failure should propagate
    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()
