"""Tests for the MGHandler (Cellular Gateway)."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.const import CONF_ENABLE_DEVICE_STATUS
from custom_components.meraki_ha.discovery.handlers.mg import MGHandler
from custom_components.meraki_ha.types import MerakiDevice

MOCK_MG_DEVICE: MerakiDevice = {
    "serial": "MG-001-TEST",
    "name": "Test MG Gateway",
    "model": "MG21",
    "networkId": "N_12345",
    "productType": "cellularGateway",
    "lanIp": "10.0.0.1",
    "status": "online",
}


@pytest.fixture
def mock_control_service() -> MagicMock:
    """Fixture for a mock DeviceControlService."""
    return MagicMock()


@pytest.fixture
def mock_network_control_service() -> MagicMock:
    """Fixture for a mock NetworkControlService."""
    return MagicMock()


@pytest.mark.asyncio
async def test_mg_handler_initialization(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test that MGHandler initializes correctly with network_control_service."""
    handler = MGHandler(
        mock_coordinator,
        MOCK_MG_DEVICE,
        mock_config_entry,
        mock_control_service,
        mock_network_control_service,
    )

    assert handler._coordinator is mock_coordinator
    assert handler.device == MOCK_MG_DEVICE
    assert handler._config_entry is mock_config_entry
    assert handler._control_service is mock_control_service
    assert handler._network_control_service is mock_network_control_service


@pytest.mark.asyncio
async def test_mg_handler_discover_entities_with_device_status_enabled(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test discover_entities returns expected entities with device status enabled."""
    mock_config_entry.options = {CONF_ENABLE_DEVICE_STATUS: True}

    handler = MGHandler(
        mock_coordinator,
        MOCK_MG_DEVICE,
        mock_config_entry,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    # Should create: RebootButton, DeviceStatusSensor, CellularUplink, CellularSignal
    assert len(entities) == 4

    entity_types = [type(e).__name__ for e in entities]
    assert "MerakiRebootButton" in entity_types
    assert "MerakiDeviceStatusSensor" in entity_types
    assert "MerakiCellularUplinkSensor" in entity_types
    assert "MerakiCellularSignalSensor" in entity_types


@pytest.mark.asyncio
async def test_mg_handler_discover_entities_with_device_status_disabled(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test discover_entities excludes DeviceStatusSensor when disabled."""
    mock_config_entry.options = {CONF_ENABLE_DEVICE_STATUS: False}

    handler = MGHandler(
        mock_coordinator,
        MOCK_MG_DEVICE,
        mock_config_entry,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    # Should create: RebootButton, CellularUplink, CellularSignal (no DeviceStatus)
    assert len(entities) == 3

    entity_types = [type(e).__name__ for e in entities]
    assert "MerakiRebootButton" in entity_types
    assert "MerakiDeviceStatusSensor" not in entity_types
    assert "MerakiCellularUplinkSensor" in entity_types
    assert "MerakiCellularSignalSensor" in entity_types


@pytest.mark.asyncio
async def test_mg_handler_discover_entities_default_device_status(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_control_service: MagicMock,
    mock_network_control_service: MagicMock,
) -> None:
    """Test that device status is enabled by default when not specified."""
    mock_config_entry.options = {}  # No explicit setting

    handler = MGHandler(
        mock_coordinator,
        MOCK_MG_DEVICE,
        mock_config_entry,
        mock_control_service,
        mock_network_control_service,
    )

    entities = await handler.discover_entities()

    # Default is True, so DeviceStatusSensor should be included
    assert len(entities) == 4

    entity_types = [type(e).__name__ for e in entities]
    assert "MerakiDeviceStatusSensor" in entity_types
