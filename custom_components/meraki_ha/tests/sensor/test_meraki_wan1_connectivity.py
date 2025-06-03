"""Tests for the Meraki WAN1 Connectivity sensor."""

from unittest.mock import AsyncMock, MagicMock, PropertyMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.sensor.meraki_wan1_connectivity import (
    MerakiWAN1ConnectivitySensor,
    STATE_CONNECTED,
    STATE_DISCONNECTED,
    STATE_UNKNOWN,
)

# Automatically patch the MerakiAPIClient for all tests in this module
pytestmark = pytest.mark.usefixtures("mock_meraki_client")


@pytest.fixture
def mock_coordinator(hass: HomeAssistant, mock_meraki_client_instance):
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MerakiDataUpdateCoordinator(
        hass, client=mock_meraki_client_instance, org_id="test_org_id"
    )
    coordinator.data = {"devices": []}  # Initial empty data
    coordinator.async_update_listeners = MagicMock() # Mock listeners
    return coordinator


@pytest.fixture
def sample_mx_device_data():
    """Sample device data for an MX device."""
    return {
        "serial": "Q123-ABCD-EFGH",
        "name": "Test MX64",
        "model": "MX64",
        "networkId": "N_12345",
        "mac": "00:11:22:33:44:55",
        "wan1Ip": None,
        "wan2Ip": None,
        "lanIp": "192.168.1.1",
        "status": "online",
        "tags": ["test", "mx"],
        "wan1_dns_servers": [],
        "wan2_dns_servers": [],
        "firmware": "MX 18.107",
        "firmware_up_to_date": True,
        "latest_firmware_version": "MX 18.107",
    }


async def test_wan1_sensor_initialization(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor initialization and basic properties."""
    sensor = MerakiWAN1ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass  # For async_write_ha_state if called directly or via _handle_coordinator_update

    assert sensor.unique_id == f"{sample_mx_device_data['serial']}_wan1_connectivity"
    assert sensor.name == "WAN 1 Connectivity"  # As _attr_name is set directly
    assert sensor.device_info["identifiers"] == {(DOMAIN, sample_mx_device_data["serial"])}
    assert sensor.device_info["name"] == sample_mx_device_data["name"]
    assert sensor.device_info["model"] == sample_mx_device_data["model"]
    assert sensor.device_info["manufacturer"] == "Cisco Meraki"


async def test_wan1_state_connected(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor state when WAN1 is connected."""
    device_data_connected = {**sample_mx_device_data, "wan1Ip": "1.2.3.4", "status": "online"}
    mock_coordinator.data = {"devices": [device_data_connected]}

    sensor = MerakiWAN1ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass
    
    # Manually trigger the first update or rely on the callback if it's set up
    # In a real HA environment, add_entity schedules _handle_coordinator_update
    # For testing, we can call it directly after attaching hass.
    await sensor.async_added_to_hass() # This should schedule the first update via the coordinator
    mock_coordinator.async_update_listeners() # Simulate coordinator calling listeners

    assert sensor.native_value == STATE_CONNECTED
    assert sensor.extra_state_attributes["wan1_ip_address"] == "1.2.3.4"


async def test_wan1_state_disconnected_no_ip(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor state when WAN1 is disconnected (no IP)."""
    device_data_no_ip = {**sample_mx_device_data, "wan1Ip": None, "status": "online"}
    mock_coordinator.data = {"devices": [device_data_no_ip]}

    sensor = MerakiWAN1ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == STATE_DISCONNECTED
    assert sensor.extra_state_attributes["wan1_ip_address"] == "N/A"


async def test_wan1_state_disconnected_device_offline(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor state when WAN1 is disconnected (device offline)."""
    device_data_offline = {**sample_mx_device_data, "wan1Ip": "1.2.3.4", "status": "offline"}
    mock_coordinator.data = {"devices": [device_data_offline]}

    sensor = MerakiWAN1ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == STATE_DISCONNECTED
    assert sensor.extra_state_attributes["wan1_ip_address"] == "1.2.3.4"


async def test_wan1_state_unknown_device_missing(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor state when device data is missing from coordinator."""
    mock_coordinator.data = {"devices": []}  # Device not in coordinator data

    sensor = MerakiWAN1ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()
    
    assert sensor.native_value == STATE_UNKNOWN
    assert sensor.extra_state_attributes == {}


async def test_wan1_availability(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor availability."""
    sensor = MerakiWAN1ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass

    # 1. Coordinator has no data yet (e.g. initial startup)
    type(mock_coordinator).data = PropertyMock(return_value=None)
    assert not sensor.available

    # 2. Coordinator has data, but 'devices' key is missing
    type(mock_coordinator).data = PropertyMock(return_value={})
    assert not sensor.available

    # 3. Coordinator has 'devices' list, but our device is not in it
    type(mock_coordinator).data = PropertyMock(return_value={"devices": []})
    assert not sensor.available # This relies on _update_state having run to see device is missing

    # 4. Device is present
    type(mock_coordinator).data = PropertyMock(return_value={"devices": [sample_mx_device_data]})
    # Call update to reflect new data
    sensor._handle_coordinator_update()
    await hass.async_block_till_done() # Allow state machine to catch up
    assert sensor.available


async def test_wan1_coordinator_update(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor state updates via _handle_coordinator_update."""
    # Initial state: disconnected
    device_initial = {**sample_mx_device_data, "wan1Ip": None, "status": "online"}
    mock_coordinator.data = {"devices": [device_initial]}

    sensor = MerakiWAN1ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners() # Initial update

    assert sensor.native_value == STATE_DISCONNECTED
    assert sensor.extra_state_attributes["wan1_ip_address"] == "N/A"

    # Simulate coordinator updating with new data: connected
    device_updated = {**sample_mx_device_data, "wan1Ip": "5.6.7.8", "status": "online"}
    # Update coordinator's data property directly for next call
    type(mock_coordinator).data = PropertyMock(return_value={"devices": [device_updated]})
    
    # Call the update handler
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()

    assert sensor.native_value == STATE_CONNECTED
    assert sensor.extra_state_attributes["wan1_ip_address"] == "5.6.7.8"

    # Simulate coordinator updating with device offline
    device_offline = {**sample_mx_device_data, "wan1Ip": "5.6.7.8", "status": "offline"}
    type(mock_coordinator).data = PropertyMock(return_value={"devices": [device_offline]})
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()

    assert sensor.native_value == STATE_DISCONNECTED
    assert sensor.extra_state_attributes["wan1_ip_address"] == "5.6.7.8"

    # Simulate device disappearing
    type(mock_coordinator).data = PropertyMock(return_value={"devices": []})
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()
    
    assert sensor.native_value == STATE_UNKNOWN
    assert sensor.extra_state_attributes == {}
    assert not sensor.available # availability should also reflect this
