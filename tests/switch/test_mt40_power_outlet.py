"""Tests for the Meraki MT40 power outlet switch."""

from unittest.mock import MagicMock, AsyncMock

import pytest

from custom_components.meraki_ha.switch.mt40_power_outlet import MerakiMt40PowerOutlet


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "mt40-1",
                "name": "MT40 Power Controller",
                "model": "MT40",
                "productType": "sensor",
                "readings": [
                    {"metric": "downstream_power", "value": True},  # Outlet is on
                ],
            },
        ]
    }
    coordinator.is_pending = MagicMock(return_value=False)
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.data = {
        "api_key": "test_key",
        "org_id": "test_org",
    }
    entry.options = {}
    return entry


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    client.sensor.create_device_sensor_command = AsyncMock()
    return client


def test_mt40_switch_state(hass, mock_coordinator, mock_config_entry, mock_meraki_client):
    """Test the initial state and update of the MT40 power outlet switch."""
    device_info = mock_coordinator.data["devices"][0]
    switch = MerakiMt40PowerOutlet(
        mock_coordinator, device_info, mock_config_entry, mock_meraki_client
    )
    switch.hass = hass
    switch.entity_id = "switch.mt40_power_controller_outlet"

    assert switch.unique_id == "mt40-1-outlet"
    assert switch.name == "MT40 Power Controller Outlet"
    assert switch.is_on is None  # Initial state is None
    assert switch.available is True

    # Simulate coordinator update
    switch._handle_coordinator_update()
    assert switch.is_on is True


@pytest.mark.asyncio
async def test_mt40_turn_on(hass, mock_coordinator, mock_config_entry, mock_meraki_client):
    """Test turning the MT40 power outlet on."""
    device_info = mock_coordinator.data["devices"][0]
    switch = MerakiMt40PowerOutlet(
        mock_coordinator, device_info, mock_config_entry, mock_meraki_client
    )
    switch.hass = hass
    switch.entity_id = "switch.mt40_power_controller_outlet"

    await switch.async_turn_on()

    mock_meraki_client.sensor.create_device_sensor_command.assert_called_once_with(
        serial="mt40-1",
        operation="enableDownstreamPower",
    )
    mock_coordinator.register_pending_update.assert_called_once_with(switch.unique_id)


@pytest.mark.asyncio
async def test_mt40_turn_off(hass, mock_coordinator, mock_config_entry, mock_meraki_client):
    """Test turning the MT40 power outlet off."""
    device_info = mock_coordinator.data["devices"][0]
    switch = MerakiMt40PowerOutlet(
        mock_coordinator, device_info, mock_config_entry, mock_meraki_client
    )
    switch.hass = hass
    switch.entity_id = "switch.mt40_power_controller_outlet"

    await switch.async_turn_off()

    mock_meraki_client.sensor.create_device_sensor_command.assert_called_once_with(
        serial="mt40-1",
        operation="disableDownstreamPower",
    )
    mock_coordinator.register_pending_update.assert_called_once_with(switch.unique_id)


def test_mt40_availability(mock_coordinator, mock_config_entry, mock_meraki_client):
    """Test availability of the MT40 switch."""
    device_info = mock_coordinator.data["devices"][0]
    switch = MerakiMt40PowerOutlet(
        mock_coordinator, device_info, mock_config_entry, mock_meraki_client
    )

    # Switch should be available
    assert switch.available is True

    # Test availability when readings are missing
    device_info["readings"] = []
    assert switch.available is False

    # Test availability when 'readings' key is absent
    del device_info["readings"]
    assert switch.available is False