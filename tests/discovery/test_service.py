"""Tests for the DeviceDiscoveryService."""

from unittest.mock import MagicMock, patch
import pytest
from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from tests.const import MOCK_DEVICE

@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    wireless_device = MOCK_DEVICE.copy()
    camera_device = MOCK_DEVICE.copy()
    camera_device["serial"] = "camera_serial"
    camera_device["productType"] = "camera"
    unsupported_device = MOCK_DEVICE.copy()
    unsupported_device["serial"] = "unsupported_serial"
    unsupported_device["productType"] = "unsupported"
    coordinator.data = {
        "devices": [wireless_device, camera_device, unsupported_device]
    }
    return coordinator

def test_discovery_service_init(mock_coordinator):
    """Test the initialization of the DeviceDiscoveryService."""
    mock_config_entry = MagicMock()
    service = DeviceDiscoveryService(mock_coordinator, mock_config_entry)
    assert service._coordinator is mock_coordinator
    assert len(service._devices) == 3

def test_discover_entities_delegates_to_handler(mock_coordinator, caplog):
    """Test that discover_entities delegates to the correct handlers."""
    # Arrange
    mock_mr_handler = MagicMock()
    mock_mr_handler.__name__ = "MRHandler"
    mock_mr_handler.return_value.discover_entities.return_value = ["mr_entity"]

    mock_mv_handler = MagicMock()
    mock_mv_handler.__name__ = "MVHandler"
    mock_mv_handler.return_value.discover_entities.return_value = ["mv_entity"]

    mock_config_entry = MagicMock()

    with patch.dict(
        "custom_components.meraki_ha.discovery.service.HANDLER_MAPPING",
        {"wireless": mock_mr_handler, "camera": mock_mv_handler},
    ) as HANDLER_MAPPING:
        service = DeviceDiscoveryService(mock_coordinator, mock_config_entry)

        # Act
        entities = service.discover_entities()

        # Assert
        assert len(entities) == 2
        assert "mr_entity" in entities
        assert "mv_entity" in entities
        mock_mr_handler.assert_called_once_with(
            mock_coordinator, mock_coordinator.data["devices"][0], mock_config_entry
        )
        mock_mv_handler.assert_called_once_with(
            mock_coordinator, mock_coordinator.data["devices"][1], mock_config_entry
        )
        assert "No handler found for product type 'unsupported'" in caplog.text
