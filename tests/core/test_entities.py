"""Tests for BaseMerakiEntity."""

from unittest.mock import MagicMock
import pytest
from custom_components.meraki_ha.core.entities import BaseMerakiEntity
from custom_components.meraki_ha.types import MerakiDevice, MerakiNetwork


class MockEntity(BaseMerakiEntity):
    """Mock entity for testing."""

    def __init__(self, coordinator, config_entry, serial=None, network_id=None):
        super().__init__(coordinator, config_entry, serial, network_id)


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()

    device = MerakiDevice(
        serial="Q2XX-XXXX-XXXX",
        name="Device 1",
        model="MR56",
        mac="00:11:22:33:44:55",
        status="online",
        product_type="wireless",
        firmware="MR 27.1",
        address="123 Street",
        url="https://dashboard.meraki.com/device",
    )

    network = MerakiNetwork(
        id="N_12345",
        name="Network 1",
        organization_id="123",
        product_types=["wireless"],
        time_zone="America/Los_Angeles",
    )

    coordinator.data = {
        "devices": [device],
        "networks": [network]
    }

    coordinator.get_device.return_value = device
    coordinator.get_network.return_value = network
    coordinator.last_update_success = True

    return coordinator


def test_base_meraki_entity_device(mock_coordinator):
    """Test BaseMerakiEntity with a device."""
    config_entry = MagicMock()
    config_entry.options = {}

    entity = MockEntity(mock_coordinator, config_entry, serial="Q2XX-XXXX-XXXX")

    assert entity.available is True

    # Verify DeviceInfo
    device_info = entity.device_info
    assert device_info["identifiers"] == {("meraki_ha", "Q2XX-XXXX-XXXX")}
    assert device_info["model"] == "MR56"
    assert device_info["sw_version"] == "MR 27.1"
    assert device_info["suggested_area"] == "123 Street"
    assert device_info["configuration_url"] == "https://dashboard.meraki.com/device"


def test_base_meraki_entity_network(mock_coordinator):
    """Test BaseMerakiEntity with a network."""
    config_entry = MagicMock()
    config_entry.options = {}

    entity = MockEntity(mock_coordinator, config_entry, network_id="N_12345")

    assert entity.available is True

    # Verify DeviceInfo
    device_info = entity.device_info
    assert device_info["identifiers"] == {("meraki_ha", "network_N_12345")}
    assert device_info["model"] == "Network"
    assert device_info["sw_version"] == "unknown"


def test_base_meraki_entity_unavailable(mock_coordinator):
    """Test BaseMerakiEntity unavailability."""
    config_entry = MagicMock()
    config_entry.options = {}

    mock_coordinator.last_update_success = False
    entity = MockEntity(mock_coordinator, config_entry, serial="Q2XX-XXXX-XXXX")
    assert entity.available is False

    mock_coordinator.last_update_success = True

    # Device offline
    device = mock_coordinator.get_device.return_value
    device.status = "offline"
    entity = MockEntity(mock_coordinator, config_entry, serial="Q2XX-XXXX-XXXX")
    assert entity.available is False
