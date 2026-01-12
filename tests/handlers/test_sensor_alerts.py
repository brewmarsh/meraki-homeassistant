"""Tests for sensor alerts handler."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.handlers.sensor_alerts import async_handle_sensor_alert


class TaskCaptureMock(MagicMock):
    """Mock that captures and closes coroutines to avoid warnings."""

    def __init__(self, *args, **kwargs):
        """Initialize with task tracking."""
        super().__init__(*args, **kwargs)
        self._captured_tasks = []

    def __call__(self, *args, **kwargs):
        """Capture and close any coroutines in the arguments."""
        super().__call__(*args, **kwargs)
        # Close any coroutines passed as arguments
        for arg in args:
            if hasattr(arg, "close"):
                arg.close()
                self._captured_tasks.append(arg)
        return None


@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.hass = MagicMock()
    coordinator.hass.bus = MagicMock()
    coordinator.hass.bus.async_fire = MagicMock()
    # Use TaskCaptureMock to capture and close coroutines properly
    coordinator.hass.async_create_task = TaskCaptureMock()
    coordinator._targeted_device_refresh = AsyncMock()
    # Mock schedule_debounced_refresh to capture and close coroutines
    coordinator.schedule_debounced_refresh = TaskCaptureMock()
    return coordinator


class TestSensorAlerts:
    """Test sensor alerts handler."""

    @pytest.mark.asyncio
    async def test_temperature_threshold_alert(self, mock_coordinator):
        """Test handling temperature threshold alert."""
        data = {
            "deviceSerial": "Q2XX-1234-5678",
            "deviceName": "Office Temp Sensor",
            "networkName": "Main Office",
            "alertData": {
                "temperature": 28.5,
                "threshold": 25.0,
            },
        }

        await async_handle_sensor_alert(
            mock_coordinator, "Temperature threshold exceeded", data
        )

        # Should fire event
        mock_coordinator.hass.bus.async_fire.assert_called_once()
        call_args = mock_coordinator.hass.bus.async_fire.call_args
        assert "meraki_ha_sensor_alert" in call_args[0][0]
        event_data = call_args[0][1]
        assert event_data["event_type"] == "temperature_threshold"
        assert event_data["value"] == 28.5
        assert event_data["threshold"] == 25.0

        # Should schedule debounced device refresh
        mock_coordinator.schedule_debounced_refresh.assert_called()

    @pytest.mark.asyncio
    async def test_humidity_threshold_alert(self, mock_coordinator):
        """Test handling humidity threshold alert."""
        data = {
            "deviceSerial": "Q2XX-1234-5678",
            "deviceName": "Office Humidity Sensor",
            "networkName": "Main Office",
            "alertData": {
                "humidity": 85,
                "threshold": 70,
            },
        }

        await async_handle_sensor_alert(
            mock_coordinator, "Humidity threshold exceeded", data
        )

        call_args = mock_coordinator.hass.bus.async_fire.call_args
        event_data = call_args[0][1]
        assert event_data["event_type"] == "humidity_threshold"

    @pytest.mark.asyncio
    async def test_water_detected_alert(self, mock_coordinator):
        """Test handling water detected alert."""
        data = {
            "deviceSerial": "Q2XX-1234-5678",
            "deviceName": "Water Sensor",
            "networkName": "Server Room",
            "alertData": {},
        }

        await async_handle_sensor_alert(mock_coordinator, "Water detected", data)

        call_args = mock_coordinator.hass.bus.async_fire.call_args
        event_data = call_args[0][1]
        assert event_data["event_type"] == "water_detected"
        assert event_data["value"] is True

    @pytest.mark.asyncio
    async def test_door_change_alert(self, mock_coordinator):
        """Test handling door open/close alert."""
        data = {
            "deviceSerial": "Q2XX-1234-5678",
            "deviceName": "Door Sensor",
            "networkName": "Main Office",
            "alertData": {
                "open": True,
            },
        }

        await async_handle_sensor_alert(mock_coordinator, "Door opened/closed", data)

        call_args = mock_coordinator.hass.bus.async_fire.call_args
        event_data = call_args[0][1]
        assert event_data["event_type"] == "door_change"
        assert event_data["value"] == "open"

    @pytest.mark.asyncio
    async def test_power_outage_alert(self, mock_coordinator):
        """Test handling power outage alert."""
        data = {
            "deviceSerial": "Q2XX-1234-5678",
            "deviceName": "Power Monitor",
            "networkName": "Server Room",
            "alertData": {
                "powerStatus": "outage",
            },
        }

        await async_handle_sensor_alert(mock_coordinator, "Power outage detected", data)

        call_args = mock_coordinator.hass.bus.async_fire.call_args
        event_data = call_args[0][1]
        assert event_data["event_type"] == "power_outage"

    @pytest.mark.asyncio
    async def test_missing_device_serial(self, mock_coordinator):
        """Test that alerts without deviceSerial are handled gracefully."""
        data = {
            "networkName": "Main Office",
            "alertData": {},
            # No deviceSerial
        }

        # Should not raise
        await async_handle_sensor_alert(
            mock_coordinator, "Temperature threshold exceeded", data
        )

        # Should not fire event
        mock_coordinator.hass.bus.async_fire.assert_not_called()
