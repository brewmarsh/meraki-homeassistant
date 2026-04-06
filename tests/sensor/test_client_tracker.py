"""Tests for the Meraki client tracker sensor."""

from unittest.mock import MagicMock
import pytest

from custom_components.meraki_ha.sensor.client_tracker import (
    ClientTrackerDeviceSensor,
    MerakiClientSensor,
)
from custom_components.meraki_ha.const.integration import DOMAIN

@pytest.mark.asyncio
async def test_client_tracker_device_sensor():
    """Test the ClientTrackerDeviceSensor."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = {}
    mock_config_entry = MagicMock()

    # Mock async_write_ha_state to avoid needing a full hass setup
    with MagicMock() as mock_write:
        # We need to patch it on the instance after creation or on the class
        sensor = ClientTrackerDeviceSensor(mock_coordinator, mock_config_entry)
        sensor.hass = MagicMock()
        sensor.async_write_ha_state = mock_write

        assert sensor.unique_id == f"{DOMAIN}_client_tracker"
        assert sensor.name == "Tracked Clients"
        assert sensor.native_value == 0

        # Test update with data
        mock_coordinator.data = {"clients": [{"mac": "11:22:33:44:55:66"}]}
        sensor._handle_coordinator_update()
        assert sensor.native_value == 1
        mock_write.assert_called()

@pytest.mark.asyncio
async def test_meraki_client_sensor():
    """Test the MerakiClientSensor."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = {"clients": [{"mac": "11:22:33:44:55:66", "description": "Test Client"}]}
    mock_config_entry = MagicMock()
    client_data = {"mac": "11:22:33:44:55:66", "description": "Test Client"}

    sensor = MerakiClientSensor(mock_coordinator, mock_config_entry, client_data)
    sensor.hass = MagicMock()
    sensor.async_write_ha_state = MagicMock()

    assert sensor.unique_id == "client-11:22:33:44:55:66"
    assert sensor.name == "Test Client"
    assert sensor.native_value == "online"

    # Test offline state
    mock_coordinator.data = {"clients": []}
    sensor._handle_coordinator_update()
    assert sensor.native_value == "offline"

    # Test no data
    mock_coordinator.data = None
    sensor._handle_coordinator_update()
    assert sensor.native_value == "offline"
