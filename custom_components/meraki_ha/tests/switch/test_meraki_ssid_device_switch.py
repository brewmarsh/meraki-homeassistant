# custom_components/meraki_ha/tests/switch/test_meraki_ssid_device_switch.py
"""Tests for the Meraki SSID device switch entities."""

from unittest.mock import AsyncMock, patch, MagicMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.meraki_ha.const import DOMAIN, DATA_CLIENT
from custom_components.meraki_ha.switch.meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
    async_setup_entry,
)
from custom_components.meraki_ha.coordinators.ssid_device_coordinator import (
    SSIDDeviceCoordinator,
)
from custom_components.meraki_ha.meraki_api import MerakiAPIClient

# Sample SSID data for testing
MOCK_SSID_UNIQUE_ID_1 = f"{DOMAIN}_net1_ssid_0"
MOCK_SSID_DATA_1_ENABLED = {
    "networkId": "net1",
    "number": 0,
    "name": "Test SSID 1",
    "enabled": True,
    "visible": True,
    "authMode": "psk",
    "psk": "password123",
    "unique_id": MOCK_SSID_UNIQUE_ID_1,
}
MOCK_SSID_DATA_1_DISABLED = {
    **MOCK_SSID_DATA_1_ENABLED,
    "enabled": False,
}

MOCK_SSID_UNIQUE_ID_2 = f"{DOMAIN}_net2_ssid_1"
MOCK_SSID_DATA_2_HIDDEN = {
    "networkId": "net2",
    "number": 1,
    "name": "Test SSID 2",
    "enabled": True,
    "visible": False,
    "authMode": "open",
    "unique_id": MOCK_SSID_UNIQUE_ID_2,
}


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock(spec=MerakiAPIClient)
    client.wireless = AsyncMock()
    # Corrected: updateNetworkWirelessSsid is the method name used in the switch code
    client.wireless.updateNetworkWirelessSsid = AsyncMock()
    return client


@pytest.fixture
def mock_ssid_coordinator() -> MagicMock:
    """Fixture for a mocked SSIDDeviceCoordinator."""
    coordinator = MagicMock(spec=SSIDDeviceCoordinator)
    coordinator.data = {
        MOCK_SSID_UNIQUE_ID_1: MOCK_SSID_DATA_1_ENABLED,
        MOCK_SSID_UNIQUE_ID_2: MOCK_SSID_DATA_2_HIDDEN,
    }
    # Mock add_listener and remove_listener which are part of DataUpdateCoordinator
    coordinator.async_add_listener = MagicMock()
    coordinator.async_remove_listener = MagicMock()
    coordinator.async_request_refresh = (
        AsyncMock()
    )  # Added missing mock for request_refresh
    return coordinator


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = "test_entry_id"
    entry.unique_id = "test_unique_id"  # For SSIDDeviceCoordinator name
    return entry


async def test_ssid_enabled_switch_state_and_turn_on_off(
    hass: HomeAssistant,
    mock_meraki_client: MagicMock,
    mock_ssid_coordinator: MagicMock,
    mock_config_entry: MagicMock,
):
    """Test the state and turn_on/turn_off methods of MerakiSSIDEnabledSwitch."""

    # Test with initially enabled SSID
    switch_enabled = MerakiSSIDEnabledSwitch(
        coordinator=mock_ssid_coordinator,
        meraki_client=mock_meraki_client,
        config_entry=mock_config_entry,
        ssid_unique_id=MOCK_SSID_UNIQUE_ID_1,
        ssid_data=MOCK_SSID_DATA_1_ENABLED,
    )
    switch_enabled.hass = hass  # Assign hass instance if needed by the entity
    # Manually call _handle_coordinator_update to set initial state from coordinator.data
    # This is because the entity is not added to an actual platform that would do this.
    switch_enabled._handle_coordinator_update()

    assert switch_enabled.unique_id == f"{MOCK_SSID_UNIQUE_ID_1}_enabled_switch"
    assert switch_enabled.name == "Test SSID 1 Enabled Control"
    assert switch_enabled.is_on is True
    assert switch_enabled.device_info["identifiers"] == {
        (DOMAIN, MOCK_SSID_UNIQUE_ID_1)
    }

    # Test turning off
    await switch_enabled.async_turn_off()
    mock_meraki_client.wireless.updateNetworkWirelessSsid.assert_called_once_with(
        networkId="net1",
        number=0,
        enabled=False,
    )
    mock_ssid_coordinator.async_request_refresh.assert_called_once()

    # Reset mocks and update coordinator data to reflect change
    mock_meraki_client.wireless.updateNetworkWirelessSsid.reset_mock()
    mock_ssid_coordinator.async_request_refresh.reset_mock()

    # Simulate coordinator updating its data
    mock_ssid_coordinator.data = {
        **mock_ssid_coordinator.data,  # Keep other SSIDs
        MOCK_SSID_UNIQUE_ID_1: MOCK_SSID_DATA_1_DISABLED,
    }

    # Manually trigger coordinator update for the switch
    # In a real scenario, the coordinator would call the update callback.
    switch_enabled._handle_coordinator_update()

    assert switch_enabled.is_on is False

    # Test turning on
    await switch_enabled.async_turn_on()
    mock_meraki_client.wireless.updateNetworkWirelessSsid.assert_called_once_with(
        networkId="net1",
        number=0,
        enabled=True,
    )
    mock_ssid_coordinator.async_request_refresh.assert_called_once()


async def test_async_setup_entry_switches(
    hass: HomeAssistant,
    mock_meraki_client: MagicMock,
    mock_ssid_coordinator: MagicMock,
    mock_config_entry: MagicMock,
):
    """Test async_setup_entry for Meraki SSID switches."""
    hass.data = {
        DOMAIN: {
            mock_config_entry.entry_id: {
                "coordinators": {"ssid_devices": mock_ssid_coordinator},
                DATA_CLIENT: mock_meraki_client,
            }
        }
    }

    async_add_entities_mock = AsyncMock()

    await async_setup_entry(hass, mock_config_entry, async_add_entities_mock)

    # Expected 2 switches per SSID (enabled + broadcast)
    # We have 2 mock SSIDs
    assert async_add_entities_mock.call_count == 1
    entities_added = async_add_entities_mock.call_args[0][0]
    assert len(entities_added) == 4

    assert isinstance(entities_added[0], MerakiSSIDEnabledSwitch)
    assert entities_added[0].unique_id == f"{MOCK_SSID_UNIQUE_ID_1}_enabled_switch"
    assert isinstance(entities_added[1], MerakiSSIDBroadcastSwitch)
    assert entities_added[1].unique_id == f"{MOCK_SSID_UNIQUE_ID_1}_broadcast_switch"
    assert isinstance(entities_added[2], MerakiSSIDEnabledSwitch)
    assert entities_added[2].unique_id == f"{MOCK_SSID_UNIQUE_ID_2}_enabled_switch"
    assert isinstance(entities_added[3], MerakiSSIDBroadcastSwitch)
    assert entities_added[3].unique_id == f"{MOCK_SSID_UNIQUE_ID_2}_broadcast_switch"


# TODO: Add similar test for MerakiSSIDBroadcastSwitch
# TODO: Add test for when coordinator has no data during setup
# TODO: Add test for entity name updates if SSID name changes in coordinator
# TODO: Test _update_internal_state more directly, especially missing data scenarios
# TODO: Test error handling in API calls within turn_on/turn_off
