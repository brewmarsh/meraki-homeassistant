"""Tests for the Meraki content filtering switch."""

from unittest.mock import AsyncMock, patch

import pytest

from custom_components.meraki_ha.switch.content_filtering import (
    MerakiContentFilteringSwitch,
)


@pytest.fixture
def mock_coordinator():
    """Mock Meraki data coordinator."""
    coordinator = AsyncMock()
    coordinator.data = {
        "content_filtering": {
            "net_1": {
                "blockedUrlCategories": ["meraki:contentFiltering/category/2"],
            }
        }
    }
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Mock config entry."""
    return AsyncMock()


def test_switch_creation(mock_coordinator, mock_config_entry):
    """Test the creation of the content filtering switch."""
    network = {"id": "net_1", "name": "Test Network"}
    category = {"id": "meraki:contentFiltering/category/1", "name": "Social Media"}
    switch = MerakiContentFilteringSwitch(
        mock_coordinator, mock_config_entry, network, category
    )
    assert (
        switch.unique_id
        == "meraki-content-filtering-net_1-meraki:contentFiltering/category/1"
    )
    assert switch.name == "Block Social Media"


def test_is_on(mock_coordinator, mock_config_entry):
    """Test the is_on property."""
    network = {"id": "net_1", "name": "Test Network"}
    category_on = {"id": "meraki:contentFiltering/category/2", "name": "Gambling"}
    category_off = {"id": "meraki:contentFiltering/category/1", "name": "Social Media"}

    switch_on = MerakiContentFilteringSwitch(
        mock_coordinator, mock_config_entry, network, category_on
    )
    switch_off = MerakiContentFilteringSwitch(
        mock_coordinator, mock_config_entry, network, category_off
    )

    assert switch_on.is_on is True
    assert switch_off.is_on is False


async def test_turn_on(mock_coordinator, mock_config_entry):
    """Test turning the switch on."""
    network = {"id": "net_1", "name": "Test Network"}
    category = {"id": "meraki:contentFiltering/category/1", "name": "Social Media"}
    switch = MerakiContentFilteringSwitch(
        mock_coordinator, mock_config_entry, network, category
    )

    with (
        patch.object(
            switch._client.appliance,
            "get_network_appliance_content_filtering",
            return_value={
                "blockedUrlCategories": ["meraki:contentFiltering/category/2"]
            },
        ) as mock_get,
        patch.object(
            switch._client.appliance, "update_network_appliance_content_filtering"
        ) as mock_update,
    ):
        await switch.async_turn_on()
        mock_get.assert_called_once_with("net_1")
        mock_update.assert_called_once_with(
            "net_1",
            blockedUrlCategories=[
                "meraki:contentFiltering/category/2",
                "meraki:contentFiltering/category/1",
            ],
        )
        mock_coordinator.async_request_refresh.assert_called_once()


async def test_turn_off(mock_coordinator, mock_config_entry):
    """Test turning the switch off."""
    network = {"id": "net_1", "name": "Test Network"}
    category = {"id": "meraki:contentFiltering/category/2", "name": "Gambling"}
    switch = MerakiContentFilteringSwitch(
        mock_coordinator, mock_config_entry, network, category
    )

    with (
        patch.object(
            switch._client.appliance,
            "get_network_appliance_content_filtering",
            return_value={
                "blockedUrlCategories": ["meraki:contentFiltering/category/2"]
            },
        ) as mock_get,
        patch.object(
            switch._client.appliance, "update_network_appliance_content_filtering"
        ) as mock_update,
    ):
        await switch.async_turn_off()
        mock_get.assert_called_once_with("net_1")
        mock_update.assert_called_once_with(
            "net_1",
            blockedUrlCategories=[],
        )
        mock_coordinator.async_request_refresh.assert_called_once()
