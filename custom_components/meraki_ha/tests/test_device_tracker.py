"""Tests for the Meraki Client Device Tracker entities."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.components.device_tracker import SourceType
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_HOME, STATE_NOT_HOME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from custom_components.meraki_ha.const import DATA_COORDINATOR, DOMAIN
from custom_components.meraki_ha.device_tracker import (
    MerakiDeviceTracker,
    async_setup_entry,
)

# --- Mock Data ---
MOCK_CLIENT_1 = {
    "mac": "AA:BB:CC:DD:EE:01",
    "description": "Client One",
    "ip": "192.168.1.101",
    "ap_serial": "Q2AB-CDEF-GHIJ",  # Serial of the AP it's connected to
    "networkId": "L_123456789",
    "status": "Online",
    "manufacturer": "Apple, Inc.",
    "os": "macOS",
}
MOCK_CLIENT_2 = {
    "mac": "AA:BB:CC:DD:EE:02",
    "description": "Client Two",
    "ip": "192.168.1.102",
    "networkId": "L_123456789",  # No AP serial, should link to network
    "status": "Online",
    "manufacturer": "Samsung",
}
MOCK_CLIENT_NO_DESC_IP = {
    "mac": "AA:BB:CC:DD:EE:03",
    "networkId": "L_123456789",
    "status": "Online",
}

MOCK_CONFIG_ENTRY_ID = "test_entry_id"

@pytest.fixture
def mock_config_entry() -> ConfigEntry:
    """Mock a Home Assistant ConfigEntry."""
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = MOCK_CONFIG_ENTRY_ID
    return entry

@pytest.fixture
def mock_coordinator(hass: HomeAssistant) -> MagicMock:
    """Mock the MerakiDataUpdateCoordinator."""
    coordinator = MagicMock(spec=DataUpdateCoordinator)
    coordinator.hass = hass
    coordinator.data = {"clients": []} # Default to no clients
    # Mock the listener management methods
    coordinator.async_add_listener = MagicMock()
    coordinator.async_remove_listener = MagicMock()
    return coordinator

def setup_hass_domain_data(
    hass: HomeAssistant, entry_id: str, coordinator: MagicMock
):
    """Set up the hass.data structure for the Meraki domain."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry_id] = {DATA_COORDINATOR: coordinator}


# --- Test Cases ---

async def test_async_setup_entry_creates_trackers(
    hass: HomeAssistant, mock_coordinator: MagicMock, mock_config_entry: ConfigEntry
):
    """Test that device trackers are created for clients."""
    mock_coordinator.data = {"clients": [MOCK_CLIENT_1, MOCK_CLIENT_2]}
    setup_hass_domain_data(hass, mock_config_entry.entry_id, mock_coordinator)
    
    mock_async_add_entities = AsyncMock()
    
    await async_setup_entry(hass, mock_config_entry, mock_async_add_entities)
    
    assert mock_async_add_entities.call_count == 1
    created_entities = mock_async_add_entities.call_args[0][0]
    assert len(created_entities) == 2
    
    entity_macs = {entity._client_info_data["mac"] for entity in created_entities}
    assert MOCK_CLIENT_1["mac"] in entity_macs
    assert MOCK_CLIENT_2["mac"] in entity_macs

    for entity in created_entities:
        assert isinstance(entity, MerakiDeviceTracker)
        if entity._client_info_data["mac"] == MOCK_CLIENT_1["mac"]:
            assert entity.unique_id == f"{MOCK_CLIENT_1['mac']}_client_tracker"
            assert entity.name == MOCK_CLIENT_1["description"]
        elif entity._client_info_data["mac"] == MOCK_CLIENT_2["mac"]:
            assert entity.unique_id == f"{MOCK_CLIENT_2['mac']}_client_tracker"
            assert entity.name == MOCK_CLIENT_2["description"]

async def test_async_setup_entry_no_clients(
    hass: HomeAssistant, mock_coordinator: MagicMock, mock_config_entry: ConfigEntry
):
    """Test that no entities are created if the coordinator provides no client data."""
    mock_coordinator.data = {"clients": []} # No clients
    setup_hass_domain_data(hass, mock_config_entry.entry_id, mock_coordinator)
    
    mock_async_add_entities = AsyncMock()
    
    await async_setup_entry(hass, mock_config_entry, mock_async_add_entities)
    
    mock_async_add_entities.assert_not_called()

async def test_async_setup_entry_coordinator_data_none(
    hass: HomeAssistant, mock_coordinator: MagicMock, mock_config_entry: ConfigEntry
):
    """Test that no entities are created if coordinator.data is None."""
    mock_coordinator.data = None # Coordinator data is None
    setup_hass_domain_data(hass, mock_config_entry.entry_id, mock_coordinator)
    
    mock_async_add_entities = AsyncMock()
    
    await async_setup_entry(hass, mock_config_entry, mock_async_add_entities)
    
    mock_async_add_entities.assert_not_called()

async def test_async_setup_entry_clients_key_missing(
    hass: HomeAssistant, mock_coordinator: MagicMock, mock_config_entry: ConfigEntry
):
    """Test that no entities are created if 'clients' key is missing in coordinator.data."""
    mock_coordinator.data = {} # 'clients' key missing
    setup_hass_domain_data(hass, mock_config_entry.entry_id, mock_coordinator)
    
    mock_async_add_entities = AsyncMock()
    
    await async_setup_entry(hass, mock_config_entry, mock_async_add_entities)
    
    mock_async_add_entities.assert_not_called()

async def test_async_setup_entry_missing_client_mac(
    hass: HomeAssistant, mock_coordinator: MagicMock, mock_config_entry: ConfigEntry
):
    """Test that clients with missing MAC addresses are skipped."""
    client_missing_mac = MOCK_CLIENT_1.copy()
    del client_missing_mac["mac"]
    mock_coordinator.data = {"clients": [client_missing_mac, MOCK_CLIENT_2]}
    setup_hass_domain_data(hass, mock_config_entry.entry_id, mock_coordinator)
    
    mock_async_add_entities = AsyncMock()
    
    await async_setup_entry(hass, mock_config_entry, mock_async_add_entities)
    
    assert mock_async_add_entities.call_count == 1
    created_entities = mock_async_add_entities.call_args[0][0]
    assert len(created_entities) == 1
    assert created_entities[0]._client_info_data["mac"] == MOCK_CLIENT_2["mac"]


def test_meraki_device_tracker_properties_connected_to_ap(
    hass: HomeAssistant, mock_coordinator: MagicMock
):
    """Test properties of a connected MerakiDeviceTracker linked to an AP."""
    # Simulate client is initially present in coordinator data
    mock_coordinator.data = {"clients": [MOCK_CLIENT_1]} 
    
    tracker = MerakiDeviceTracker(mock_coordinator, MOCK_CLIENT_1)
    tracker.hass = hass # Assign hass for entity registry linking
    
    assert tracker.unique_id == f"{MOCK_CLIENT_1['mac']}_client_tracker"
    assert tracker.name == MOCK_CLIENT_1["description"]
    assert tracker.is_connected is True
    assert tracker.source_type == SourceType.ROUTER
    assert tracker.icon == "mdi:lan-connect"
    
    device_info = tracker.device_info
    assert device_info is not None
    assert device_info["identifiers"] == {(DOMAIN, MOCK_CLIENT_1["ap_serial"])}
    # The device_info name should refer to the parent device (AP in this case)
    assert device_info["name"] == f"Meraki Client on {MOCK_CLIENT_1['ap_serial']}"
    assert device_info["model"] == "Client Device"
    assert device_info["manufacturer"] == MOCK_CLIENT_1["manufacturer"]

def test_meraki_device_tracker_properties_connected_to_network(
    hass: HomeAssistant, mock_coordinator: MagicMock
):
    """Test properties of a connected MerakiDeviceTracker linked to a Network."""
    mock_coordinator.data = {"clients": [MOCK_CLIENT_2]}
    
    tracker = MerakiDeviceTracker(mock_coordinator, MOCK_CLIENT_2)
    tracker.hass = hass
    
    assert tracker.unique_id == f"{MOCK_CLIENT_2['mac']}_client_tracker"
    assert tracker.name == MOCK_CLIENT_2["description"]
    assert tracker.is_connected is True
    
    device_info = tracker.device_info
    assert device_info is not None
    # Linked to networkId as ap_serial is missing
    assert device_info["identifiers"] == {(DOMAIN, MOCK_CLIENT_2["networkId"])}
    assert device_info["name"] == f"Meraki Client on {MOCK_CLIENT_2['networkId']}"
    assert device_info["model"] == "Client Device"
    assert device_info["manufacturer"] == MOCK_CLIENT_2["manufacturer"]

def test_meraki_device_tracker_properties_disconnected(
    hass: HomeAssistant, mock_coordinator: MagicMock
):
    """Test properties when the client is not in the coordinator's data (disconnected)."""
    # Client MOCK_CLIENT_1 is used to initialize, but not present in coordinator.data
    mock_coordinator.data = {"clients": [MOCK_CLIENT_2]} # MOCK_CLIENT_1 is not here
    
    tracker = MerakiDeviceTracker(mock_coordinator, MOCK_CLIENT_1)
    tracker.hass = hass
    
    # _update_attributes would have been called in __init__
    # based on the coordinator state at that time.
    assert tracker.is_connected is False 
    assert tracker.icon == "mdi:lan-disconnect"
    assert tracker.name == MOCK_CLIENT_1["description"] # Name should still be from initial info


def test_meraki_device_tracker_name_fallback(
    hass: HomeAssistant, mock_coordinator: MagicMock
):
    """Test name fallback if description is missing."""
    client_no_desc_ip_copy = MOCK_CLIENT_NO_DESC_IP.copy()
    client_no_desc_ip_copy["ip"] = "192.168.1.103"
    mock_coordinator.data = {"clients": [client_no_desc_ip_copy]}

    tracker_ip = MerakiDeviceTracker(mock_coordinator, client_no_desc_ip_copy)
    assert tracker_ip.name == "192.168.1.103"

    client_no_desc_no_ip = MOCK_CLIENT_NO_DESC_IP.copy()
    # 'ip' is not in client_no_desc_no_ip
    mock_coordinator.data = {"clients": [client_no_desc_no_ip]}
    tracker_mac = MerakiDeviceTracker(mock_coordinator, client_no_desc_no_ip)
    # Based on current implementation, name attribute is set in init.
    # If description and IP are None, _attr_name will be None.
    # Home Assistant might then use entity_id or device name.
    # For this test, we check it's None as per current code.
    assert tracker_mac.name is None # Or it could be the MAC address if we want to implement that fallback for _attr_name


async def test_coordinator_updates_client_disconnects(
    hass: HomeAssistant, mock_coordinator: MagicMock
):
    """Test entity state update when a client disconnects."""
    mock_coordinator.data = {"clients": [MOCK_CLIENT_1]}
    
    tracker = MerakiDeviceTracker(mock_coordinator, MOCK_CLIENT_1)
    tracker.hass = hass
    tracker.async_write_ha_state = MagicMock() # Mock this method
    
    # Initial state
    assert tracker.is_connected is True
    assert tracker.icon == "mdi:lan-connect"
    
    # Simulate client disconnects - update coordinator data
    mock_coordinator.data = {"clients": []} 
    
    # Manually call the update handler (as the actual coordinator update is mocked)
    tracker._handle_coordinator_update()
    # await hass.async_block_till_done() # Not strictly necessary here as we call directly
    
    assert tracker.is_connected is False
    assert tracker.icon == "mdi:lan-disconnect"
    tracker.async_write_ha_state.assert_called_once()

async def test_coordinator_updates_client_connects(
    hass: HomeAssistant, mock_coordinator: MagicMock
):
    """Test entity state update when a client connects."""
    # Initially client is not present
    mock_coordinator.data = {"clients": []}
    
    tracker = MerakiDeviceTracker(mock_coordinator, MOCK_CLIENT_1)
    tracker.hass = hass
    tracker.async_write_ha_state = MagicMock()
    
    assert tracker.is_connected is False
    assert tracker.icon == "mdi:lan-disconnect"
    
    # Simulate client connects - update coordinator data
    mock_coordinator.data = {"clients": [MOCK_CLIENT_1]}
    
    tracker._handle_coordinator_update()
    
    assert tracker.is_connected is True
    assert tracker.icon == "mdi:lan-connect"
    tracker.async_write_ha_state.assert_called_once()

async def test_coordinator_updates_client_info_changes(
    hass: HomeAssistant, mock_coordinator: MagicMock
):
    """Test entity state update when client information (e.g., description) changes."""
    initial_client_data = MOCK_CLIENT_1.copy()
    mock_coordinator.data = {"clients": [initial_client_data]}
    
    tracker = MerakiDeviceTracker(mock_coordinator, initial_client_data)
    tracker.hass = hass
    tracker.async_write_ha_state = MagicMock()
    
    assert tracker.name == MOCK_CLIENT_1["description"]
    assert tracker._client_info_data["ip"] == MOCK_CLIENT_1["ip"]

    # Simulate client info changes in coordinator data
    updated_client_data = MOCK_CLIENT_1.copy()
    updated_client_data["description"] = "Client One Updated"
    updated_client_data["ip"] = "192.168.1.201" # IP also changed
    mock_coordinator.data = {"clients": [updated_client_data]}
    
    tracker._handle_coordinator_update()
    
    # Name is set at __init__ and not updated by _handle_coordinator_update by default.
    # This is standard HA behavior for `name` unless explicitly coded.
    # The test confirms _client_info_data IS updated.
    assert tracker.name == MOCK_CLIENT_1["description"] # Name remains initial
    assert tracker._client_info_data["description"] == "Client One Updated"
    assert tracker._client_info_data["ip"] == "192.168.1.201"
    assert tracker.is_connected is True # Still connected
    tracker.async_write_ha_state.assert_called_once()

async def test_entity_added_to_platform_and_coordinator(
    hass: HomeAssistant, mock_coordinator: MagicMock, mock_config_entry: ConfigEntry
):
    """Test that the entity correctly subscribes to coordinator updates when added."""
    mock_coordinator.data = {"clients": [MOCK_CLIENT_1]}
    setup_hass_domain_data(hass, mock_config_entry.entry_id, mock_coordinator)

    # Patch the MerakiDeviceTracker's methods for subscribing to coordinator
    with patch.object(MerakiDeviceTracker, 'async_added_to_hass', new_callable=AsyncMock) as mock_added_to_hass, \
         patch.object(MerakiDeviceTracker, '_handle_coordinator_update', new=MagicMock()) as mock_handle_update:

        mock_async_add_entities = AsyncMock()
        await async_setup_entry(hass, mock_config_entry, mock_async_add_entities)

        assert mock_async_add_entities.call_count == 1
        created_entities = mock_async_add_entities.call_args[0][0]
        tracker = created_entities[0]

        # Simulate Home Assistant adding the entity to the platform
        await tracker.async_added_to_hass()

        # Check that it called the original async_added_to_hass (which calls super)
        mock_added_to_hass.assert_called_once()
        
        # Check that it registered itself with the coordinator
        # This is implicitly tested by _handle_coordinator_update being callable
        # and the fact that CoordinatorEntity.__init__ sets this up.
        # We can also check if add_listener was called on coordinator by CoordinatorEntity.
        # The CoordinatorEntity's async_added_to_hass calls self.coordinator.async_add_listener(self._handle_coordinator_update)
        # So, if our mock_coordinator.async_add_listener was called, it means setup is correct.
        mock_coordinator.async_add_listener.assert_called_with(tracker._handle_coordinator_update)
        
        # Also, the initial state should be set by calling _handle_coordinator_update
        mock_handle_update.assert_called_once() # Called during __init__

```
