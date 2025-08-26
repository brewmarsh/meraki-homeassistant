"""Tests for the MSHandler."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.discovery.handlers.ms import MSHandler


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
    }

    handler = MSHandler(
        mock_coordinator, mock_switch_device, mock_config_entry, mock_control_service
    )

    # Act
    entities = handler.discover_entities()

    # Assert
    assert len(entities) == 0
