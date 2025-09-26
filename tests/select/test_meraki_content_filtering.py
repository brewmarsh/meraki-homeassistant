"""Tests for the Meraki Content Filtering select entity."""

from unittest.mock import AsyncMock, MagicMock, PropertyMock

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.meraki_ha.select.meraki_content_filtering import (
    MerakiContentFilteringSelect,
    FILTERING_OPTIONS,
)
from custom_components.meraki_ha.core.coordinators.ssid_firewall_coordinator import (
    SsidFirewallCoordinator,
)

MOCK_SSID = {
    "number": 0,
    "name": "Test SSID",
    "enabled": True,
    "networkId": "N_12345",
}


@pytest.fixture
def mock_coordinator():
    """Mock the SsidFirewallCoordinator."""
    coordinator = MagicMock(spec=SsidFirewallCoordinator)
    coordinator.async_update_content_filtering = AsyncMock()
    type(coordinator).data = PropertyMock(return_value={"settings": {"enabled": False}})
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Mock the ConfigEntry."""
    return MockConfigEntry(domain="meraki_ha", entry_id="test_entry")


def test_initial_state_disabled(mock_coordinator, mock_config_entry):
    """Test the initial state when content filtering is disabled."""
    select = MerakiContentFilteringSelect(
        firewall_coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        ssid_data=MOCK_SSID,
    )
    assert select.current_option == FILTERING_OPTIONS["Disabled"]["name"]


def test_initial_state_topsites(mock_coordinator, mock_config_entry):
    """Test the initial state when 'Top Sites' is the policy."""
    type(mock_coordinator).data = PropertyMock(
        return_value={"settings": {"enabled": True, "blockedUrlCategories": ["Top Sites"]}}
    )
    select = MerakiContentFilteringSelect(
        firewall_coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        ssid_data=MOCK_SSID,
    )
    assert select.current_option == FILTERING_OPTIONS["Top Sites"]["name"]


async def test_select_option(mock_coordinator, mock_config_entry):
    """Test selecting a new content filtering option."""
    select = MerakiContentFilteringSelect(
        firewall_coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        ssid_data=MOCK_SSID,
    )
    select.async_write_ha_state = MagicMock()

    await select.async_select_option(FILTERING_OPTIONS["Strict"]["name"])

    mock_coordinator.async_update_content_filtering.assert_called_once_with(
        FILTERING_OPTIONS["Strict"]["id"]
    )
    assert select.current_option == FILTERING_OPTIONS["Strict"]["name"]


def test_state_updates_on_coordinator_update(mock_coordinator, mock_config_entry):
    """Test that the select state updates when the coordinator data changes."""
    select = MerakiContentFilteringSelect(
        firewall_coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        ssid_data=MOCK_SSID,
    )
    select.async_write_ha_state = MagicMock()
    assert select.current_option == FILTERING_OPTIONS["Disabled"]["name"]

    # Simulate coordinator update with 'Normal' policy
    type(mock_coordinator).data = PropertyMock(
        return_value={"settings": {"enabled": True, "blockedUrlCategories": ["Normal"]}}
    )
    select._handle_coordinator_update()

    assert select.current_option == FILTERING_OPTIONS["Normal"]["name"]

    # Simulate coordinator update with filtering disabled
    type(mock_coordinator).data = PropertyMock(
        return_value={"settings": {"enabled": False}}
    )
    select._handle_coordinator_update()

    assert select.current_option == FILTERING_OPTIONS["Disabled"]["name"]