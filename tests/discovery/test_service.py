"""Tests for the DeviceDiscoveryService."""

from unittest.mock import MagicMock, patch
import pytest
from custom_components.meraki_ha.discovery.service import DeviceDiscoveryService
from tests.const import MOCK_DEVICE

@pytest.fixture
def mock_org_hub():
    """Fixture for a mocked OrganizationHub."""
    hub = MagicMock()
    wireless_device = MOCK_DEVICE.copy()
    unsupported_device = MOCK_DEVICE.copy()
    unsupported_device["serial"] = "unsupported_serial"
    unsupported_device["productType"] = "unsupported"
    hub.data = {"devices": [wireless_device, unsupported_device]}
    return hub

def test_discovery_service_init(mock_org_hub):
    """Test the initialization of the DeviceDiscoveryService."""
    service = DeviceDiscoveryService(mock_org_hub)
    assert service._org_hub is mock_org_hub
    assert len(service._devices) == 2

def test_discover_entities_delegates_to_handler(mock_org_hub):
    """Test that discover_entities delegates to the correct handler."""
    # Arrange
    mock_mr_handler = MagicMock()
    mock_mr_handler.__name__ = "MRHandler"
    mock_mr_handler.return_value.discover_entities.return_value = ["entity1", "entity2"]

    with patch.dict(
        "custom_components.meraki_ha.discovery.service.HANDLER_MAPPING",
        {"wireless": mock_mr_handler},
    ):
        service = DeviceDiscoveryService(mock_org_hub)

        # Act
        entities = service.discover_entities()

        # Assert
        assert len(entities) == 2
        mock_mr_handler.assert_called_once_with(mock_org_hub.data["devices"][0])
        mock_mr_handler.return_value.discover_entities.assert_called_once()

def test_discover_entities_skips_unsupported_devices(mock_org_hub, caplog):
    """Test that discover_entities skips devices with no handler."""
    # Arrange
    service = DeviceDiscoveryService(mock_org_hub)

    # Act
    entities = service.discover_entities()

    # Assert
    assert len(entities) == 0
    assert "No handler found for product type 'unsupported'" in caplog.text
