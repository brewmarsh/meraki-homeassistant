"""Tests for Meraki availability edge cases."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.entity import MerakiEntity


@pytest.fixture
def mock_coordinator_availability():
    """Fixture for a mocked coordinator with specific device status."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices_by_serial": {
            "online_serial": {"serial": "online_serial", "status": "online"},
            "alerting_serial": {"serial": "alerting_serial", "status": "alerting"},
            "dormant_serial": {"serial": "dormant_serial", "status": "dormant"},
            "offline_serial": {"serial": "offline_serial", "status": "offline"},
            "unknown_serial": {"serial": "unknown_serial", "status": "something_else"},
            "dict_online": {"serial": "dict_online", "status": "online"},
        }
    }
    return coordinator


def test_meraki_entity_availability_statuses(mock_coordinator_availability):
    """Test that MerakiEntity reports available for correct statuses."""
    # Online
    entity_online = MerakiEntity(mock_coordinator_availability)
    entity_online._device_serial = "online_serial"
    assert entity_online.available is True

    # Alerting
    entity_alerting = MerakiEntity(mock_coordinator_availability)
    entity_alerting._device_serial = "alerting_serial"
    assert entity_alerting.available is True

    # Dormant
    entity_dormant = MerakiEntity(mock_coordinator_availability)
    entity_dormant._device_serial = "dormant_serial"
    assert entity_dormant.available is True

    # Offline
    entity_offline = MerakiEntity(mock_coordinator_availability)
    entity_offline._device_serial = "offline_serial"
    assert entity_offline.available is False

    # Unknown/Other
    entity_unknown = MerakiEntity(mock_coordinator_availability)
    entity_unknown._device_serial = "unknown_serial"
    assert entity_unknown.available is False


def test_meraki_entity_availability_no_data(mock_coordinator_availability):
    """Test availability when coordinator has no data."""
    mock_coordinator_availability.data = None
    entity = MerakiEntity(mock_coordinator_availability)
    entity._device_serial = "online_serial"
    assert entity.available is False


def test_meraki_entity_availability_missing_serial(mock_coordinator_availability):
    """Test availability when serial is not in coordinator data."""
    entity = MerakiEntity(mock_coordinator_availability)
    entity._device_serial = "missing_serial"
    assert entity.available is False


def test_meraki_entity_availability_no_serial_attribute(mock_coordinator_availability):
    """Test availability when entity has no serial attribute (e.g. network entity)."""
    entity = MerakiEntity(mock_coordinator_availability)
    # No _device_serial, _serial, etc.
    assert entity.available is True
