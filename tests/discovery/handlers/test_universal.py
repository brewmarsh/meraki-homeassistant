"""Tests for the UniversalHandler."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.button.reboot import MerakiRebootButton
from custom_components.meraki_ha.core.const import DEFAULT_CAPS, DEVICE_CAPABILITIES
from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.discovery.handlers.universal import UniversalHandler
from custom_components.meraki_ha.sensor.device.device_status import (
    MerakiDeviceStatusSensor,
)
from custom_components.meraki_ha.switch.switch_port import MerakiSwitchPortSwitch


@pytest.fixture
def mock_coordinator():
    """Fixture for a mock MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {}
    coordinator.hass = MagicMock()
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Fixture for a mock ConfigEntry."""
    config_entry = MagicMock()
    config_entry.options = {}
    return config_entry


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    return AsyncMock()


@pytest.fixture
def mock_control_service():
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


@pytest.fixture
def mock_network_control_service():
    """Fixture for a mock NetworkControlService."""
    return MagicMock()


@pytest.mark.asyncio
async def test_universal_handler_mt15_no_battery(
    mock_coordinator,
    mock_config_entry,
    mock_camera_service,
    mock_control_service,
    mock_network_control_service,
):
    """Test that MT15 does not have a battery sensor."""
    device = MerakiDevice(serial="mt15-serial", model="MT15")
    handler = UniversalHandler(
        mock_coordinator,
        device,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    # Check that it has CO2 but NOT battery
    keys = [getattr(e, "entity_description", MagicMock()).key for e in entities]
    assert "co2" in keys
    assert "battery" not in keys


@pytest.mark.asyncio
async def test_universal_handler_mt10_has_battery(
    mock_coordinator,
    mock_config_entry,
    mock_camera_service,
    mock_control_service,
    mock_network_control_service,
):
    """Test that MT10 has a battery sensor."""
    device = MerakiDevice(serial="mt10-serial", model="MT10")
    handler = UniversalHandler(
        mock_coordinator,
        device,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    keys = [getattr(e, "entity_description", MagicMock()).key for e in entities]
    assert "battery" in keys
    assert "temperature" in keys


@pytest.mark.asyncio
async def test_universal_handler_unknown_model_default_caps(
    mock_coordinator,
    mock_config_entry,
    mock_camera_service,
    mock_control_service,
    mock_network_control_service,
):
    """Test that an unknown model gets default capabilities (reboot, status)."""
    device = MerakiDevice(serial="unknown-serial", model="UNKNOWN_MODEL")
    handler = UniversalHandler(
        mock_coordinator,
        device,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    assert any(isinstance(e, MerakiRebootButton) for e in entities)
    assert any(isinstance(e, MerakiDeviceStatusSensor) for e in entities)


@pytest.mark.asyncio
async def test_universal_handler_mx_capabilities(
    mock_coordinator,
    mock_config_entry,
    mock_camera_service,
    mock_control_service,
    mock_network_control_service,
):
    """Test that MX67 has expected capabilities."""
    device = MerakiDevice(serial="mx67-serial", model="MX67")
    handler = UniversalHandler(
        mock_coordinator,
        device,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = []
    async for entity in handler.discover_entities():
        entities.append(entity)

    assert any(isinstance(e, MerakiRebootButton) for e in entities)
    assert any(isinstance(e, MerakiDeviceStatusSensor) for e in entities)
    assert len(entities) >= 2


@pytest.mark.asyncio
async def test_universal_handler_capability_compliance(
    mock_coordinator,
    mock_config_entry,
    mock_camera_service,
    mock_control_service,
    mock_network_control_service,
):
    """Specifically verify MT15 vs MT10 compliance as requested."""
    # Test MT15 (Should have CO2, Temp, Humidity, but NO Battery)
    device_mt15 = MerakiDevice(serial="mt15-serial", model="MT15")
    handler_mt15 = UniversalHandler(
        mock_coordinator,
        device_mt15,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities_mt15 = []
    async for entity in handler_mt15.discover_entities():
        entities_mt15.append(entity)

    keys_mt15 = [
        getattr(e, "entity_description", MagicMock()).key for e in entities_mt15
    ]
    assert "co2" in keys_mt15
    assert "temperature" in keys_mt15
    assert "humidity" in keys_mt15
    assert "battery" not in keys_mt15

    # Test MT10 (Should have Temp, Humidity, AND Battery)
    device_mt10 = MerakiDevice(serial="mt10-serial", model="MT10")
    handler_mt10 = UniversalHandler(
        mock_coordinator,
        device_mt10,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities_mt10 = []
    async for entity in handler_mt10.discover_entities():
        entities_mt10.append(entity)

    keys_mt10 = [
        getattr(e, "entity_description", MagicMock()).key for e in entities_mt10
    ]
    assert "temperature" in keys_mt10
    assert "humidity" in keys_mt10
    assert "battery" in keys_mt10


@pytest.mark.asyncio
async def test_universal_handler_unknown_wireless_fallback(
    mock_coordinator,
    mock_config_entry,
    mock_camera_service,
    mock_control_service,
    mock_network_control_service,
):
    """Test that an unknown wireless model gets ssids capability."""
    device = MerakiDevice(
        serial="mr99-serial",
        model="MR99",
        product_type="wireless",
    )

    handler = UniversalHandler(
        mock_coordinator,
        device,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    assert "ssids" in handler.capabilities
