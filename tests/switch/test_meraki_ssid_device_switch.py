"""Tests for the Meraki SSID device switch."""

import pytest
from unittest.mock import MagicMock, AsyncMock

from custom_components.meraki_ha.switch.meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiNetworkCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "ssid_0": {
            "number": 0,
            "name": "Test SSID",
            "enabled": True,
            "broadcast": True,
            "networkId": "net-123",
            "unique_id": "ssid_0",
            "productType": "ssid",
        }
    }
    return coordinator


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.update_network_wireless_ssid = AsyncMock()
    return client


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry


async def test_meraki_ssid_enabled_switch(
    mock_coordinator, mock_meraki_client, mock_config_entry
) -> None:
    """Test the Meraki SSID enabled switch."""
    ssid_data = mock_coordinator.data["ssid_0"]
    switch = MerakiSSIDEnabledSwitch(
        mock_coordinator, mock_meraki_client, mock_config_entry, "ssid_0", ssid_data
    )
    switch._update_internal_state()
    assert switch.is_on is True
    assert switch.name == "Test SSID Enabled Control"

    await switch.async_turn_off()
    mock_meraki_client.update_network_wireless_ssid.assert_called_with(
        network_id="net-123", number=0, enabled=False
    )


async def test_meraki_ssid_broadcast_switch(
    mock_coordinator, mock_meraki_client, mock_config_entry
) -> None:
    """Test the Meraki SSID broadcast switch."""
    ssid_data = mock_coordinator.data["ssid_0"]
    switch = MerakiSSIDBroadcastSwitch(
        mock_coordinator, mock_meraki_client, mock_config_entry, "ssid_0", ssid_data
    )
    switch._update_internal_state()
    assert switch.is_on is True
    assert switch.name == "Test SSID Broadcast Control"

    await switch.async_turn_off()
    mock_meraki_client.update_network_wireless_ssid.assert_called_with(
        network_id="net-123", number=0, broadcast=False
    )
