"""Tests for Meraki Appliance Port discovery."""

from unittest.mock import MagicMock
import pytest
from custom_components.meraki_ha.discovery.providers.appliance import AppliancePortProvider
from custom_components.meraki_ha.const.config import CONF_ENABLE_PORT_SENSORS
from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.core.models.appliance import MerakiAppliancePort
from custom_components.meraki_ha.sensor.device.appliance_port import MerakiAppliancePortSensor
from custom_components.meraki_ha.binary_sensor.device.appliance_port import AppliancePortBinarySensor
from custom_components.meraki_ha.switch.switch_port import MerakiAppliancePortSwitch

@pytest.fixture
def mock_coordinator():
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    return coordinator

@pytest.fixture
def mock_device():
    device = MerakiDevice(
        serial="dev1",
        name="Appliance",
        model="MX64",
        product_type="appliance",
    )
    device.appliance_ports = [
        MerakiAppliancePort(number=1, enabled=True, status="connected")
    ]
    return device

@pytest.fixture
def mock_config_entry():
    config_entry = MagicMock()
    config_entry.options = {CONF_ENABLE_PORT_SENSORS: True}
    return config_entry

def test_appliance_port_discovery_enabled(mock_coordinator, mock_device, mock_config_entry):
    """Test that appliance ports are discovered when enabled."""
    entities = AppliancePortProvider.get_entities(mock_coordinator, mock_device, mock_config_entry)

    assert len(entities) > 0
    # Should find binary sensor, sensor, and switch
    assert any(isinstance(e, AppliancePortBinarySensor) for e in entities)
    assert any(isinstance(e, MerakiAppliancePortSensor) for e in entities)
    assert any(isinstance(e, MerakiAppliancePortSwitch) for e in entities)

def test_appliance_port_discovery_disabled(mock_coordinator, mock_device):
    """Test that appliance ports are not discovered when disabled."""
    mock_config_entry = MagicMock()
    mock_config_entry.options = {CONF_ENABLE_PORT_SENSORS: False}

    entities = AppliancePortProvider.get_entities(mock_coordinator, mock_device, mock_config_entry)

    assert len(entities) == 0

def test_appliance_port_discovery_with_ports_dict(mock_coordinator, mock_config_entry):
    """Test discovery using the device.ports dictionary."""
    device = MerakiDevice(
        serial="dev1",
        name="Appliance",
        model="MX64",
        product_type="appliance",
    )
    device.ports = {
        "1": {"number": 1, "enabled": True, "status": "connected"}
    }

    entities = AppliancePortProvider.get_entities(mock_coordinator, device, mock_config_entry)

    assert len(entities) > 0
    assert any(isinstance(e, AppliancePortBinarySensor) for e in entities)
    assert any(isinstance(e, MerakiAppliancePortSensor) for e in entities)
    assert any(isinstance(e, MerakiAppliancePortSwitch) for e in entities)
