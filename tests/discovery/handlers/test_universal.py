"""Tests for the UniversalHandler."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.button.reboot import MerakiRebootButton
from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.discovery.handlers.universal import UniversalHandler
from custom_components.meraki_ha.sensor.device.device_status import (
    MerakiDeviceStatusSensor,
)


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
    handler = UniversalHandler.create(
        mock_coordinator,
        device,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

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
    handler = UniversalHandler.create(
        mock_coordinator,
        device,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

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
    handler = UniversalHandler.create(
        mock_coordinator,
        device,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

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
    handler = UniversalHandler.create(
        mock_coordinator,
        device,
        mock_config_entry,
        mock_camera_service,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    assert any(isinstance(e, MerakiRebootButton) for e in entities)
    assert any(isinstance(e, MerakiDeviceStatusSensor) for e in entities)
    # Uplinks are created via UplinkProvider, we can check for their existence if we mock uplink data
    # For now just verify handler creation succeeded
    assert len(entities) >= 2
