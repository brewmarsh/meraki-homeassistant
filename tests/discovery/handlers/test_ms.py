"""Tests for the MSHandler."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.discovery.handlers.ms import MSHandler
<<<<<<< HEAD
=======
from custom_components.meraki_ha.types import MerakiDevice
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)


@pytest.mark.asyncio
async def test_discover_entities():
    """Test that the handler discovers entities correctly."""
    # Arrange
    mock_coordinator = MagicMock()
    mock_config_entry = MagicMock()
    mock_control_service = MagicMock()
<<<<<<< HEAD
    mock_network_control_service = MagicMock()
    mock_switch_device = {
        "serial": "Q234-ABCD-5678",
        "name": "My Switch",
        "model": "MS220-8P",
        "ports_statuses": [
            {"portId": 1, "enabled": True},
            {"portId": 2, "enabled": True},
        ],
    }
=======
    mock_switch_port_coordinator = MagicMock()
    mock_switch_device = MerakiDevice(
        serial="Q234-ABCD-5678",
        name="My Switch",
        model="MS220-8P",
        mac="00:11:22:33:44:55",
        ports_statuses=[
            {"portId": 1, "enabled": True},
            {"portId": 2, "enabled": True},
        ],
    )
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)

    handler = MSHandler(
        mock_coordinator,
        mock_switch_device,
        mock_config_entry,
<<<<<<< HEAD
        mock_control_service,
        mock_network_control_service,
=======
        mock_switch_port_coordinator,
        mock_control_service,
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    )

    # Act
    entities = await handler.discover_entities()

    # Assert
    assert len(entities) == 2
