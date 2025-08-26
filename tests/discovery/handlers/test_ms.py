"""Tests for the MSHandler."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.discovery.handlers.ms import MSHandler
from custom_components.meraki_ha.binary_sensor.switch_port import SwitchPortSensor


def test_discover_entities():
    """Test that the handler discovers entities correctly."""
    # Arrange
    mock_coordinator = MagicMock()
    mock_config_entry = MagicMock()
    mock_control_service = MagicMock()

    mock_switch_device = {
        "serial": "Q234-ABCD-5678",
        "name": "My Switch",
        "model": "MS220-8P",
        "ports_statuses": [
            {"portId": 1, "status": "Connected"},
            {"portId": 2, "status": "Disconnected"},
        ],
    }

    handler = MSHandler(
        mock_coordinator, mock_switch_device, mock_config_entry, mock_control_service
    )

    # Act
    entities = handler.discover_entities()

    # Assert
    assert len(entities) == 2
    assert isinstance(entities[0], SwitchPortSensor)
    assert entities[0].unique_id == "Q234-ABCD-5678_1"
    assert isinstance(entities[1], SwitchPortSensor)
    assert entities[1].unique_id == "Q234-ABCD-5678_2"
