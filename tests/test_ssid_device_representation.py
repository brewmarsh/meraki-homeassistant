"""Tests for consistent SSID device representation across all entity types."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.meraki_select.rf_profile import (
    MerakiRFProfileSelect,
)
from custom_components.meraki_ha.sensor.network.ssid_availability import (
    MerakiSSIDAvailabilitySensor,
)
from custom_components.meraki_ha.sensor.network.ssid_details import (
    MerakiSSIDWalledGardenSensor,
)
from custom_components.meraki_ha.switch.meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
)
from custom_components.meraki_ha.text.meraki_ssid_name import MerakiSSIDNameText


@pytest.fixture
def mock_coordinator_and_data() -> tuple[MagicMock, MagicMock, dict[str, Any]]:
    """Fixture for a mocked MerakiDataUpdateCoordinator and basic data."""
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


def test_ssid_device_unification(
    mock_coordinator_and_data: tuple[MagicMock, MagicMock, dict[str, Any]],
) -> None:
    """
    Test that all SSID entity types have the same device info (Virtual Controller).

    Args:
    ----
        mock_coordinator_and_data: The mocked coordinator and data.

    """
    coordinator, meraki_client, ssid_data = mock_coordinator_and_data
    config_entry = coordinator.config_entry

    # The unique ID for the SSID "device" itself (Now Virtual Controller)
    expected_device_identifier = ("meraki_ha", "network_net1")

    # --- Instantiate one of each type of SSID entity ---

    # 1. A sensor based on MerakiSSIDBaseSensor
    sensor = MerakiSSIDAvailabilitySensor(coordinator, config_entry, ssid_data)

    # 2. A sensor based on MerakiSSIDDetailSensor
    detail_sensor = MerakiSSIDWalledGardenSensor(
        coordinator,
        config_entry,
        ssid_data,
        None,
    )

    # 3. A switch based on MerakiSSIDBaseSwitch
    switch = MerakiSSIDEnabledSwitch(
        coordinator,
        meraki_client,
        config_entry,
        ssid_data,
    )

    # 4. The text entity
    text = MerakiSSIDNameText(coordinator, meraki_client, config_entry, ssid_data)

    # 5. The RF profile select entity
    rf_select = MerakiRFProfileSelect(
        coordinator,
        meraki_client,
        config_entry,
        ssid_data,
    )

    # --- Assertions ---

    # Get the identifiers from each entity's DeviceInfo
    sensor_device_info = sensor.device_info
    assert sensor_device_info is not None
    sensor_identifiers = sensor_device_info["identifiers"]

    # Refactor: Name is no longer present in SSID entity device_info
    assert "name" not in sensor_device_info

    detail_sensor_device_info = detail_sensor.device_info
    assert detail_sensor_device_info is not None
    detail_sensor_identifiers = detail_sensor_device_info["identifiers"]

    switch_device_info = switch.device_info
    assert switch_device_info is not None
    switch_identifiers = switch_device_info["identifiers"]

    text_device_info = text.device_info
    assert text_device_info is not None
    text_identifiers = text_device_info["identifiers"]

    rf_select_device_info = rf_select.device_info
    assert rf_select_device_info is not None
    rf_select_identifiers = rf_select_device_info["identifiers"]

    # Assert that all entities share the exact same device identifier (Network Device)
    assert sensor_identifiers == {expected_device_identifier}
    assert detail_sensor_identifiers == {expected_device_identifier}
    assert switch_identifiers == {expected_device_identifier}
    assert text_identifiers == {expected_device_identifier}
    assert rf_select_identifiers == {expected_device_identifier}

    # As a final check, assert they are all equal to each other
    assert (
        sensor_identifiers
        == detail_sensor_identifiers
        == switch_identifiers
        == text_identifiers
        == rf_select_identifiers
    )

    # Verify via_device is NOT present (as it attaches directly to the device)
    assert "via_device" not in sensor_device_info
