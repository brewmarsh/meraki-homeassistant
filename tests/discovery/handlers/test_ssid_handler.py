"""Tests for the SSIDHandler."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from custom_components.meraki_ha.discovery.handlers.ssid import SSIDHandler
from custom_components.meraki_ha.switch.meraki_ssid_device_switch import (
    MerakiSSIDEnabledSwitch,
    MerakiSSIDBroadcastSwitch,
)
from custom_components.meraki_ha.text.meraki_ssid_name import MerakiSSIDNameText
from custom_components.meraki_ha.sensor.network.ssid_client_count import (
    MerakiSSIDClientCountSensor,
)

from tests.const import MOCK_SSID, MOCK_CONFIG_ENTRY_ID


@pytest.fixture
def mock_coordinator():
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock()
    coordinator.data = {"ssids": [MOCK_SSID], "rf_profiles": {}}
    return coordinator


@pytest.fixture
def mock_config_entry():
    """Fixture for a mocked config entry."""
    entry = MagicMock()
    entry.entry_id = MOCK_CONFIG_ENTRY_ID
    return entry


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked MerakiAPIClient."""
    return AsyncMock()


@pytest.mark.asyncio
async def test_ssid_handler_discover_entities(
    mock_coordinator, mock_config_entry, mock_meraki_client
):
    """Test that the SSIDHandler discovers the correct entities."""
    handler = SSIDHandler(mock_coordinator, mock_config_entry, mock_meraki_client)
    entities = await handler.discover_entities()

    # There are 2 switches, 1 text, and 20 sensors = 23 entities
    assert len(entities) == 23

    # Check that the entities are of the correct type
    assert any(isinstance(e, MerakiSSIDEnabledSwitch) for e in entities)
    assert any(isinstance(e, MerakiSSIDBroadcastSwitch) for e in entities)
    assert any(isinstance(e, MerakiSSIDNameText) for e in entities)
    assert any(isinstance(e, MerakiSSIDClientCountSensor) for e in entities)

    # Check that all entities have a device_info attribute
    for entity in entities:
        assert entity.device_info is not None

    # Check that all entities are linked to the same device
    device_identifiers = [e.device_info["identifiers"] for e in entities]
    assert len(set(device_identifiers)) == 1
