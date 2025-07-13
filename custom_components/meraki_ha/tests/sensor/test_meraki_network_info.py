"""Tests for the Meraki Network Info sensor."""

from unittest.mock import AsyncMock, MagicMock, PropertyMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.sensor.meraki_network_info import (
    MerakiNetworkInfoSensor,
)

@pytest.fixture
def mock_coordinator(hass: HomeAssistant):
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MerakiDataUpdateCoordinator(
        hass, client=MagicMock(), org_id="test_org_id"
    )
    coordinator.data = {"devices": []}
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
        "lan_dns_settings": {
            "VLAN 10 (Data)": ["192.168.10.5", "192.168.10.6"],
            "VLAN 20 (Voice)": "google_dns",
        },
        "firmware": "MX 18.107",
        "firmware_up_to_date": True,
        "latest_firmware_version": "MX 18.107",
    }


@pytest.fixture
def minimal_mx_device_data():
    """Sample device data for an MX device with only essential fields."""
    return {
        "serial": "Q987-ZYXW-VUTS",
        "name": "Test MX60 Minimal",  # Name might be missing in some API responses
        "model": "MX60",
        "status": "online",  # Assume online for basic info
        # All other optional fields are None or missing
    }


async def test_network_info_sensor_initialization(
    hass: HomeAssistant, mock_coordinator, full_mx_device_data
):
    """Test sensor initialization."""
    device_arg = {
        "serial": full_mx_device_data["serial"],
        "name": full_mx_device_data["name"],
        "model": full_mx_device_data["model"],
    }
    sensor = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor.hass = hass

    assert sensor.unique_id == f"{full_mx_device_data['serial']}_network_info"
    assert sensor.name == "Network Information"
    assert sensor.device_info["identifiers"] == {
        (DOMAIN, full_mx_device_data["serial"])
    }


async def test_network_info_full_data(
    hass: HomeAssistant, mock_coordinator, full_mx_device_data
):
    """Test sensor state and attributes with full device data."""
    mock_coordinator.data = {"devices": [full_mx_device_data]}
    device_arg = {
        "serial": full_mx_device_data["serial"],
        "name": full_mx_device_data["name"],
        "model": full_mx_device_data["model"],
    }

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
    assert attrs["lan_dns_settings"] == full_mx_device_data["lan_dns_settings"]
    assert attrs["firmware_version"] == full_mx_device_data["firmware"]
    assert attrs["firmware_up_to_date"] == full_mx_device_data["firmware_up_to_date"]
    assert (
        attrs["latest_firmware_version"]
        == full_mx_device_data["latest_firmware_version"]
    )


async def test_network_info_partial_and_empty_dns_data(
    hass: HomeAssistant, mock_coordinator, minimal_mx_device_data
):
    """Test sensor with various DNS data scenarios: empty lists, absent."""
    # Scenario 1: WAN DNS empty, LAN DNS empty dict
    device_data_empty_dns = {
        **minimal_mx_device_data,  # Use minimal as a base
        "wan1_dns_servers": [],
        "wan2_dns_servers": [],
        "lan_dns_settings": {},
    }
    mock_coordinator.data = {"devices": [device_data_empty_dns]}
    device_arg = {
        "serial": device_data_empty_dns["serial"],
        "name": device_data_empty_dns["name"],
        "model": device_data_empty_dns["model"],
    }

    sensor_empty = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor_empty.hass = hass
    await sensor_empty.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    attrs_empty = sensor_empty.extra_state_attributes
    assert attrs_empty["wan1_dns_servers"] == []
    assert attrs_empty["wan2_dns_servers"] == []
    assert attrs_empty["lan_dns_settings"] == {}

    # Scenario 2: LAN DNS absent (None), WAN DNS still empty
    device_data_no_lan_dns = {
        **minimal_mx_device_data,
        "wan1_dns_servers": [],
        "wan2_dns_servers": [],
        "lan_dns_settings": None,  # Explicitly None
    }
    mock_coordinator.data = {"devices": [device_data_no_lan_dns]}
    # Re-use device_arg for sensor init as serial/name/model are same for this test variation

    sensor_no_lan = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor_no_lan.hass = hass
    # Need to re-trigger the update mechanism for the new sensor instance or new data
    # Forcing update by calling the handler
    sensor_no_lan._handle_coordinator_update()
    await hass.async_block_till_done()

    attrs_no_lan = sensor_no_lan.extra_state_attributes
    assert attrs_no_lan["wan1_dns_servers"] == []
    assert attrs_no_lan["wan2_dns_servers"] == []
    assert "lan_dns_settings" not in attrs_no_lan  # Should be filtered out if None

    # Scenario 3: All DNS fields completely missing from device data (not even None)
    # This also tests the defaults in the sensor's .get("...", []) calls
    device_data_missing_all_dns = {
        **minimal_mx_device_data  # Base, and don't add any _dns_servers or _settings keys
    }
    # Remove keys if they were part of minimal_mx_device_data, though they aren't by default
    device_data_missing_all_dns.pop("wan1_dns_servers", None)
    device_data_missing_all_dns.pop("wan2_dns_servers", None)
    device_data_missing_all_dns.pop("lan_dns_settings", None)

    mock_coordinator.data = {"devices": [device_data_missing_all_dns]}
    sensor_missing_all = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor_missing_all.hass = hass
    sensor_missing_all._handle_coordinator_update()
    await hass.async_block_till_done()

    attrs_missing_all = sensor_missing_all.extra_state_attributes
    # Based on sensor code: .get("wanX_dns_servers", []) will result in empty list being added
    assert attrs_missing_all["wan1_dns_servers"] == []
    assert attrs_missing_all["wan2_dns_servers"] == []
    assert (
        "lan_dns_settings" not in attrs_missing_all
    )  # .get("lan_dns_settings") is None, so filtered


async def test_network_info_device_name_fallback(hass: HomeAssistant, mock_coordinator):
    """Test native_value falls back to serial if device name is missing."""
    device_no_name = {
        "serial": "Q555-TEST-NAME",
        "model": "MX60",
        "status": "online",
        # "name" is missing
    }
    mock_coordinator.data = {"devices": [device_no_name]}
    device_arg = {
        "serial": device_no_name["serial"],
        "model": device_no_name["model"],
    }  # name will be None

    sensor = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == device_no_name["serial"]  # Fallback to serial
    assert (
        "hostname" not in sensor.extra_state_attributes
    )  # Name is None, so filtered out


async def test_network_info_unknown_device_missing(
    hass: HomeAssistant, mock_coordinator, full_mx_device_data
):
    """Test sensor state when device data is missing."""
    mock_coordinator.data = {"devices": []}  # Device not present
    device_arg = {
        "serial": full_mx_device_data["serial"],
        "name": full_mx_device_data["name"],
        "model": full_mx_device_data["model"],
    }

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
    device_arg = {
        "serial": full_mx_device_data["serial"],
        "name": full_mx_device_data["name"],
        "model": full_mx_device_data["model"],
    }
    sensor = MerakiNetworkInfoSensor(mock_coordinator, device_arg)
    sensor.hass = hass

    type(mock_coordinator).data = PropertyMock(return_value=None)
    assert not sensor.available

    type(mock_coordinator).data = PropertyMock(return_value={"devices": []})
    assert not sensor.available

    type(mock_coordinator).data = PropertyMock(
        return_value={"devices": [full_mx_device_data]}
    )
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()
    assert sensor.available
