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
    mock_control_service = MagicMock()
<<<<<<< HEAD
    mock_switch_port_coordinator = MagicMock()
=======
    mock_network_control_service = MagicMock()
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    mock_switch_device = {
        "serial": "Q234-ABCD-5678",
        "name": "My Switch",
        "model": "MS220-8P",
        "ports_statuses": [
            {"portId": 1, "enabled": True},
            {"portId": 2, "enabled": True},
        ],
    }

    handler = MSHandler(
        mock_coordinator,
        mock_switch_device,
        mock_config_entry,
<<<<<<< HEAD
        mock_switch_port_coordinator,
        mock_control_service,
=======
        mock_control_service,
        mock_network_control_service,
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    )

    # Act
    entities = await handler.discover_entities()

    # Assert
    assert len(entities) == 2
