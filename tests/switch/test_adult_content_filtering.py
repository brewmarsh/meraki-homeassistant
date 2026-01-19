"""Tests for the Meraki adult content filtering switch."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.switch.adult_content_filtering import (
    MerakiAdultContentFilteringSwitch,
)


@pytest.fixture
def mock_coordinator_with_ssid_filtering(mock_coordinator: MagicMock) -> MagicMock:
<<<<<<< HEAD
    """Fixture for a mocked MerakiDataUpdateCoordinator with SSID filtering data."""
=======
    """Fixture for a mocked MerakiDataCoordinator with SSID filtering data."""
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    mock_coordinator.get_ssid.return_value = {"adultContentFilteringEnabled": True}
    mock_coordinator.api.wireless.update_network_wireless_ssid = AsyncMock()
    mock_coordinator.async_request_refresh = AsyncMock()
    return mock_coordinator


def test_switch_creation(
    mock_coordinator_with_ssid_filtering: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test the creation of the adult content filtering switch."""
    ssid = {"networkId": "net_1", "number": 0, "name": "Test SSID"}
    switch = MerakiAdultContentFilteringSwitch(
        mock_coordinator_with_ssid_filtering, mock_config_entry, ssid
    )
    assert switch.unique_id == "meraki-adult-content-filtering-net_1-0"
    assert switch.name == "Adult Content Filtering on Test SSID"


def test_is_on(
    mock_coordinator_with_ssid_filtering: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test the is_on property."""
    ssid = {"networkId": "net_1", "number": 0, "name": "Test SSID"}
    switch = MerakiAdultContentFilteringSwitch(
        mock_coordinator_with_ssid_filtering, mock_config_entry, ssid
    )
    assert switch.is_on is True

    # Test with filtering disabled
    mock_coordinator_with_ssid_filtering.get_ssid.return_value = {
        "adultContentFilteringEnabled": False
    }
    switch_off = MerakiAdultContentFilteringSwitch(
        mock_coordinator_with_ssid_filtering, mock_config_entry, ssid
    )
    assert switch_off.is_on is False


async def test_turn_on(
    mock_coordinator_with_ssid_filtering: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test turning the switch on."""
    ssid = {"networkId": "net_1", "number": 0, "name": "Test SSID"}
    switch = MerakiAdultContentFilteringSwitch(
        mock_coordinator_with_ssid_filtering, mock_config_entry, ssid
    )

    await switch.async_turn_on()
    switch._client.wireless.update_network_wireless_ssid.assert_called_once_with(  # type: ignore[attr-defined]
        network_id="net_1",
        number=0,
        adultContentFilteringEnabled=True,
    )
    mock_coordinator_with_ssid_filtering.async_request_refresh.assert_called_once()


async def test_turn_off(
    mock_coordinator_with_ssid_filtering: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test turning the switch off."""
    ssid = {"networkId": "net_1", "number": 0, "name": "Test SSID"}
    switch = MerakiAdultContentFilteringSwitch(
        mock_coordinator_with_ssid_filtering, mock_config_entry, ssid
    )

    await switch.async_turn_off()
    switch._client.wireless.update_network_wireless_ssid.assert_called_once_with(  # type: ignore[attr-defined]
        network_id="net_1",
        number=0,
        adultContentFilteringEnabled=False,
    )
    mock_coordinator_with_ssid_filtering.async_request_refresh.assert_called_once()
