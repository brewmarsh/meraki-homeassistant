"""Test for reproducing camera status issue."""

from unittest.mock import MagicMock, patch

import pytest
from custom_components.meraki_ha.meraki_data_coordinator import MerakiDataCoordinator
from homeassistant.helpers import entity_registry as er


@pytest.fixture
def mock_api_client():
    """Fixture for a mocked MerakiAPIClient."""
    client = MagicMock()
    return client


@pytest.fixture
def coordinator(hass, mock_api_client):
    """Fixture for a MerakiDataCoordinator instance."""
    entry = MagicMock()
    entry.options = {}
    return MerakiDataCoordinator(
        hass=hass, api_client=mock_api_client, scan_interval=300, entry=entry
    )


async def test_populate_device_entities_picks_camera(coordinator, hass):
    """Test that _populate_device_entities picks the camera entity over sensor."""
    # Mock data
    data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "model": "MV12",
                "name": "Test Camera",
            }
        ]
    }

    # Mock Device Registry
    mock_dr = MagicMock()
    mock_device = MagicMock()
    mock_device.id = "device_id_123"
    mock_dr.async_get_device.return_value = mock_device

    # Mock Entity Registry
    mock_er = MagicMock()

    # Create mock entities
    # Entity 1: Sensor (e.g. timestamp) - should NOT be picked
    entity_sensor = MagicMock(spec=er.RegistryEntry)
    entity_sensor.entity_id = "sensor.test_camera_last_reported"
    entity_sensor.name = "Test Camera Last Reported"
    entity_sensor.original_name = "Test Camera Last Reported"
    entity_sensor.platform = "meraki_ha"  # Integration platform
    entity_sensor.domain = "sensor"  # Entity domain
    entity_sensor.unique_id = "Q234-ABCD-5678_last_reported"

    # Entity 2: Camera - SHOULD be picked
    entity_camera = MagicMock(spec=er.RegistryEntry)
    entity_camera.entity_id = "camera.test_camera"
    entity_camera.name = "Test Camera"
    entity_camera.original_name = "Test Camera"
    entity_camera.platform = "meraki_ha"  # Integration platform
    entity_camera.domain = "camera"  # Entity domain
    entity_camera.unique_id = "Q234-ABCD-5678-camera"

    # Return them in an order where sensor comes first (to test priority)
    mock_entries = [entity_sensor, entity_camera]

    # Set states in HA state machine
    hass.states.async_set("sensor.test_camera_last_reported", "2023-01-01")
    hass.states.async_set("camera.test_camera", "idle")

    with (
        patch(
            "custom_components.meraki_ha.meraki_data_coordinator.dr.async_get",
            return_value=mock_dr,
        ),
        patch(
            "custom_components.meraki_ha.meraki_data_coordinator.er.async_get",
            return_value=mock_er,
        ),
        patch(
            "custom_components.meraki_ha.meraki_data_coordinator.er.async_entries_for_device",
            return_value=mock_entries,
        ),
    ):
        coordinator._populate_device_entities(data)

        device = data["devices"][0]

        # We expect camera.test_camera
        assert device.get("entity_id") == "camera.test_camera"
