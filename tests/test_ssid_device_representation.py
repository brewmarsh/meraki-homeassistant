"""Tests for consistent SSID device representation across all entity types."""

import pytest
from unittest.mock import MagicMock

# Import all the different types of SSID entities
from custom_components.meraki_ha.sensor.network.ssid_availability import MerakiSSIDAvailabilitySensor
from custom_components.meraki_ha.sensor.network.ssid_details import MerakiSSIDWalledGardenSensor
from custom_components.meraki_ha.switch.meraki_ssid_device_switch import MerakiSSIDEnabledSwitch
from custom_components.meraki_ha.text.meraki_ssid_name import MerakiSSIDNameText


@pytest.fixture
def mock_coordinator_and_data():
    """Fixture for a mocked MerakiDataCoordinator and basic data."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}

    ssid_data = {
        "number": 0,
        "name": "Test SSID",
        "networkId": "net1",
        "enabled": True,
    }

    # Mock the client for switch/text entities that need it for API calls
    meraki_client = MagicMock()

    return coordinator, meraki_client, ssid_data


def test_ssid_device_unification(mock_coordinator_and_data):
    """Test that all SSID entity types have the same device info."""
    coordinator, meraki_client, ssid_data = mock_coordinator_and_data
    config_entry = coordinator.config_entry

    # The unique ID for the SSID "device" itself
    # This is based on the logic in device_info_helpers.py
    expected_device_identifier = ("meraki_ha", "net1_0")

    # --- Instantiate one of each type of SSID entity ---

    # 1. A sensor based on MerakiSSIDBaseSensor
    sensor = MerakiSSIDAvailabilitySensor(coordinator, config_entry, ssid_data)

    # 2. A sensor based on MerakiSSIDDetailSensor
    detail_sensor = MerakiSSIDWalledGardenSensor(coordinator, config_entry, ssid_data, None)

    # 3. A switch based on MerakiSSIDBaseSwitch
    # 3. A switch based on MerakiSSIDBaseSwitch
    switch = MerakiSSIDEnabledSwitch(coordinator, meraki_client, config_entry, ssid_data)

    # 4. The text entity
    text = MerakiSSIDNameText(coordinator, meraki_client, config_entry, ssid_data)

    # --- Assertions ---

    # Get the identifiers from each entity's DeviceInfo
    sensor_identifiers = sensor.device_info["identifiers"]
    detail_sensor_identifiers = detail_sensor.device_info["identifiers"]
    switch_identifiers = switch.device_info["identifiers"]
    text_identifiers = text.device_info["identifiers"]

    # Assert that all entities share the exact same device identifier
    assert sensor_identifiers == {expected_device_identifier}
    assert detail_sensor_identifiers == {expected_device_identifier}
    assert switch_identifiers == {expected_device_identifier}
    assert text_identifiers == {expected_device_identifier}

    # As a final check, assert they are all equal to each other
    assert sensor_identifiers == detail_sensor_identifiers == switch_identifiers == text_identifiers
