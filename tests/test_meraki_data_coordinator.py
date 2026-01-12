"""Tests for the Meraki data coordinator."""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.meraki_ha.core.errors import ApiClientCommunicationError
from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator
from tests.const import MOCK_NETWORK


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.get_all_data = AsyncMock()
    return client


@pytest.fixture
def coordinator(hass, mock_api_client):
    """Fixture for a MerakiDataCoordinator instance."""
    entry = MagicMock()
    entry.options = {}
    entry.entry_id = "test_entry_id"
    coord = MerakiDataCoordinator(hass=hass, api_client=mock_api_client, entry=entry)
    coord.config_entry = entry
    return coord


@pytest.fixture
def coordinator_with_scan_interval(hass, mock_api_client):
    """Fixture for coordinator with custom scan interval."""
    entry = MagicMock()
    entry.options = {"scan_interval": 120}
    entry.entry_id = "test_entry_id"
    coord = MerakiDataCoordinator(hass=hass, api_client=mock_api_client, entry=entry)
    coord.config_entry = entry
    return coord


@pytest.mark.asyncio
async def test_update_data_handles_errors(coordinator, mock_api_client):
    """Test that _async_update_data handles disabled features."""
    # Arrange
    mock_api_client.get_all_data.return_value = {
        "networks": [MOCK_NETWORK],
        "devices": [],
        "appliance_traffic": {
            MOCK_NETWORK["id"]: {
                "error": "disabled",
                "reason": "Traffic analysis is not enabled",
            }
        },
        "vlans": {MOCK_NETWORK["id"]: []},
    }
    coordinator.add_network_status_message = MagicMock()
    coordinator.mark_traffic_check_done = MagicMock()
    coordinator.mark_vlan_check_done = MagicMock()

    # Act
    await coordinator._async_update_data()

    # Assert
    coordinator.add_network_status_message.assert_any_call(
        MOCK_NETWORK["id"], "Traffic Analysis is not enabled for this network."
    )
    coordinator.mark_traffic_check_done.assert_called_once_with(MOCK_NETWORK["id"])
    coordinator.add_network_status_message.assert_any_call(
        MOCK_NETWORK["id"], "VLANs are not enabled for this network."
    )
    coordinator.mark_vlan_check_done.assert_called_once_with(MOCK_NETWORK["id"])


@pytest.mark.asyncio
async def test_update_data_processes_devices(coordinator, mock_api_client):
    """Test that _async_update_data correctly processes device data."""
    mock_api_client.get_all_data.return_value = {
        "networks": [MOCK_NETWORK],
        "devices": [
            {
                "serial": "ABC-123",
                "name": "Switch",
                "model": "MS120",
                "status": "online",
                "networkId": MOCK_NETWORK["id"],
            },
            {
                "serial": "DEF-456",
                "name": "AP",
                "model": "MR33",
                "status": "online",
                "networkId": MOCK_NETWORK["id"],
            },
        ],
        "appliance_traffic": {},
        "vlans": {},
    }
    coordinator.mark_traffic_check_done = MagicMock()
    coordinator.mark_vlan_check_done = MagicMock()

    # Mock device and entity registries
    with (
        patch(
            "custom_components.meraki_ha.meraki_data_coordinator.dr.async_get"
        ) as mock_dev_reg,
        patch(
            "custom_components.meraki_ha.meraki_data_coordinator.er.async_get"
        ) as mock_ent_reg,
    ):
        mock_dev_reg.return_value.async_get_device.return_value = None
        mock_dev_reg.return_value.devices.values.return_value = []
        mock_ent_reg.return_value.async_entries_for_device.return_value = []

        result = await coordinator._async_update_data()

    assert "devices" in result
    assert len(result["devices"]) == 2
    assert result["devices"][0]["serial"] == "ABC-123"


@pytest.mark.asyncio
async def test_update_data_with_empty_networks(coordinator, mock_api_client):
    """Test _async_update_data handles empty network list."""
    mock_api_client.get_all_data.return_value = {
        "networks": [],
        "devices": [],
        "appliance_traffic": {},
        "vlans": {},
    }

    result = await coordinator._async_update_data()

    assert "networks" in result
    assert len(result["networks"]) == 0


@pytest.mark.asyncio
async def test_update_data_with_empty_ssids(coordinator, mock_api_client):
    """Test _async_update_data processes empty SSID data."""
    mock_api_client.get_all_data.return_value = {
        "networks": [MOCK_NETWORK],
        "devices": [],
        "ssids": {},
        "appliance_traffic": {},
        "vlans": {},
    }
    coordinator.mark_traffic_check_done = MagicMock()
    coordinator.mark_vlan_check_done = MagicMock()

    result = await coordinator._async_update_data()

    assert "ssids" in result


@pytest.mark.asyncio
async def test_coordinator_api_failure_handling(coordinator, mock_api_client):
    """Test coordinator handles API failures gracefully."""
    mock_api_client.get_all_data.side_effect = Exception("API Error")

    with pytest.raises(Exception, match="API Error"):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_update_data_with_clients(coordinator, mock_api_client):
    """Test _async_update_data processes client data."""
    mock_api_client.get_all_data.return_value = {
        "networks": [MOCK_NETWORK],
        "devices": [],
        "clients": {
            MOCK_NETWORK["id"]: [
                {"id": "client1", "mac": "00:11:22:33:44:55", "ip": "192.168.1.100"},
            ]
        },
        "appliance_traffic": {},
        "vlans": {},
    }
    coordinator.mark_traffic_check_done = MagicMock()
    coordinator.mark_vlan_check_done = MagicMock()

    result = await coordinator._async_update_data()

    assert "clients" in result


def test_coordinator_has_required_attributes(coordinator):
    """Test coordinator has required attributes."""
    # Coordinator should have the data and last_update_success attributes
    assert hasattr(coordinator, "data")
    assert hasattr(coordinator, "last_update_success")


def test_coordinator_initialization_defaults(coordinator):
    """Test coordinator initialization with default values."""
    assert coordinator.api is not None
    assert coordinator.devices_by_serial == {}
    assert coordinator.networks_by_id == {}
    assert coordinator.ssids_by_network_and_number == {}
    assert coordinator.last_successful_update is None
    assert coordinator.last_successful_data == {}


def test_coordinator_update_interval_is_fixed(hass, mock_api_client):
    """Test that the coordinator's update_interval is fixed, ignoring legacy options."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"

    # Test with a valid legacy option
    entry.options = {"scan_interval": 120}
    coord = MerakiDataCoordinator(hass=hass, api_client=mock_api_client, entry=entry)
    # The coordinator's internal update interval is fixed at 60 seconds
    # to drive the tiered polling mechanism.
    assert coord.update_interval == timedelta(seconds=60)

    # Test with an invalid legacy option
    entry.options = {"scan_interval": "invalid"}
    coord = MerakiDataCoordinator(hass=hass, api_client=mock_api_client, entry=entry)
    assert coord.update_interval == timedelta(seconds=60)

    # Test with a negative legacy option
    entry.options = {"scan_interval": -10}
    coord = MerakiDataCoordinator(hass=hass, api_client=mock_api_client, entry=entry)
    assert coord.update_interval == timedelta(seconds=60)


def test_register_pending_update(coordinator):
    """Test registering a pending update."""
    coordinator.register_pending_update("test_entity_123", expiry_seconds=60)

    assert "test_entity_123" in coordinator._pending_updates
    assert coordinator.is_update_pending("test_entity_123") is True


def test_is_update_pending_not_registered(coordinator):
    """Test is_update_pending returns False for non-registered entity."""
    assert coordinator.is_update_pending("non_existent_entity") is False


def test_is_update_pending_expired(coordinator):
    """Test is_update_pending returns False when expired."""
    # Register with expired time
    expired_time = datetime.now() - timedelta(seconds=10)
    coordinator._pending_updates["expired_entity"] = expired_time

    assert coordinator.is_update_pending("expired_entity") is False
    # Should be removed from the dictionary
    assert "expired_entity" not in coordinator._pending_updates


def test_is_pending_alias(coordinator):
    """Test is_pending is an alias for is_update_pending."""
    coordinator.register_pending_update("alias_test")
    assert coordinator.is_pending("alias_test") is True


def test_register_pending_alias(coordinator):
    """Test register_pending is an alias for register_pending_update."""
    coordinator.register_pending("alias_test_2", expiry_seconds=100)
    assert "alias_test_2" in coordinator._pending_updates


def test_get_device(coordinator):
    """Test get_device returns device data."""
    coordinator.devices_by_serial = {
        "ABC-123": {"serial": "ABC-123", "name": "Test Device"}
    }

    device = coordinator.get_device("ABC-123")
    assert device is not None
    assert device["name"] == "Test Device"


def test_get_device_not_found(coordinator):
    """Test get_device returns None for unknown serial."""
    coordinator.devices_by_serial = {}

    assert coordinator.get_device("UNKNOWN") is None


def test_get_network(coordinator):
    """Test get_network returns network data."""
    coordinator.networks_by_id = {"N_123": {"id": "N_123", "name": "Test Network"}}

    network = coordinator.get_network("N_123")
    assert network is not None
    assert network["name"] == "Test Network"


def test_get_network_not_found(coordinator):
    """Test get_network returns None for unknown network ID."""
    coordinator.networks_by_id = {}

    assert coordinator.get_network("N_UNKNOWN") is None


def test_get_ssid(coordinator):
    """Test get_ssid returns SSID data."""
    coordinator.ssids_by_network_and_number = {
        ("N_123", 0): {"networkId": "N_123", "number": 0, "name": "Corporate"}
    }

    ssid = coordinator.get_ssid("N_123", 0)
    assert ssid is not None
    assert ssid["name"] == "Corporate"


def test_get_ssid_not_found(coordinator):
    """Test get_ssid returns None for unknown SSID."""
    coordinator.ssids_by_network_and_number = {}

    assert coordinator.get_ssid("N_123", 99) is None


def test_add_status_message(coordinator):
    """Test add_status_message adds message to device."""
    coordinator.data = {
        "devices": [{"serial": "ABC-123", "name": "Device", "status_messages": []}]
    }

    coordinator.add_status_message("ABC-123", "Test message")

    assert "Test message" in coordinator.data["devices"][0]["status_messages"]


def test_add_status_message_no_duplicate(coordinator):
    """Test add_status_message avoids duplicates."""
    coordinator.data = {
        "devices": [
            {"serial": "ABC-123", "name": "Device", "status_messages": ["Existing"]}
        ]
    }

    coordinator.add_status_message("ABC-123", "Existing")

    assert coordinator.data["devices"][0]["status_messages"] == ["Existing"]


def test_add_status_message_creates_list(coordinator):
    """Test add_status_message creates status_messages list if missing."""
    coordinator.data = {"devices": [{"serial": "ABC-123", "name": "Device"}]}

    coordinator.add_status_message("ABC-123", "New message")

    assert "New message" in coordinator.data["devices"][0]["status_messages"]


def test_add_network_status_message(coordinator):
    """Test add_network_status_message adds message to network."""
    coordinator.data = {
        "networks": [{"id": "N_123", "name": "Network", "status_messages": []}]
    }

    coordinator.add_network_status_message("N_123", "Network message")

    assert "Network message" in coordinator.data["networks"][0]["status_messages"]


def test_is_vlan_check_due_first_time(coordinator):
    """Test is_vlan_check_due returns True on first check."""
    assert coordinator.is_vlan_check_due("N_123") is True


def test_is_vlan_check_due_after_mark(coordinator):
    """Test is_vlan_check_due returns False after marking done."""
    coordinator.mark_vlan_check_done("N_123")

    assert coordinator.is_vlan_check_due("N_123") is False


def test_is_traffic_check_due_first_time(coordinator):
    """Test is_traffic_check_due returns True on first check."""
    assert coordinator.is_traffic_check_due("N_123") is True


def test_is_traffic_check_due_after_mark(coordinator):
    """Test is_traffic_check_due returns False after marking done."""
    coordinator.mark_traffic_check_done("N_123")

    assert coordinator.is_traffic_check_due("N_123") is False


def test_is_check_due_after_24_hours(coordinator):
    """Test _is_check_due returns True after 24 hours."""
    coordinator._vlan_check_timestamps["N_123"] = datetime.now() - timedelta(hours=25)

    assert coordinator.is_vlan_check_due("N_123") is True


def test_process_sensor_readings_for_frontend(coordinator):
    """Test _process_sensor_readings_for_frontend processes readings."""
    readings = [
        {"metric": "temperature", "temperature": {"celsius": 23.5}},
        {"metric": "humidity", "humidity": {"relativePercentage": 45}},
        {"metric": "water", "water": {"present": True}},
    ]

    result = coordinator._process_sensor_readings_for_frontend(readings)

    assert result["temperature"] == 23.5
    assert result["humidity"] == 45
    assert result["water"] is True


def test_process_sensor_readings_empty(coordinator):
    """Test _process_sensor_readings_for_frontend handles empty input."""
    assert coordinator._process_sensor_readings_for_frontend([]) == {}
    assert coordinator._process_sensor_readings_for_frontend(None) == {}


def test_process_sensor_readings_noise(coordinator):
    """Test _process_sensor_readings_for_frontend handles noise metric."""
    readings = [{"metric": "noise", "noise": {"ambient": {"level": 42.5}}}]

    result = coordinator._process_sensor_readings_for_frontend(readings)

    assert result["noise"] == 42.5


def test_filter_enabled_networks_no_config(coordinator):
    """Test _filter_enabled_networks handles missing config."""
    coordinator.config_entry = None
    data = {"networks": [{"id": "N_123"}]}

    coordinator._filter_enabled_networks(data)

    # Should return without modification
    assert "is_enabled" not in data["networks"][0]


def test_filter_device_types(coordinator):
    """Test _filter_device_types filters correctly."""
    coordinator.config_entry.options = {
        "dashboard_device_type_filter": ["camera", "switch"]
    }
    data = {
        "devices": [
            {"serial": "A", "model": "MV12"},
            {"serial": "B", "model": "MS120"},
            {"serial": "C", "model": "MR33"},
        ]
    }

    coordinator._filter_device_types(data)

    assert len(data["devices"]) == 2
    assert data["devices"][0]["serial"] == "A"
    assert data["devices"][1]["serial"] == "B"


def test_filter_enabled_networks_with_filter(coordinator):
    """Test _filter_enabled_networks filters correctly."""
    coordinator.config_entry.options = {"enabled_networks": ["N_123"]}
    data = {
        "networks": [
            {"id": "N_123", "name": "Enabled"},
            {"id": "N_456", "name": "Disabled"},
        ],
        "devices": [
            {"serial": "A", "networkId": "N_123"},
            {"serial": "B", "networkId": "N_456"},
        ],
        "ssids": [
            {"networkId": "N_123", "number": 0},
            {"networkId": "N_456", "number": 0},
        ],
    }

    coordinator._filter_enabled_networks(data)

    assert data["networks"][0]["is_enabled"] is True
    assert data["networks"][1]["is_enabled"] is False
    assert len(data["devices"]) == 1
    assert data["devices"][0]["serial"] == "A"
    assert len(data["ssids"]) == 1


def test_get_enabled_network_ids_no_config(coordinator):
    """Test _get_enabled_network_ids returns None when no config."""
    coordinator.config_entry = None

    assert coordinator._get_enabled_network_ids() is None


def test_get_enabled_network_ids_empty(coordinator):
    """Test _get_enabled_network_ids returns None when empty."""
    coordinator.config_entry.options = {"enabled_networks": []}

    assert coordinator._get_enabled_network_ids() is None


def test_get_enabled_network_ids_with_values(coordinator):
    """Test _get_enabled_network_ids returns set of IDs."""
    coordinator.config_entry.options = {"enabled_networks": ["N_123", "N_456"]}

    result = coordinator._get_enabled_network_ids()

    assert result == {"N_123", "N_456"}


@pytest.mark.asyncio
async def test_update_data_no_data_raises(coordinator, mock_api_client):
    """Test _async_update_data raises when API returns None."""
    mock_api_client.get_all_data.return_value = None

    with pytest.raises(UpdateFailed, match="API call returned no data"):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_update_data_communication_error_with_stale_data(
    coordinator, mock_api_client
):
    """Test _async_update_data returns stale data on communication error."""
    coordinator.last_successful_data = {
        "networks": [MOCK_NETWORK],
        "devices": [],
    }
    mock_api_client.get_all_data.side_effect = ApiClientCommunicationError("Timeout")

    result = await coordinator._async_update_data()

    assert result == coordinator.last_successful_data


@pytest.mark.asyncio
async def test_update_data_communication_error_no_stale_data(
    coordinator, mock_api_client
):
    """Test _async_update_data raises when no stale data available."""
    coordinator.last_successful_data = {}
    mock_api_client.get_all_data.side_effect = ApiClientCommunicationError("Timeout")

    with pytest.raises(UpdateFailed, match="Could not connect to Meraki API"):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_update_data_populates_lookup_tables(coordinator, mock_api_client):
    """Test _async_update_data populates lookup tables."""
    mock_api_client.get_all_data.return_value = {
        "networks": [{"id": "N_123", "name": "Test Network"}],
        "devices": [{"serial": "ABC-123", "name": "Device", "networkId": "N_123"}],
        "ssids": [{"networkId": "N_123", "number": 0, "name": "WiFi"}],
        "appliance_traffic": {},
        "vlans": {},
    }

    # Mock device and entity registries to avoid real HA calls
    with (
        patch(
            "custom_components.meraki_ha.meraki_data_coordinator.dr.async_get"
        ) as mock_dev_reg,
        patch(
            "custom_components.meraki_ha.meraki_data_coordinator.er.async_get"
        ) as mock_ent_reg,
    ):
        mock_dev_reg.return_value.async_get_device.return_value = None
        mock_dev_reg.return_value.devices.values.return_value = []
        mock_ent_reg.return_value.async_entries_for_device.return_value = []

        await coordinator._async_update_data()

    assert "ABC-123" in coordinator.devices_by_serial
    assert "N_123" in coordinator.networks_by_id
    assert ("N_123", 0) in coordinator.ssids_by_network_and_number


@pytest.mark.asyncio
async def test_update_data_sets_last_successful_update(coordinator, mock_api_client):
    """Test _async_update_data sets last successful update timestamp."""
    mock_api_client.get_all_data.return_value = {
        "networks": [],
        "devices": [],
        "appliance_traffic": {},
        "vlans": {},
    }

    before = datetime.now()
    await coordinator._async_update_data()
    after = datetime.now()

    assert coordinator.last_successful_update is not None
    assert before <= coordinator.last_successful_update <= after


@pytest.mark.asyncio
async def test_update_data_adds_ssids_to_networks(coordinator, mock_api_client):
    """Test _async_update_data adds SSIDs to network objects."""
    mock_api_client.get_all_data.return_value = {
        "networks": [{"id": "N_123", "name": "Test"}],
        "devices": [],
        "ssids": [
            {"networkId": "N_123", "number": 0, "name": "WiFi1"},
            {"networkId": "N_123", "number": 1, "name": "WiFi2"},
            {"networkId": "N_456", "number": 0, "name": "Other"},
        ],
        "appliance_traffic": {},
        "vlans": {},
    }

    result = await coordinator._async_update_data()

    assert len(result["networks"][0]["ssids"]) == 2


def test_populate_device_entities_no_device(coordinator):
    """Test _populate_device_entities handles missing device in registry."""
    data = {"devices": [{"serial": "ABC-123", "name": "Device"}]}

    # Mock device registry to return no device
    with (
        patch(
            "custom_components.meraki_ha.meraki_data_coordinator.dr.async_get"
        ) as mock_dev_reg,
        patch("custom_components.meraki_ha.meraki_data_coordinator.er.async_get"),
    ):
        mock_dev_reg.return_value.async_get_device.return_value = None

        coordinator._populate_device_entities(data)

        # Device should have empty status_messages list but no entity_id
        assert data["devices"][0].get("status_messages") == []
        assert "entity_id" not in data["devices"][0]


def test_populate_device_entities_empty_data(coordinator):
    """Test _populate_device_entities handles empty data."""
    coordinator._populate_device_entities(None)
    coordinator._populate_device_entities({})
    coordinator._populate_device_entities({"devices": []})
    # Should not raise any exceptions


def test_populate_ssid_entities_empty_data(coordinator):
    """Test _populate_ssid_entities handles empty data."""
    coordinator._populate_ssid_entities(None)
    coordinator._populate_ssid_entities({})
    coordinator._populate_ssid_entities({"ssids": []})
    # Should not raise any exceptions


# =============================================================================
# Tiered Polling Tests
# =============================================================================


@pytest.fixture
def coordinator_with_tiered_polling(hass, mock_api_client):
    """Fixture for coordinator with tiered polling intervals configured."""
    entry = MagicMock()
    entry.options = {
        "network_scan_interval": 600,  # 10 minutes
        "device_scan_interval": 300,  # 5 minutes
        "client_scan_interval": 60,  # 1 minute
        "ssid_scan_interval": 300,  # 5 minutes
    }
    entry.entry_id = "test_entry_id"
    coord = MerakiDataCoordinator(hass=hass, api_client=mock_api_client, entry=entry)
    coord.config_entry = entry
    return coord


@pytest.mark.asyncio
async def test_tiered_polling_first_call_fetches_all(
    coordinator_with_tiered_polling, mock_api_client
):
    """Test that the first call fetches all data types."""
    mock_api_client.get_all_data.return_value = {
        "networks": [{"id": "N_123", "name": "Test"}],
        "devices": [],
        "appliance_traffic": {},
        "vlans": {},
    }

    # All timestamps should be None initially
    assert coordinator_with_tiered_polling.last_network_update is None
    assert coordinator_with_tiered_polling.last_device_update is None
    assert coordinator_with_tiered_polling.last_client_update is None
    assert coordinator_with_tiered_polling.last_ssid_update is None

    await coordinator_with_tiered_polling._async_update_data()

    # Verify get_all_data was called with all fetch flags True
    mock_api_client.get_all_data.assert_called_once()
    call_kwargs = mock_api_client.get_all_data.call_args[1]
    assert call_kwargs["fetch_networks"] is True
    assert call_kwargs["fetch_devices"] is True
    assert call_kwargs["fetch_clients"] is True
    assert call_kwargs["fetch_ssids"] is True

    # All timestamps should be set
    assert coordinator_with_tiered_polling.last_network_update is not None
    assert coordinator_with_tiered_polling.last_device_update is not None
    assert coordinator_with_tiered_polling.last_client_update is not None
    assert coordinator_with_tiered_polling.last_ssid_update is not None


@pytest.mark.asyncio
async def test_tiered_polling_skips_when_intervals_not_exceeded(
    coordinator_with_tiered_polling, mock_api_client
):
    """Test that polling is skipped when no intervals have been exceeded."""
    mock_data = {
        "networks": [{"id": "N_123", "name": "Test"}],
        "devices": [],
        "appliance_traffic": {},
        "vlans": {},
    }
    mock_api_client.get_all_data.return_value = mock_data

    # First call to set timestamps
    await coordinator_with_tiered_polling._async_update_data()
    mock_api_client.get_all_data.reset_mock()

    # Set last_successful_data so the coordinator returns cached data
    coordinator_with_tiered_polling.last_successful_data = mock_data

    # Immediately call again - no intervals should be exceeded
    result = await coordinator_with_tiered_polling._async_update_data()

    # Should return cached data without calling API
    mock_api_client.get_all_data.assert_not_called()
    assert result == mock_data


@pytest.mark.asyncio
async def test_tiered_polling_respects_individual_intervals(
    coordinator_with_tiered_polling, mock_api_client
):
    """Test that each data type respects its own interval."""
    mock_data = {
        "networks": [{"id": "N_123", "name": "Test"}],
        "devices": [],
        "appliance_traffic": {},
        "vlans": {},
    }
    mock_api_client.get_all_data.return_value = mock_data

    # First call to set timestamps
    await coordinator_with_tiered_polling._async_update_data()
    mock_api_client.get_all_data.reset_mock()

    # Simulate client interval exceeded but others not
    coordinator_with_tiered_polling.last_client_update = (
        datetime.now() - timedelta(seconds=120)  # 2 minutes ago
    )
    # Keep other timestamps recent
    now = datetime.now()
    coordinator_with_tiered_polling.last_network_update = now
    coordinator_with_tiered_polling.last_device_update = now
    coordinator_with_tiered_polling.last_ssid_update = now

    await coordinator_with_tiered_polling._async_update_data()

    # Verify only clients are fetched
    mock_api_client.get_all_data.assert_called_once()
    call_kwargs = mock_api_client.get_all_data.call_args[1]
    assert call_kwargs["fetch_networks"] is False
    assert call_kwargs["fetch_devices"] is False
    assert call_kwargs["fetch_clients"] is True
    assert call_kwargs["fetch_ssids"] is False


@pytest.mark.asyncio
async def test_tiered_polling_uses_default_intervals(coordinator, mock_api_client):
    """Test that default intervals are used when not configured."""
    mock_api_client.get_all_data.return_value = {
        "networks": [],
        "devices": [],
        "appliance_traffic": {},
        "vlans": {},
    }

    # First call to set timestamps
    await coordinator._async_update_data()

    # Verify the coordinator used default intervals by checking timestamps were set
    assert coordinator.last_network_update is not None
    assert coordinator.last_device_update is not None
    assert coordinator.last_client_update is not None
    assert coordinator.last_ssid_update is not None


# === Scanning API Data Handling Tests ===


@pytest.mark.asyncio
async def test_scanning_api_updates_existing_client(coordinator):
    """Test that scanning API data updates existing clients."""
    # Set up coordinator with existing client data
    coordinator.data = {
        "clients": [
            {
                "mac": "aa:bb:cc:dd:ee:ff",
                "ip": "192.168.1.100",
                "description": "Test Device",
                "lastSeen": "2024-01-01T00:00:00Z",
            }
        ]
    }
    coordinator.async_update_listeners = MagicMock()

    # Scanning API data payload
    scanning_data = {
        "apMac": "00:11:22:33:44:55",
        "observations": [
            {
                "clientMac": "aa:bb:cc:dd:ee:ff",
                "seenTime": "2024-01-15T12:00:00Z",
                "rssi": -45,
                "location": {"lat": 37.7749, "lng": -122.4194},
            }
        ],
    }

    await coordinator.async_handle_scanning_api_data(scanning_data)

    # Verify client data was updated
    client = coordinator.data["clients"][0]
    assert client["lastSeen"] == "2024-01-15T12:00:00Z"
    assert client["rssi"] == -45
    assert client["recentDeviceMac"] == "00:11:22:33:44:55"
    assert client["latitude"] == 37.7749
    assert client["longitude"] == -122.4194
    coordinator.async_update_listeners.assert_called_once()


@pytest.mark.asyncio
async def test_scanning_api_ignores_unknown_client(coordinator):
    """Test that scanning API data ignores unknown client MACs."""
    # Set up coordinator with no matching client
    coordinator.data = {
        "clients": [
            {
                "mac": "11:22:33:44:55:66",  # Different MAC
                "ip": "192.168.1.100",
            }
        ]
    }
    coordinator.async_update_listeners = MagicMock()

    # Scanning API data with unknown MAC
    scanning_data = {
        "apMac": "00:11:22:33:44:55",
        "observations": [
            {
                "clientMac": "aa:bb:cc:dd:ee:ff",  # Unknown MAC
                "seenTime": "2024-01-15T12:00:00Z",
                "rssi": -45,
            }
        ],
    }

    await coordinator.async_handle_scanning_api_data(scanning_data)

    # Verify existing client was not modified
    client = coordinator.data["clients"][0]
    assert "lastSeen" not in client
    assert "rssi" not in client
    # Listeners should not be called since no updates were made
    coordinator.async_update_listeners.assert_not_called()


@pytest.mark.asyncio
async def test_scanning_api_handles_multiple_observations(coordinator):
    """Test that scanning API handles multiple observations correctly."""
    # Set up coordinator with multiple clients
    coordinator.data = {
        "clients": [
            {"mac": "aa:bb:cc:dd:ee:ff", "ip": "192.168.1.100"},
            {"mac": "11:22:33:44:55:66", "ip": "192.168.1.101"},
            {"mac": "ff:ee:dd:cc:bb:aa", "ip": "192.168.1.102"},
        ]
    }
    coordinator.async_update_listeners = MagicMock()

    # Scanning API data with multiple observations
    scanning_data = {
        "apMac": "00:11:22:33:44:55",
        "observations": [
            {"clientMac": "aa:bb:cc:dd:ee:ff", "seenTime": "2024-01-15T12:00:00Z"},
            {"clientMac": "11:22:33:44:55:66", "seenTime": "2024-01-15T12:01:00Z"},
            {"clientMac": "xx:yy:zz:aa:bb:cc", "seenTime": "2024-01-15T12:02:00Z"},
        ],
    }

    await coordinator.async_handle_scanning_api_data(scanning_data)

    # Verify first two clients were updated, third client unchanged
    assert coordinator.data["clients"][0]["lastSeen"] == "2024-01-15T12:00:00Z"
    assert coordinator.data["clients"][1]["lastSeen"] == "2024-01-15T12:01:00Z"
    assert "lastSeen" not in coordinator.data["clients"][2]
    coordinator.async_update_listeners.assert_called_once()


@pytest.mark.asyncio
async def test_scanning_api_handles_empty_data(coordinator):
    """Test that scanning API handles missing or empty data gracefully."""
    coordinator.data = None
    coordinator.async_update_listeners = MagicMock()

    scanning_data = {
        "apMac": "00:11:22:33:44:55",
        "observations": [{"clientMac": "aa:bb:cc:dd:ee:ff"}],
    }

    # Should not raise an error
    await coordinator.async_handle_scanning_api_data(scanning_data)
    coordinator.async_update_listeners.assert_not_called()


@pytest.mark.asyncio
async def test_scanning_api_handles_missing_clients_key(coordinator):
    """Test that scanning API handles missing clients key gracefully."""
    coordinator.data = {"networks": [], "devices": []}  # No clients key
    coordinator.async_update_listeners = MagicMock()

    scanning_data = {
        "apMac": "00:11:22:33:44:55",
        "observations": [{"clientMac": "aa:bb:cc:dd:ee:ff"}],
    }

    # Should not raise an error
    await coordinator.async_handle_scanning_api_data(scanning_data)
    coordinator.async_update_listeners.assert_not_called()


@pytest.mark.asyncio
async def test_scanning_api_handles_observation_without_location(coordinator):
    """Test that scanning API handles observations without location data."""
    coordinator.data = {
        "clients": [{"mac": "aa:bb:cc:dd:ee:ff", "ip": "192.168.1.100"}]
    }
    coordinator.async_update_listeners = MagicMock()

    # Observation without location
    scanning_data = {
        "apMac": "00:11:22:33:44:55",
        "observations": [
            {
                "clientMac": "aa:bb:cc:dd:ee:ff",
                "seenTime": "2024-01-15T12:00:00Z",
                "rssi": -50,
                # No location field
            }
        ],
    }

    await coordinator.async_handle_scanning_api_data(scanning_data)

    client = coordinator.data["clients"][0]
    assert client["lastSeen"] == "2024-01-15T12:00:00Z"
    assert client["rssi"] == -50
    assert "latitude" not in client
    assert "longitude" not in client
