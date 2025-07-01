# /config/custom_components/meraki-ha/tests/sensor/test_network_clients.py
"""Tests for the Meraki Network Clients sensor."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

# Import the sensor class we want to test
from custom_components.meraki_ha.sensor.network_clients import (
    MerakiNetworkClientsSensor,
)
# Import the coordinator and API client for proper mocking
from custom_components.meraki_ha.coordinators import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.meraki_api import MerakiAPIClient


# Constants for testing
TEST_NETWORK_ID = "N_123456789012345678"
TEST_NETWORK_NAME = "My Test Network"


@pytest.fixture
def mock_coordinator(hass: HomeAssistant, mock_api_client: MagicMock): # Add hass and typed mock_api_client
    """Fixture for a mock MerakiDataUpdateCoordinator."""
    # Spec with the actual coordinator class used by the sensor
    coordinator = MagicMock(spec=MerakiDataUpdateCoordinator)
    # Initialize common attributes HA might expect or the entity might use
    coordinator.hass = hass
    coordinator.data = {} # Default to empty data
    coordinator.meraki_client = mock_api_client # Attach mocked API client if coordinator uses it
    coordinator.last_update_success = True
    coordinator.async_request_refresh = AsyncMock()
    # Ensure listeners attribute exists, as DataUpdateCoordinator has it
    coordinator._listeners = {} # Simplified mock for listeners
    return coordinator

@pytest.fixture
def mock_api_client():
    """Fixture for a mock MerakiAPIClient."""
    client = MagicMock(spec=MerakiAPIClient) # Spec with actual class
    client.networks = MagicMock()
    # Define the return value structure for getNetworkClients
    client.networks.getNetworkClients = AsyncMock(return_value=[]) # Default to empty list
    return client

async def test_network_clients_sensor_setup_and_initial_state(
    hass: HomeAssistant, mock_coordinator: MerakiDataUpdateCoordinator, mock_api_client: MagicMock
):
    """Test sensor setup and its initial state before any API data."""
    sensor = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        network_id=TEST_NETWORK_ID,
        network_name=TEST_NETWORK_NAME,
        meraki_api_client=mock_api_client, # Pass the MagicMock instance
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

    # API should not be called during init because _clients_data is empty
    # and _update_sensor_state is called before any async_update.
    mock_api_client.networks.getNetworkClients.assert_not_called()


async def test_network_clients_sensor_update_success(
    hass: HomeAssistant, mock_coordinator: MerakiDataUpdateCoordinator, mock_api_client: MagicMock
):
    """Test sensor update with successful API data fetch."""
    mock_clients_response = [
        { # Full data from API
            "description": "Client 1", "mac": "00:11:22:33:44:51", "ip": "192.168.1.101",
            "vlan": 10, "status": "Online", "lastSeen": "2023-01-01T12:00:00Z",
            "manufacturer": "FakeManu", "os": "FakeOS", "user": "User1", "ssid": "TestSSID1",
            "ip6": "2001:db8::1"
        },
        {
            "description": "Client 2", "mac": "00:11:22:33:44:52", "ip": "192.168.1.102",
            "vlan": 20, "status": "Offline", "lastSeen": "2023-01-01T10:00:00Z",
            "manufacturer": "FakeManu", "os": "FakeOS", "user": "User2", "ssid": "TestSSID2",
            "ip6": None
        },
    ]
    mock_api_client.networks.getNetworkClients.return_value = mock_clients_response

    sensor = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        network_id=TEST_NETWORK_ID,
        network_name=TEST_NETWORK_NAME,
        meraki_api_client=mock_api_client, # Pass the MagicMock instance
    )
    sensor.hass = hass

    await sensor.async_update()

    assert sensor.native_value == 2
    attributes = sensor.extra_state_attributes
    assert attributes is not None
    assert len(attributes["clients_list"]) == 2

    # Verify only the reduced set of fields is present
    client_attr_1 = attributes["clients_list"][0]
    assert client_attr_1 == {
        "mac": "00:11:22:33:44:51",
        "description": "Client 1",
        "ip": "192.168.1.101",
        "status": "Online",
    }
    # Check that other fields are NOT present
    assert "vlan" not in client_attr_1
    assert "lastSeen" not in client_attr_1
    assert "manufacturer" not in client_attr_1
    assert "os" not in client_attr_1
    assert "user" not in client_attr_1
    assert "ssid" not in client_attr_1
    assert "ip6" not in client_attr_1

    client_attr_2 = attributes["clients_list"][1]
    assert client_attr_2 == {
        "mac": "00:11:22:33:44:52",
        "description": "Client 2",
        "ip": "192.168.1.102",
        "status": "Offline",
    }

    mock_api_client.networks.getNetworkClients.assert_called_once_with(
        networkId=TEST_NETWORK_ID, timespan=86400, perPage=1000
    )

async def test_network_clients_sensor_api_error(
    hass: HomeAssistant, mock_coordinator: MerakiDataUpdateCoordinator, mock_api_client: MagicMock
):
    """Test sensor update when API fetch fails."""
    mock_api_client.networks.getNetworkClients.side_effect = Exception("API Call Failed")

    sensor = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        network_id=TEST_NETWORK_ID,
        network_name=TEST_NETWORK_NAME,
        meraki_api_client=mock_api_client, # Pass the MagicMock instance
    )
    sensor.hass = hass

    await sensor.async_update()

    assert sensor.native_value == 0
    attributes = sensor.extra_state_attributes
    assert attributes is not None
    assert attributes["clients_list"] == []

    mock_api_client.networks.getNetworkClients.assert_called_once_with(
        networkId=TEST_NETWORK_ID, timespan=86400, perPage=1000
    )

async def test_network_clients_sensor_empty_response(
    hass: HomeAssistant, mock_coordinator: MerakiDataUpdateCoordinator, mock_api_client: MagicMock
):
    """Test sensor update with an empty list response from API (no clients)."""
    mock_api_client.networks.getNetworkClients.return_value = []

    sensor = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        network_id=TEST_NETWORK_ID,
        network_name=TEST_NETWORK_NAME,
        meraki_api_client=mock_api_client, # Pass the MagicMock instance
    )
    sensor.hass = hass

    await sensor.async_update()

    assert sensor.native_value == 0
    attributes = sensor.extra_state_attributes
    assert attributes is not None
    assert attributes["clients_list"] == []

    mock_api_client.networks.getNetworkClients.assert_called_once_with(
        networkId=TEST_NETWORK_ID, timespan=86400, perPage=1000
    )

async def test_network_clients_sensor_coordinator_update(
    hass: HomeAssistant, mock_coordinator: MerakiDataUpdateCoordinator, mock_api_client: MagicMock
):
    """Test sensor state update via coordinator _handle_coordinator_update."""
    sensor = MerakiNetworkClientsSensor(
        coordinator=mock_coordinator,
        network_id=TEST_NETWORK_ID,
        network_name=TEST_NETWORK_NAME,
        meraki_api_client=mock_api_client, # Pass the MagicMock instance
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
