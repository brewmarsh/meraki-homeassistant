"""Tests for the SwitchHandler."""

from unittest.mock import MagicMock, patch

import pytest

from custom_components.meraki_ha.button.device.poe_cycle import MerakiPoECycleButton
from custom_components.meraki_ha.const.config import CONF_ENABLE_PORT_SENSORS, from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.discovery.handlers.switch import SwitchHandler
from custom_components.meraki_ha.sensor.device.switch_client_count import (
    MerakiSwitchClientCountSensor,
)
from custom_components.meraki_ha.switch.switch_port import MerakiSwitchPortToggle


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiMainCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {}
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Fixture for a mock ConfigEntry."""
    config_entry = MagicMock()
    config_entry.options = {"enable_port_sensors": False}
    return config_entry


@pytest.mark.asyncio
async def test_switch_handler_exclusion_logic(mock_coordinator, mock_config_entry):
    """Test that SwitchHandler excludes appliances and Z3 devices."""
    # Disable port sensors to simplify entity count assertion
    mock_config_entry.options = {CONF_ENABLE_PORT_SENSORS: False}

    # Define devices with ports to satisfy reviewer concern
    mx_appliance = MerakiDevice(
        serial="MX_SERIAL",
        model="MX64",
        product_type="appliance",
        switch_ports=[{"portId": "1", "enabled": True}],
    )
    z3_appliance = MerakiDevice(
        serial="Z3_SERIAL",
        model="Z3",
        product_type="appliance",
        switch_ports=[{"portId": "1", "enabled": True}],
    )
    # Some devices might have product_type="switch" but are MX models
    mx_labeled_switch = MerakiDevice(
        serial="MX_SWITCH_SERIAL",
        model="MX67",
        product_type="switch",
        switch_ports=[{"portId": "1", "enabled": True}],
    )
    normal_switch = MerakiDevice(
        serial="MS_SERIAL",
        model="MS120",
        product_type="switch",
        switch_ports=[{"portId": "1", "enabled": True}],
    )
    wireless_device = MerakiDevice(
        serial="MR_SERIAL", model="MR36", product_type="wireless"
    )

    mock_coordinator.data = {
        "devices": [
            mx_appliance,
            z3_appliance,
            mx_labeled_switch,
            normal_switch,
            wireless_device,
        ]
    }

    handler = SwitchHandler(mock_coordinator, mock_config_entry)

    with patch(
        "custom_components.meraki_ha.discovery.handlers.switch._LOGGER"
    ) as mock_logger:
        entities = []
        async for entity in handler.discover_entities():
            entities.append(entity)

        # Assertions
        # Should only have 1 entity (the normal switch's client count)
        # Even though appliances have ports_statuses, SwitchHandler doesn't yield
        # port sensors, and it should skip processing them entirely due to
        # the new logic.
        assert len(entities) == 1
        assert isinstance(entities[0], MerakiSwitchClientCountSensor)
        assert entities[0]._device_serial == "MS_SERIAL"

        # Check debug logs for skips
        # MX_SERIAL (product_type="appliance")
        # Z3_SERIAL (product_type="appliance")
        # MX_SWITCH_SERIAL (model starts with "MX")
        assert mock_logger.debug.call_count == 3

        # Verify specific skip messages
        skip_calls = [call.args[1] for call in mock_logger.debug.call_args_list]
        assert "MX_SERIAL" in skip_calls
        assert "Z3_SERIAL" in skip_calls
        assert "MX_SWITCH_SERIAL" in skip_calls


@pytest.mark.asyncio
async def test_switch_handler_unknown_model_fallback(
    mock_coordinator, mock_config_entry
):
    """Test that an unknown switch model (e.g. MS390) gets switch_ports capability."""
    # Ensure port sensors are enabled
    mock_config_entry.options = {CONF_ENABLE_PORT_SENSORS: True}

    # MS390 is not in DEVICE_CAPABILITIES usually, but product_type="switch"
    device = MerakiDevice(
        serial="ms390-serial",
        model="MS390",
        product_type="switch",
        switch_ports=[{"portId": "1", "enabled": True}],
    )

    mock_coordinator.data = {"devices": [device]}

    handler = SwitchHandler(mock_coordinator, mock_config_entry)

    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    # Expected entities:
    # 1. MerakiSwitchClientCountSensor
    # 2. SwitchPortSensor
    # 3. MerakiSwitchPortSensor
    # 4. MerakiSwitchPortPowerSensor
    # 5. MerakiSwitchPortEnergySensor
    # 6. MerakiSwitchPortToggle
    # 7. MerakiPoECycleButton

    assert len(entities) == 7
    # Check if switch port switch entity is present
    assert any(isinstance(e, MerakiSwitchPortToggle) for e in entities)
    # Check if client count sensor is present
    assert any(isinstance(e, MerakiSwitchClientCountSensor) for e in entities)
    # Check if PoE cycle button is present
    assert any(isinstance(e, MerakiPoECycleButton) for e in entities)


@pytest.mark.asyncio
async def test_switch_handler_no_data(mock_coordinator, mock_config_entry):
    """Test SwitchHandler with no coordinator data."""
    mock_coordinator.data = None
    handler = SwitchHandler(mock_coordinator, mock_config_entry)

    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    assert len(entities) == 0
