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
<<<<<<< HEAD
    mock_switch_port_coordinator = MagicMock()
=======
<<<<<<< HEAD
    mock_switch_port_coordinator = MagicMock()
=======
    mock_network_control_service = MagicMock()
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    mock_network_control_service = MagicMock()
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
        mock_switch_port_coordinator,
        mock_control_service,
=======
<<<<<<< HEAD
        mock_switch_port_coordinator,
        mock_control_service,
=======
        mock_control_service,
        mock_network_control_service,
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
        mock_control_service,
        mock_network_control_service,
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
    )

    # Act
    entities = await handler.discover_entities()

    # Assert
    assert len(entities) == 2
