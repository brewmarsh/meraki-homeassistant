"""Tests for the Meraki adult content filtering switch."""

from unittest.mock import AsyncMock, patch

import pytest

from custom_components.meraki_ha.switch.adult_content_filtering import (
    MerakiAdultContentFilteringSwitch,
)


@pytest.fixture
def mock_coordinator():
    """Mock Meraki data coordinator."""
    coordinator = AsyncMock()
    coordinator.get_ssid.return_value = {"adultContentFilteringEnabled": True}
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Mock config entry."""
    return AsyncMock()


def test_switch_creation(mock_coordinator, mock_config_entry):
    """Test the creation of the adult content filtering switch."""
    ssid = {"networkId": "net_1", "number": 0, "name": "Test SSID"}
    switch = MerakiAdultContentFilteringSwitch(
        mock_coordinator, mock_config_entry, ssid
    )
    assert switch.unique_id == "meraki-adult-content-filtering-net_1-0"
    assert switch.name == "Adult Content Filtering on Test SSID"


def test_is_on(mock_coordinator, mock_config_entry):
    """Test the is_on property."""
    ssid = {"networkId": "net_1", "number": 0, "name": "Test SSID"}
    switch = MerakiAdultContentFilteringSwitch(
        mock_coordinator, mock_config_entry, ssid
    )
    assert switch.is_on is True

    # Test with filtering disabled
    mock_coordinator.get_ssid.return_value = {"adultContentFilteringEnabled": False}
    switch_off = MerakiAdultContentFilteringSwitch(
        mock_coordinator, mock_config_entry, ssid
    )
    assert switch_off.is_on is False


async def test_turn_on(mock_coordinator, mock_config_entry):
    """Test turning the switch on."""
    ssid = {"networkId": "net_1", "number": 0, "name": "Test SSID"}
    switch = MerakiAdultContentFilteringSwitch(
        mock_coordinator, mock_config_entry, ssid
    )

    with patch.object(
        switch._client.wireless, "update_network_wireless_ssid"
    ) as mock_update:
        await switch.async_turn_on()
        mock_update.assert_called_once_with(
            networkId="net_1",
            number=0,
            adultContentFilteringEnabled=True,
        )
        mock_coordinator.async_request_refresh.assert_called_once()


async def test_turn_off(mock_coordinator, mock_config_entry):
    """Test turning the switch off."""
    ssid = {"networkId": "net_1", "number": 0, "name": "Test SSID"}
    switch = MerakiAdultContentFilteringSwitch(
        mock_coordinator, mock_config_entry, ssid
    )

    with patch.object(
        switch._client.wireless, "update_network_wireless_ssid"
    ) as mock_update:
        await switch.async_turn_off()
        mock_update.assert_called_once_with(
            networkId="net_1",
            number=0,
            adultContentFilteringEnabled=False,
        )
        mock_coordinator.async_request_refresh.assert_called_once()
