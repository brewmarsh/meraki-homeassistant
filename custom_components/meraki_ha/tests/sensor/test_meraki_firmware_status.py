"""Tests for the Meraki Firmware Status sensor."""

from unittest.mock import AsyncMock, MagicMock, PropertyMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.coordinator import MerakiDataUpdateCoordinator
from custom_components.meraki_ha.sensor.meraki_firmware_status import (
    MerakiFirmwareStatusSensor,
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
def device_data_template():
    """Base template for MX device data for firmware tests."""
    return {
        "serial": "QXYZ-9876-WVUT",
        "name": "Test MX Firmware",
        "model": "MX68W",
        "status": "online",
        "mac": "AA:BB:CC:DD:EE:FF",
        "lanIp": "192.168.10.1",
    }


async def test_firmware_sensor_initialization(
    hass: HomeAssistant, mock_coordinator, device_data_template
):
    """Test sensor initialization."""
    device_arg = {
        "serial": device_data_template["serial"],
        "name": device_data_template["name"],
        "model": device_data_template["model"],
    }
    sensor = MerakiFirmwareStatusSensor(mock_coordinator, device_arg)
    sensor.hass = hass

    assert sensor.unique_id == f"{device_data_template['serial']}_firmware_status"
    assert sensor.name == "Firmware Status"
    assert sensor.device_info["identifiers"] == {
        (DOMAIN, device_data_template["serial"])
    }


async def test_firmware_up_to_date(
    hass: HomeAssistant, mock_coordinator, device_data_template
):
    """Test sensor state when firmware is up to date."""
    current_fw = "MX 18.107.1"
    device_firmware_data = {
        **device_data_template,
        "firmware": current_fw,
        "firmware_up_to_date": True,
        "latest_firmware_version": current_fw,
    }
    mock_coordinator.data = {"devices": [device_firmware_data]}
    device_arg = {
        "serial": device_firmware_data["serial"],
        "name": device_firmware_data["name"],
        "model": device_firmware_data["model"],
    }

    sensor = MerakiFirmwareStatusSensor(mock_coordinator, device_arg)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == current_fw
    attrs = sensor.extra_state_attributes
    assert attrs["current_firmware_version"] == current_fw
    assert attrs["firmware_up_to_date"] is True
    assert attrs["latest_available_firmware_version"] == current_fw
    assert attrs["model"] == device_firmware_data["model"]


async def test_firmware_outdated(
    hass: HomeAssistant, mock_coordinator, device_data_template
):
    """Test sensor state when firmware is outdated."""
    current_fw = "MX 17.9.3"
    latest_fw = "MX 18.107.1"
    device_firmware_data = {
        **device_data_template,
        "firmware": current_fw,
        "firmware_up_to_date": False,
        "latest_firmware_version": latest_fw,
    }
    mock_coordinator.data = {"devices": [device_firmware_data]}
    device_arg = {
        "serial": device_firmware_data["serial"],
        "name": device_firmware_data["name"],
        "model": device_firmware_data["model"],
    }

    sensor = MerakiFirmwareStatusSensor(mock_coordinator, device_arg)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == current_fw
    attrs = sensor.extra_state_attributes
    assert attrs["current_firmware_version"] == current_fw
    assert attrs["firmware_up_to_date"] is False
    assert attrs["latest_available_firmware_version"] == latest_fw


async def test_firmware_info_missing_from_fetcher(
    hass: HomeAssistant, mock_coordinator, device_data_template
):
    """Test sensor state when firmware_up_to_date fields are missing (e.g., API error during fetch)."""
    current_fw = "MX 18.100"
    # firmware_up_to_date and latest_firmware_version are missing from device_firmware_data
    device_firmware_data = {
        **device_data_template,
        "firmware": current_fw,
        # "firmware_up_to_date": ..., (missing)
        # "latest_firmware_version": ..., (missing)
    }
    mock_coordinator.data = {"devices": [device_firmware_data]}
    device_arg = {
        "serial": device_firmware_data["serial"],
        "name": device_firmware_data["name"],
        "model": device_firmware_data["model"],
    }

    sensor = MerakiFirmwareStatusSensor(mock_coordinator, device_arg)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == current_fw
    attrs = sensor.extra_state_attributes
    assert attrs["current_firmware_version"] == current_fw
    # Default value for firmware_up_to_date in sensor is False
    assert attrs["firmware_up_to_date"] is False
    # Default value for latest_firmware_version in sensor is "N/A"
    assert attrs["latest_available_firmware_version"] == "N/A"


async def test_firmware_current_version_missing(
    hass: HomeAssistant, mock_coordinator, device_data_template
):
    """Test sensor state when the base 'firmware' field itself is missing."""
    # 'firmware' (current version) is missing
    device_firmware_data = {
        **device_data_template,
        # "firmware": ..., (missing)
        "firmware_up_to_date": True,  # Assume fetcher somehow got this
        "latest_firmware_version": "MX 18.107.1",
    }
    mock_coordinator.data = {"devices": [device_firmware_data]}
    device_arg = {
        "serial": device_firmware_data["serial"],
        "name": device_firmware_data["name"],
        "model": device_firmware_data["model"],
    }

    sensor = MerakiFirmwareStatusSensor(mock_coordinator, device_arg)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == "N/A"  # Default for missing firmware
    attrs = sensor.extra_state_attributes
    assert "current_firmware_version" not in attrs  # Filtered out if None
    assert attrs["firmware_up_to_date"] is True
    assert attrs["latest_available_firmware_version"] == "MX 18.107.1"


async def test_firmware_status_unknown_device_missing(
    hass: HomeAssistant, mock_coordinator, device_data_template
):
    """Test sensor state when device data is missing from coordinator."""
    mock_coordinator.data = {"devices": []}
    device_arg = {
        "serial": device_data_template["serial"],
        "name": device_data_template["name"],
        "model": device_data_template["model"],
    }

    sensor = MerakiFirmwareStatusSensor(mock_coordinator, device_arg)
    sensor.hass = hass
    await sensor.async_added_to_hass()
    mock_coordinator.async_update_listeners()

    assert sensor.native_value == "Unknown"
    assert sensor.extra_state_attributes == {}


async def test_firmware_status_availability(
    hass: HomeAssistant, mock_coordinator, device_data_template
):
    """Test sensor availability."""
    device_arg = {
        "serial": device_data_template["serial"],
        "name": device_data_template["name"],
        "model": device_data_template["model"],
    }
    sensor = MerakiFirmwareStatusSensor(mock_coordinator, device_arg)
    sensor.hass = hass

    type(mock_coordinator).data = PropertyMock(return_value=None)
    assert not sensor.available

    type(mock_coordinator).data = PropertyMock(return_value={"devices": []})
    assert not sensor.available

    type(mock_coordinator).data = PropertyMock(
        return_value={"devices": [device_data_template]}
    )
    sensor._handle_coordinator_update()
    await hass.async_block_till_done()
    assert sensor.available
