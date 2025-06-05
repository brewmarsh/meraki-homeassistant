# /config/custom_components/meraki_ha/tests/sensor/test_network_clients.py
"""Tests for the Meraki Network Clients sensor."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

# Import the sensor class we want to test
from custom_components.meraki_ha.sensor.network_clients import (
    MerakiNetworkClientsSensor,
)

# Constants for testing
TEST_NETWORK_ID = "N_123456789012345678"
TEST_NETWORK_NAME = "My Test Network"

# Mock MerakiAPIClient for tests
# We don't need to define a class MockMerakiAPIClient,
# MagicMock can be used directly for the instance.
# However, if MerakiAPIClient is type hinted in the sensor,
# it might be better to mock the actual class if available for import.
# For this test, we'll directly mock the instance passed to the sensor.


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock DataUpdateCoordinator."""
    coordinator = MagicMock(spec=DataUpdateCoordinator)
    coordinator.data = {}
    coordinator.async_request_refresh = AsyncMock()
    return coordinator

@pytest.fixture
def mock_api_client():
    """Fixture for a mock MerakiAPIClient.
    This mock represents an instance of the actual MerakiAPIClient.
    """
    client = MagicMock() # Can be spec'd with the actual class if imported: spec=MerakiAPIClient
    client.networks = MagicMock()
    client.networks.getNetworkClients = AsyncMock()
    return client

async def test_network_clients_sensor_setup_and_initial_state(
    hass: HomeAssistant, mock_coordinator, mock_api_client
):
    """Test sensor setup and its initial state before any API data."""
    # Initial call during __init__ -> _update_sensor_state uses empty _clients_data
    # async_update is not called yet here by HA, so getNetworkClients shouldn't be called yet
    # by the constructor's _update_sensor_state path.

    sensor = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        network_id=TEST_NETWORK_ID,
        network_name=TEST_NETWORK_NAME,
        meraki_api_client=mock_api_client,
    )
    sensor.hass = hass # Simulate adding to HASS

    assert sensor.name == f"{TEST_NETWORK_NAME} Clients"
    assert sensor.unique_id == f"meraki_network_clients_{TEST_NETWORK_ID}"
    assert sensor.native_value == 0 # Initial state from empty _clients_data
    assert sensor.icon == "mdi:account-multiple"
    assert sensor.native_unit_of_measurement == "clients"

    attributes = sensor.extra_state_attributes
    assert attributes is not None
    assert attributes["network_id"] == TEST_NETWORK_ID
    assert attributes["network_name"] == TEST_NETWORK_NAME
    assert attributes["clients_list"] == []

    # Ensure API was not called during init
    mock_api_client.networks.getNetworkClients.assert_not_called()


async def test_network_clients_sensor_update_success(
    hass: HomeAssistant, mock_coordinator, mock_api_client
):
    """Test sensor update with successful API data fetch."""
    mock_clients_response = [
        {
            "description": "Client 1", "mac": "00:11:22:33:44:51", "ip": "192.168.1.101",
            "vlan": 10, "status": "Online", "lastSeen": "2023-01-01T12:00:00Z",
            "manufacturer": "FakeManu", "os": "FakeOS", "user": "User1", "ssid": "TestSSID1"
        },
        {
            "description": "Client 2", "mac": "00:11:22:33:44:52", "ip": "192.168.1.102",
            "vlan": 20, "status": "Offline", "lastSeen": "2023-01-01T10:00:00Z",
            "manufacturer": "FakeManu", "os": "FakeOS", "user": "User2", "ssid": "TestSSID2"
        },
    ]
    mock_api_client.networks.getNetworkClients.return_value = mock_clients_response

    sensor = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        network_id=TEST_NETWORK_ID,
        network_name=TEST_NETWORK_NAME,
        meraki_api_client=mock_api_client,
    )
    sensor.hass = hass

    # Call async_update to trigger API fetch
    await sensor.async_update()

    assert sensor.native_value == 2
    attributes = sensor.extra_state_attributes
    assert attributes is not None
    assert len(attributes["clients_list"]) == 2

    client_attr_1 = attributes["clients_list"][0]
    assert client_attr_1["description"] == "Client 1"
    assert client_attr_1["mac"] == "00:11:22:33:44:51"
    assert client_attr_1["ip"] == "192.168.1.101"
    assert client_attr_1["vlan"] == 10
    assert client_attr_1["status"] == "Online"
    assert client_attr_1["last_seen"] == "2023-01-01T12:00:00Z"
    assert client_attr_1["manufacturer"] == "FakeManu"
    assert client_attr_1["os"] == "FakeOS"
    assert client_attr_1["user"] == "User1"
    assert client_attr_1["ssid"] == "TestSSID1"

    mock_api_client.networks.getNetworkClients.assert_called_once_with(networkId=TEST_NETWORK_ID)

async def test_network_clients_sensor_api_error(
    hass: HomeAssistant, mock_coordinator, mock_api_client
):
    """Test sensor update when API fetch fails."""
    mock_api_client.networks.getNetworkClients.side_effect = Exception("API Call Failed")

    sensor = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        network_id=TEST_NETWORK_ID,
        network_name=TEST_NETWORK_NAME,
        meraki_api_client=mock_api_client,
    )
    sensor.hass = hass

    # Call async_update to trigger API fetch
    await sensor.async_update()

    # State should remain at initial (or last known good if that were the case)
    # For a fresh sensor where first update fails, it should be 0 / empty.
    assert sensor.native_value == 0
    attributes = sensor.extra_state_attributes
    assert attributes is not None
    assert attributes["clients_list"] == []

    mock_api_client.networks.getNetworkClients.assert_called_once_with(networkId=TEST_NETWORK_ID)

async def test_network_clients_sensor_empty_response(
    hass: HomeAssistant, mock_coordinator, mock_api_client
):
    """Test sensor update with an empty list response from API (no clients)."""
    mock_api_client.networks.getNetworkClients.return_value = [] # API returns empty list

    sensor = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        network_id=TEST_NETWORK_ID,
        network_name=TEST_NETWORK_NAME,
        meraki_api_client=mock_api_client,
    )
    sensor.hass = hass

    # Call async_update to trigger API fetch
    await sensor.async_update()

    assert sensor.native_value == 0
    attributes = sensor.extra_state_attributes
    assert attributes is not None
    assert attributes["clients_list"] == []

    mock_api_client.networks.getNetworkClients.assert_called_once_with(networkId=TEST_NETWORK_ID)

async def test_network_clients_sensor_coordinator_update(
    hass: HomeAssistant, mock_coordinator, mock_api_client
):
    """Test sensor state update via coordinator _handle_coordinator_update."""
    # Initial state
    sensor = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        network_id=TEST_NETWORK_ID,
        network_name=TEST_NETWORK_NAME,
        meraki_api_client=mock_api_client,
    )
    sensor.hass = hass
    sensor.async_write_ha_state = MagicMock() # Mock this method

    # Assume async_update has run once and populated _clients_data
    initial_clients_data = [{"mac": "aa:bb:cc:dd:ee:ff", "description": "Initial Client"}]
    sensor._clients_data = initial_clients_data
    sensor._update_sensor_state() # Manually update state based on this internal data

    assert sensor.native_value == 1
    sensor.async_write_ha_state.assert_not_called() # _update_sensor_state doesn't call it directly

    # Simulate coordinator update
    # The current _handle_coordinator_update calls _update_sensor_state and async_write_ha_state
    # _update_sensor_state will use the existing sensor._clients_data
    sensor._handle_coordinator_update()

    # Value should be the same as _clients_data hasn't changed by _handle_coordinator_update itself
    assert sensor.native_value == 1
    # Check that async_write_ha_state was called by _handle_coordinator_update
    sensor.async_write_ha_state.assert_called_once()

    # Verify that _fetch_clients_data (and thus API call) was NOT made by _handle_coordinator_update
    mock_api_client.networks.getNetworkClients.assert_not_called()
```
