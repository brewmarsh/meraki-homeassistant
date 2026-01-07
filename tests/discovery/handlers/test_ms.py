"""Tests for the MSHandler."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.discovery.handlers.ms import MSHandler


@pytest.mark.asyncio
async def test_discover_entities():
    """Test that the handler discovers entities correctly."""
    # Arrange
    mock_coordinator = MagicMock()
    mock_config_entry = MagicMock()
    mock_config_entry.options = {
        "enable_device_status": True,
        "enable_port_sensors": True,
    }
    mock_control_service = MagicMock()
    mock_network_control_service = MagicMock()
    mock_switch_device = {
        "serial": "Q234-ABCD-5678",
        "name": "My Switch",
        "model": "MS220-8P",
        "ports_statuses": [
            {"portId": "1", "enabled": True, "status": "Connected"},
            {"portId": "2", "enabled": True, "status": "Disconnected"},
        ],
    }

    handler = MSHandler(
        mock_coordinator,
        mock_switch_device,
        mock_config_entry,
        mock_control_service,
        mock_network_control_service,
    )

    # Act
    entities = await handler.discover_entities()

    # Assert
    # MS handler creates: RebootButton, DeviceStatusSensor, ConnectedClientsSensor,
    # PoEUsageSensor, and 2 port sensors = 6 total
    assert len(entities) == 6

    entity_types = [type(e).__name__ for e in entities]
    assert "MerakiRebootButton" in entity_types
    assert "MerakiDeviceStatusSensor" in entity_types
    assert "MerakiDeviceConnectedClientsSensor" in entity_types
    assert "MerakiPoeUsageSensor" in entity_types
    assert entity_types.count("SwitchPortSensor") == 2
