"""Tests for the Meraki Network Info sensor."""

from unittest.mock import AsyncMock, MagicMock, PropertyMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.sensor.meraki_network_info import (
    MerakiNetworkInfoSensor,
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
    coordinator.async_update_listeners = MagicMock()
    return coordinator


@pytest.fixture
def full_mx_device_data():
    """Sample device data for an MX device with all fields populated."""
    return {
        "serial": "Q123-ABCD-EFGH",
        "name": "Test MX64 Full",
        "model": "MX64",
        "networkId": "N_12345",
        "mac": "00:11:22:33:44:55",
        "wan1Ip": "1.2.3.4",
        "wan2Ip": "5.6.7.8",
        "lanIp": "192.168.1.1",
        "publicIp": "100.200.10.20",
        "status": "online",
        "tags": ["test", "mx", "full_data"],
        "wan1_dns_servers": ["8.8.8.8", "8.8.4.4"],
        "wan2_dns_servers": ["1.1.1.1"],
        "firmware": "MX 18.107",
        "firmware_up_to_date": True,
        "latest_firmware_version": "MX 18.107",
    }

@pytest.fixture
def minimal_mx_device_data():
    """Sample device data for an MX device with only essential fields."""
    return {
        "serial": "Q987-ZYXW-VUTS",
        "name": "Test MX60 Minimal", # Name might be missing in some API responses
        "model": "MX60",
        "status": "online", # Assume online for basic info
        # All other optional fields are None or missing
    }


async def test_network_info_sensor_initialization(
    hass: HomeAssistant, mock_coordinator, full_mx_device_data
):
    """Test sensor initialization."""
    device_arg = {"serial": full_mx_device_data["serial"], "name": full_mx_device_data["name"], "model": full_mx_device_data["model"]}
    sensor = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor.hass = hass

    assert sensor.unique_id == f"{full_mx_device_data['serial']}_network_info"
    assert sensor.name == "Network Information"
    assert sensor.device_info["identifiers"] == {(DOMAIN, full_mx_device_data["serial"])}


async def test_network_info_full_data(
    hass: HomeAssistant, mock_coordinator, full_mx_device_data
):
    """Test sensor state and attributes with full device data."""
    mock_coordinator.data = {"devices": [full_mx_device_data]}
    device_arg = {"serial": full_mx_device_data["serial"], "name": full_mx_device_data["name"], "model": full_mx_device_data["model"]}


    sensor = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == full_mx_device_data["name"]
    attrs = sensor.extra_state_attributes
    assert attrs["hostname"] == full_mx_device_data["name"]
    assert attrs["serial_number"] == full_mx_device_data["serial"]
    assert attrs["model"] == full_mx_device_data["model"]
    assert attrs["mac_address"] == full_mx_device_data["mac"]
    assert attrs["wan1_ip_address"] == full_mx_device_data["wan1Ip"]
    assert attrs["wan1_dns_servers"] == full_mx_device_data["wan1_dns_servers"]
    assert attrs["wan2_ip_address"] == full_mx_device_data["wan2Ip"]
    assert attrs["wan2_dns_servers"] == full_mx_device_data["wan2_dns_servers"]
    assert attrs["lan_ip_address"] == full_mx_device_data["lanIp"]
    assert attrs["public_ip_address"] == full_mx_device_data["publicIp"]
    assert attrs["network_id"] == full_mx_device_data["networkId"]
    assert attrs["tags"] == full_mx_device_data["tags"]
    assert attrs["firmware_version"] == full_mx_device_data["firmware"]
    assert attrs["firmware_up_to_date"] == full_mx_device_data["firmware_up_to_date"]
    assert attrs["latest_firmware_version"] == full_mx_device_data["latest_firmware_version"]


async def test_network_info_minimal_data(
    hass: HomeAssistant, mock_coordinator, minimal_mx_device_data
):
    """Test sensor state and attributes with minimal device data."""
    mock_coordinator.data = {"devices": [minimal_mx_device_data]}
    device_arg = {"serial": minimal_mx_device_data["serial"], "name": minimal_mx_device_data["name"], "model": minimal_mx_device_data["model"]}

    sensor = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == minimal_mx_device_data["name"]
    attrs = sensor.extra_state_attributes
    assert attrs["hostname"] == minimal_mx_device_data["name"]
    assert attrs["serial_number"] == minimal_mx_device_data["serial"]
    assert attrs["model"] == minimal_mx_device_data["model"]
    
    # These fields should be absent from attributes if not in source data (due to None filtering)
    assert "mac_address" not in attrs
    assert "wan1_ip_address" not in attrs
    assert attrs.get("wan1_dns_servers") == [] # Should default to empty list if key exists from fetcher but is None
    assert "wan2_ip_address" not in attrs
    assert attrs.get("wan2_dns_servers") == []
    assert "lan_ip_address" not in attrs
    assert "public_ip_address" not in attrs
    assert "network_id" not in attrs
    assert attrs.get("tags") == [] # Default to empty list
    assert "firmware_version" not in attrs # if 'firmware' key is missing
    assert "firmware_up_to_date" not in attrs # if 'firmware_up_to_date' key is missing
    assert "latest_firmware_version" not in attrs # if 'latest_firmware_version' key is missing


async def test_network_info_device_name_fallback(
    hass: HomeAssistant, mock_coordinator
):
    """Test native_value falls back to serial if device name is missing."""
    device_no_name = {
        "serial": "Q555-TEST-NAME",
        "model": "MX60",
        "status": "online",
        # "name" is missing
    }
    mock_coordinator.data = {"devices": [device_no_name]}
    device_arg = {"serial": device_no_name["serial"], "model": device_no_name["model"]} # name will be None

    sensor = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == device_no_name["serial"] # Fallback to serial
    assert "hostname" not in sensor.extra_state_attributes # Name is None, so filtered out


async def test_network_info_unknown_device_missing(
    hass: HomeAssistant, mock_coordinator, full_mx_device_data
):
    """Test sensor state when device data is missing."""
    mock_coordinator.data = {"devices": []} # Device not present
    device_arg = {"serial": full_mx_device_data["serial"], "name": full_mx_device_data["name"], "model": full_mx_device_data["model"]}


    sensor = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == "Unknown"
    assert sensor.extra_state_attributes == {}


async def test_network_info_availability(
    hass: HomeAssistant, mock_coordinator, full_mx_device_data
):
    """Test sensor availability."""
    device_arg = {"serial": full_mx_device_data["serial"], "name": full_mx_device_data["name"], "model": full_mx_device_data["model"]}
    sensor = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor.hass = hass

    type(mock_coordinator).data = PropertyMock(return_value=None)
    assert not sensor.available

    type(mock_coordinator).data = PropertyMock(return_value={"devices": []})
    assert not sensor.available

    type(mock_coordinator).data = PropertyMock(return_value={"devices": [full_mx_device_data]})
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()
    assert sensor.available
