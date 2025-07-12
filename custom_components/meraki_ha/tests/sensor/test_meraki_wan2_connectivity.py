"""Tests for the Meraki WAN2 Connectivity sensor."""

from unittest.mock import AsyncMock, MagicMock, PropertyMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.sensor.meraki_wan2_connectivity import (
    MerakiWAN2ConnectivitySensor,
    STATE_CONNECTED,
    STATE_DISCONNECTED,
    STATE_UNKNOWN,
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
def sample_mx_device_data():
    """Sample device data for an MX device. Note: wan2Ip specifically."""
    return {
        "serial": "Q123-ABCD-EFGH",
        "name": "Test MX64",
        "model": "MX64",
        "networkId": "N_12345",
        "mac": "00:11:22:33:44:55",
        "wan1Ip": "1.2.3.4",  # Assume WAN1 is up for these tests unless specified
        "wan2Ip": None,  # Default to None for WAN2
        "lanIp": "192.168.1.1",
        "status": "online",
        "tags": ["test", "mx"],
        "wan1_dns_servers": ["8.8.8.8"],
        "wan2_dns_servers": [],
        "firmware": "MX 18.107",
        "firmware_up_to_date": True,
        "latest_firmware_version": "MX 18.107",
    }


async def test_wan2_sensor_initialization(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor initialization and basic properties for WAN2."""
    sensor = MerakiWAN2ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass

    assert sensor.unique_id == f"{sample_mx_device_data['serial']}_wan2_connectivity"
    assert sensor.name == "WAN 2 Connectivity"
    assert sensor.device_info["identifiers"] == {
        (DOMAIN, sample_mx_device_data["serial"])
    }


async def test_wan2_state_connected(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor state when WAN2 is connected."""
    device_data_connected = {
        **sample_mx_device_data,
        "wan2Ip": "5.6.7.8",
        "status": "online",
    }
    mock_coordinator.data = {"devices": [device_data_connected]}

    sensor = MerakiWAN2ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == STATE_CONNECTED
    assert sensor.extra_state_attributes["wan2_ip_address"] == "5.6.7.8"


async def test_wan2_state_disconnected_no_ip(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor state when WAN2 is disconnected (no IP)."""
    device_data_no_ip = {**sample_mx_device_data, "wan2Ip": None, "status": "online"}
    mock_coordinator.data = {"devices": [device_data_no_ip]}

    sensor = MerakiWAN2ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == STATE_DISCONNECTED
    assert sensor.extra_state_attributes["wan2_ip_address"] == "N/A"


async def test_wan2_state_disconnected_device_offline(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor state when WAN2 is disconnected (device offline)."""
    device_data_offline = {
        **sample_mx_device_data,
        "wan2Ip": "5.6.7.8",
        "status": "offline",
    }
    mock_coordinator.data = {"devices": [device_data_offline]}

    sensor = MerakiWAN2ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == STATE_DISCONNECTED
    assert sensor.extra_state_attributes["wan2_ip_address"] == "5.6.7.8"


async def test_wan2_state_unknown_device_missing(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor state when device data is missing from coordinator for WAN2."""
    mock_coordinator.data = {"devices": []}

    sensor = MerakiWAN2ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == STATE_UNKNOWN
    assert sensor.extra_state_attributes == {}


async def test_wan2_availability(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor availability for WAN2."""
    sensor = MerakiWAN2ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass

    type(mock_coordinator).data = PropertyMock(return_value=None)
    assert not sensor.available

    type(mock_coordinator).data = PropertyMock(return_value={})
    assert not sensor.available

    type(mock_coordinator).data = PropertyMock(return_value={"devices": []})
    assert not sensor.available

    type(mock_coordinator).data = PropertyMock(
        return_value={"devices": [sample_mx_device_data]}
    )
    sensor._handle_coordinator_update()  # update based on new mock data
    await hass.async_block_till_done()
    assert sensor.available


async def test_wan2_coordinator_update(
    hass: HomeAssistant, mock_coordinator, sample_mx_device_data
):
    """Test sensor state updates via _handle_coordinator_update for WAN2."""
    device_initial = {**sample_mx_device_data, "wan2Ip": None, "status": "online"}
    mock_coordinator.data = {"devices": [device_initial]}

    sensor = MerakiWAN2ConnectivitySensor(mock_coordinator, sample_mx_device_data)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == STATE_DISCONNECTED

    device_updated = {
        **sample_mx_device_data,
        "wan2Ip": "9.10.11.12",
        "status": "online",
    }
    type(mock_coordinator).data = PropertyMock(
        return_value={"devices": [device_updated]}
    )
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()

    assert sensor.native_value == STATE_CONNECTED
    assert sensor.extra_state_attributes["wan2_ip_address"] == "9.10.11.12"

    device_offline = {
        **sample_mx_device_data,
        "wan2Ip": "9.10.11.12",
        "status": "offline",
    }
    type(mock_coordinator).data = PropertyMock(
        return_value={"devices": [device_offline]}
    )
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()

    assert sensor.native_value == STATE_DISCONNECTED

    type(mock_coordinator).data = PropertyMock(return_value={"devices": []})
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()

    assert sensor.native_value == STATE_UNKNOWN
    assert not sensor.available
