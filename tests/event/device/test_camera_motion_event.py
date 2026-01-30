"""Tests for the Meraki camera motion event entity."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.components.event import EventDeviceClass

from custom_components.meraki_ha.event.device.camera_motion import (
    MerakiCameraMotionEvent,
)


@pytest.fixture
def mock_camera_service():
    """Fixture for a mocked CameraService."""
    service = AsyncMock()
    service.get_motion_history = AsyncMock(return_value=[])
    return service


async def test_camera_motion_event_initialization(
    hass, mock_coordinator, mock_camera_service, mock_config_entry
):
    """Test the initialization of the camera motion event entity."""
    device = MagicMock()
    device.serial = "Q2XX-XXXX-XXXX"
    device.name = "Test Camera"
    device.model = "MV22"

    with patch(
        "custom_components.meraki_ha.event.device.camera_motion.resolve_device_info",
        return_value={"identifiers": {("meraki_ha", "Q2XX-XXXX-XXXX")}},
    ):
        entity = MerakiCameraMotionEvent(
            mock_coordinator, device, mock_camera_service, mock_config_entry
        )

        assert entity.unique_id == "Q2XX-XXXX-XXXX-motion-event"
        assert entity.name == "Motion Event"
        assert entity.device_class == EventDeviceClass.MOTION
        assert entity.event_types == ["motion", "person", "vehicle"]
    assert entity.should_poll is True


async def test_camera_motion_event_update(
    hass, mock_coordinator, mock_camera_service, mock_config_entry
):
    """Test that events are triggered on update."""
    device = MagicMock()
    device.serial = "Q2XX-XXXX-XXXX"

    with patch(
        "custom_components.meraki_ha.event.device.camera_motion.resolve_device_info",
        return_value={"identifiers": {("meraki_ha", "Q2XX-XXXX-XXXX")}},
    ):
        entity = MerakiCameraMotionEvent(
            mock_coordinator, device, mock_camera_service, mock_config_entry
        )
        entity.hass = hass
        entity.async_write_ha_state = MagicMock()
        entity._trigger_event = MagicMock()

        # Initial update - should set _last_timestamp but not trigger
        mock_camera_service.get_motion_history.return_value = [
            {"startTs": 1000, "event_type": "person"},
            {"startTs": 2000, "event_type": "vehicle"},
        ]

        await entity.async_update()

        assert entity._last_timestamp == 2000
        entity._trigger_event.assert_not_called()

        # Second update - new event
        mock_camera_service.get_motion_history.return_value = [
            {"startTs": 1000, "event_type": "person"},
            {"startTs": 2000, "event_type": "vehicle"},
            {"startTs": 3000, "event_type": "person"},
        ]

        await entity.async_update()

        assert entity._last_timestamp == 3000
        entity._trigger_event.assert_called_once_with(
            "person", {"startTs": 3000, "event_type": "person"}
        )

        # Third update - no new events
        entity._trigger_event.reset_mock()
        await entity.async_update()
        entity._trigger_event.assert_not_called()


async def test_camera_motion_event_unknown_type(
    hass, mock_coordinator, mock_camera_service, mock_config_entry
):
    """Test handling of unknown event types."""
    device = MagicMock()
    device.serial = "Q2XX-XXXX-XXXX"

    with patch(
        "custom_components.meraki_ha.event.device.camera_motion.resolve_device_info",
        return_value={"identifiers": {("meraki_ha", "Q2XX-XXXX-XXXX")}},
    ):
        entity = MerakiCameraMotionEvent(
            mock_coordinator, device, mock_camera_service, mock_config_entry
        )
        entity.hass = hass
        entity._trigger_event = MagicMock()

        # Initial update
        mock_camera_service.get_motion_history.return_value = []
        await entity.async_update()

        # Update with unknown type
        mock_camera_service.get_motion_history.return_value = [
            {"startTs": 4000, "event_type": "unknown_thing"},
        ]

        await entity.async_update()

        assert entity._last_timestamp == 4000
        entity._trigger_event.assert_called_once_with(
            "motion", {"startTs": 4000, "event_type": "unknown_thing"}
        )
