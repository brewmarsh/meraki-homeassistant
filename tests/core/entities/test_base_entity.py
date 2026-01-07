"""Tests for core/entities/__init__.py module."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.core.entities import BaseMerakiEntity


@pytest.fixture
def mock_entity_coordinator() -> MagicMock:
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.last_update_success = True
    coordinator.data = {
        "devices": [{"serial": "SW-001", "name": "Test Switch", "status": "online"}],
        "networks": [{"id": "N_123", "name": "Test Network"}],
    }
    coordinator.get_device = MagicMock(
        return_value={"serial": "SW-001", "name": "Test Switch", "status": "online"}
    )
    coordinator.get_network = MagicMock(
        return_value={"id": "N_123", "name": "Test Network"}
    )
    return coordinator


class ConcreteBaseMerakiEntity(BaseMerakiEntity):
    """Concrete implementation for testing."""

    def __init__(self, coordinator, config_entry, serial=None, network_id=None):
        """Initialize test entity."""
        super().__init__(coordinator, config_entry, serial, network_id)
        self._attr_name = "Test Entity"


def test_base_entity_initialization_with_serial(
    mock_entity_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test BaseMerakiEntity initialization with serial."""
    entity = ConcreteBaseMerakiEntity(
        coordinator=mock_entity_coordinator,
        config_entry=mock_config_entry,
        serial="SW-001",
    )

    assert entity._serial == "SW-001"
    assert entity._network_id is None


def test_base_entity_initialization_with_network_id(
    mock_entity_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test BaseMerakiEntity initialization with network_id."""
    entity = ConcreteBaseMerakiEntity(
        coordinator=mock_entity_coordinator,
        config_entry=mock_config_entry,
        network_id="N_123",
    )

    assert entity._network_id == "N_123"
    assert entity._serial is None


def test_base_entity_device_info_for_device(
    mock_entity_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test device_info for device-based entity."""
    entity = ConcreteBaseMerakiEntity(
        coordinator=mock_entity_coordinator,
        config_entry=mock_config_entry,
        serial="SW-001",
    )

    device_info = entity.device_info

    assert device_info is not None


def test_base_entity_device_info_for_network(
    mock_entity_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test device_info for network-based entity."""
    entity = ConcreteBaseMerakiEntity(
        coordinator=mock_entity_coordinator,
        config_entry=mock_config_entry,
        network_id="N_123",
    )

    device_info = entity.device_info

    assert device_info is not None


def test_base_entity_available_with_device(
    mock_entity_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test available property for device-based entity."""
    entity = ConcreteBaseMerakiEntity(
        coordinator=mock_entity_coordinator,
        config_entry=mock_config_entry,
        serial="SW-001",
    )

    assert entity.available is True


def test_base_entity_available_offline_device(
    mock_entity_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test available property when device is offline."""
    mock_entity_coordinator.get_device = MagicMock(
        return_value={"serial": "SW-001", "status": "offline"}
    )

    entity = ConcreteBaseMerakiEntity(
        coordinator=mock_entity_coordinator,
        config_entry=mock_config_entry,
        serial="SW-001",
    )

    assert entity.available is False


def test_base_entity_available_coordinator_failed(
    mock_entity_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test available property when coordinator update failed."""
    mock_entity_coordinator.last_update_success = False

    entity = ConcreteBaseMerakiEntity(
        coordinator=mock_entity_coordinator,
        config_entry=mock_config_entry,
        serial="SW-001",
    )

    assert entity.available is False


def test_base_entity_entity_category(
    mock_entity_coordinator: MagicMock,
    mock_config_entry: MagicMock,
) -> None:
    """Test entity_category returns None by default."""
    entity = ConcreteBaseMerakiEntity(
        coordinator=mock_entity_coordinator,
        config_entry=mock_config_entry,
        serial="SW-001",
    )

    assert entity.entity_category is None
