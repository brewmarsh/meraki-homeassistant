"""Tests for the SwitchPortService."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.services.switch_port_service import SwitchPortService


@pytest.mark.asyncio
async def test_async_get_ports_statuses():
    """Test getting port statuses."""
    # Arrange
    mock_repository = MagicMock()
    mock_repository.async_get_switch_port_statuses = AsyncMock(
        return_value=[{"portId": "1", "status": "Connected"}]
    )
    service = SwitchPortService(mock_repository)
    serial = "Q234-ABCD-5678"

    # Act
    result = await service.async_get_ports_statuses(serial)

    # Assert
    mock_repository.async_get_switch_port_statuses.assert_called_once_with(serial)
    assert result == [{"portId": "1", "status": "Connected"}]


@pytest.mark.asyncio
async def test_async_get_port_status():
    """Test getting a single port's status."""
    # Arrange
    mock_repository = MagicMock()
    mock_repository.async_get_switch_port_statuses = AsyncMock(
        return_value=[
            {"portId": "1", "status": "Connected"},
            {"portId": "2", "status": "Disconnected"},
        ]
    )
    service = SwitchPortService(mock_repository)
    serial = "Q234-ABCD-5678"

    # Act
    result = await service.async_get_port_status(serial, "1")

    # Assert
    assert result == "Connected"


@pytest.mark.asyncio
async def test_async_get_port_speed():
    """Test getting a single port's speed."""
    # Arrange
    mock_repository = MagicMock()
    mock_repository.async_get_switch_port_statuses = AsyncMock(
        return_value=[
            {"portId": "1", "speed": "1000 Mbps"},
            {"portId": "2", "speed": "100 Mbps"},
        ]
    )
    service = SwitchPortService(mock_repository)
    serial = "Q234-ABCD-5678"

    # Act
    result = await service.async_get_port_speed(serial, "1")

    # Assert
    assert result == "1000 Mbps"


@pytest.mark.asyncio
async def test_async_cycle_ports():
    """Test cycling ports."""
    # Arrange
    mock_repository = MagicMock()
    mock_repository.async_cycle_switch_ports = AsyncMock(return_value={})
    service = SwitchPortService(mock_repository)
    serial = "Q234-ABCD-5678"
    ports = ["1"]

    # Act
    await service.async_cycle_ports(serial, ports)

    # Assert
    mock_repository.async_cycle_switch_ports.assert_called_once_with(serial, ports)
