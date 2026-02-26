"""Tests for the Meraki MT40 power outlet switch."""

from typing import Any, Generator, List, Optional
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# Assuming these imports exist in the actual component structure.
# If these modules (client.py, coordinator.py) do not expose MerakiAPIClient
# or MerakiDataCoordinator types, then MagicMock with a spec argument or Any
# would be the appropriate fallback.
from custom_components.meraki_ha.switch.mt40_power_outlet import MerakiMt40PowerOutlet
from custom_components.meraki_ha.types import MerakiDevice


@pytest.fixture
def mock_coordinator_with_mt40_data(
    mock_coordinator: MagicMock,  # This typically mocks MerakiDataCoordinator
) -> MagicMock:
    """Fixture for a mocked MerakiDataCoordinator with MT40 data."""
    device_data: dict[str, Any] = {
        "serial": "mt40-1",
        "name": "MT40 Power Controller",
        "model": "MT40",
        "productType": "sensor",
        "networkId": "net-123",
        "readings": [
            {
                "metric": "downstreamPower",
                "downstreamPower": {"enabled": True},
            },  # Outlet is on
        ],
        "outletStatus": True,
    }
    mock_coordinator.data = {"devices": [MerakiDevice.from_dict(device_data)]}

    mock_coordinator.is_pending = MagicMock(return_value=False)

    def _get_device(serial: str) -> Optional[MerakiDevice]:
        """Helper to simulate the coordinator's get_device method."""
        devices: List[MerakiDevice] = mock_coordinator.data["devices"]
        for d in devices:
            if d.serial == serial:
                return d
        return None

    # Assigning the helper as a side effect for the mocked get_device method
    mock_coordinator.get_device.side_effect = _get_device  # type: ignore[attr-defined] # `get_device` is mocked onto MagicMock
    # Mocking other common coordinator methods expected by HA entities
    mock_coordinator.register_pending_update = MagicMock()
    mock_coordinator.async_request_refresh = AsyncMock()
    return mock_coordinator


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Fixture for a mocked MerakiAPIClient."""
    # Using spec for MagicMock helps ensure the mock matches the API client's interface
    # However, since sensor is an instance attribute not present in the class definition,
    # spec=MerakiAPIClient prevents access to it. We use MagicMock() without spec.
    client = MagicMock()
    client.sensor.create_device_sensor_command = AsyncMock()
    return client


@pytest.fixture
def mt40_power_outlet_switch(
    hass: HomeAssistant,
    mock_coordinator_with_mt40_data: MagicMock,  # Mock of MerakiDataCoordinator
    mock_config_entry: ConfigEntry,
    mock_meraki_client: MagicMock,  # Mock of MerakiAPIClient
) -> Generator[MerakiMt40PowerOutlet, None, None]:
    """Fixture for an initialized MerakiMt40PowerOutlet instance."""
    device_info: MerakiDevice = mock_coordinator_with_mt40_data.data["devices"][0]
    switch = MerakiMt40PowerOutlet(
        mock_coordinator_with_mt40_data,
        device_info,
        mock_config_entry,
        mock_meraki_client,
    )
    switch.hass = hass
    switch.entity_id = "switch.mt40_power_controller_outlet"
    yield switch


def test_mt40_switch_state(
    mt40_power_outlet_switch: MerakiMt40PowerOutlet,
) -> None:
    """Test the initial state and update of the MT40 power outlet switch."""
    switch = mt40_power_outlet_switch

    assert switch.unique_id == "meraki_device_mt40-1_outlet"
    assert switch.name == "Outlet"
    # Initial state might be None depending on initialization, but we check update
    # by simulating a coordinator update.

    # Simulate coordinator update to set the state based on fixture data
    switch._handle_coordinator_update()
    assert switch.is_on is True


@pytest.mark.asyncio
async def test_mt40_turn_on(
    mt40_power_outlet_switch: MerakiMt40PowerOutlet,
    mock_meraki_client: MagicMock,
    mock_coordinator_with_mt40_data: MagicMock,
) -> None:
    """Test turning the MT40 power outlet on."""
    switch = mt40_power_outlet_switch

    await switch.async_turn_on()

    mock_meraki_client.sensor.create_device_sensor_command.assert_called_once_with(
        serial="mt40-1",
        operation="enableDownstreamPower",
    )
    mock_coordinator_with_mt40_data.register_pending_update.assert_called_once_with(
        switch.unique_id
    )


@pytest.mark.asyncio
async def test_mt40_turn_off(
    mt40_power_outlet_switch: MerakiMt40PowerOutlet,
    mock_meraki_client: MagicMock,
    mock_coordinator_with_mt40_data: MagicMock,
) -> None:
    """Test turning the MT40 power outlet off."""
    switch = mt40_power_outlet_switch

    await switch.async_turn_off()

    mock_meraki_client.sensor.create_device_sensor_command.assert_called_once_with(
        serial="mt40-1",
        operation="disableDownstreamPower",
    )
    mock_coordinator_with_mt40_data.register_pending_update.assert_called_once_with(
        switch.unique_id
    )


def test_mt40_availability(
    mt40_power_outlet_switch: MerakiMt40PowerOutlet,
    mock_coordinator_with_mt40_data: MagicMock,
) -> None:
    """Test availability of the MT40 switch."""
    switch = mt40_power_outlet_switch

    # Switch should be available initially based on the coordinator fixture's data
    switch._handle_coordinator_update()  # Ensure initial state is loaded
    assert switch.available is True

    # Simulate a change in the underlying device data in the coordinator
    # and then trigger an update on the switch.
    device_info_in_coordinator: MerakiDevice = mock_coordinator_with_mt40_data.data[
        "devices"
    ][0]
    device_info_in_coordinator.outlet_status = None

    # Trigger an update on the switch to reflect the change in coordinator data
    switch._handle_coordinator_update()
    assert switch.available is False
