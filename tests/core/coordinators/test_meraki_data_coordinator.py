"""Tests for the Meraki data coordinator."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_IGNORED_NETWORKS,
    CONF_HIDE_UNCONFIGURED_SSIDS,
)

MOCK_API_DATA = {
    "networks": [
        {"id": "N_1", "name": "Network To Keep"},
        {"id": "N_2", "name": "Network To Ignore"},
    ],
    "ssids": [
        {"id": "s_1", "name": "Enabled SSID", "enabled": True},
        {"id": "s_2", "name": "Disabled SSID", "enabled": False},
    ],
}

@pytest.mark.asyncio
async def test_ignored_networks_filter(hass: HomeAssistant):
    """Test that networks are filtered based on the ignored_networks option."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        options={
            CONF_IGNORED_NETWORKS: "Network To Ignore, Some Other Network",
        },
    )

    mock_api_client = MagicMock()
    mock_api_client.get_all_data = AsyncMock(return_value=MOCK_API_DATA)

    coordinator = MerakiDataCoordinator(hass, mock_api_client, 60, config_entry)

    data = await coordinator._async_update_data()

    assert len(data["networks"]) == 1
    assert data["networks"][0]["name"] == "Network To Keep"


@pytest.mark.asyncio
async def test_hide_unconfigured_ssids_filter(hass: HomeAssistant):
    """Test that SSIDs are filtered when hide_unconfigured_ssids is true."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        options={
            CONF_HIDE_UNCONFIGURED_SSIDS: True,
        },
    )

    mock_api_client = MagicMock()
    mock_api_client.get_all_data = AsyncMock(return_value=MOCK_API_DATA)

    coordinator = MerakiDataCoordinator(hass, mock_api_client, 60, config_entry)

    data = await coordinator._async_update_data()

    assert len(data["ssids"]) == 1
    assert data["ssids"][0]["name"] == "Enabled SSID"
