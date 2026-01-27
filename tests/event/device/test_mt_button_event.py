"""Tests for the Meraki MT button event entity."""

from unittest.mock import MagicMock, patch

import pytest
from homeassistant.components.event import EventDeviceClass

from custom_components.meraki_ha.event.device.mt_button import MerakiMtButtonEvent


async def test_mt_button_event_initialization(hass, mock_coordinator, mock_config_entry):
    """Test the initialization of the MT button event entity."""
    device = MagicMock()
    device.serial = "Q2XX-XXXX-XXXX"
    device.name = "Test Button"
    device.model = "MT30"
    device.button_press = None

    with patch(
        "custom_components.meraki_ha.event.device.mt_button.resolve_device_info",
        return_value={"identifiers": {("meraki_ha", "Q2XX-XXXX-XXXX")}},
    ):
        entity = MerakiMtButtonEvent(mock_coordinator, device, mock_config_entry)

        assert entity.unique_id == "Q2XX-XXXX-XXXX-button-event"
        assert entity.name == "Button Press"
        assert entity.device_class == EventDeviceClass.BUTTON
        assert entity.event_types == ["short_press", "long_press"]
        assert entity._last_ts == ""


async def test_mt_button_event_update(hass, mock_coordinator, mock_config_entry):
    """Test that events are triggered on update."""
    device = MagicMock()
    device.serial = "Q2XX-XXXX-XXXX"
    device.button_press = None

    mock_coordinator.get_device.return_value = device

    with patch(
        "custom_components.meraki_ha.event.device.mt_button.resolve_device_info",
        return_value={"identifiers": {("meraki_ha", "Q2XX-XXXX-XXXX")}},
    ):
        entity = MerakiMtButtonEvent(mock_coordinator, device, mock_config_entry)
        entity.hass = hass
        entity.async_write_ha_state = MagicMock()
        entity._trigger_event = MagicMock()

        # Simulate async_added_to_hass
        await entity.async_added_to_hass()
        assert entity._last_ts == ""

        # Update with a button press
        device.button_press = {"ts": "2023-01-01T12:00:00Z", "pressType": "short"}
        mock_coordinator.get_device.return_value = device

        entity._handle_coordinator_update()

        assert entity._last_ts == "2023-01-01T12:00:00Z"
        entity._trigger_event.assert_called_once_with("short_press")
        entity.async_write_ha_state.assert_called()

        # Update with same timestamp - should not trigger
        entity._trigger_event.reset_mock()
        entity.async_write_ha_state.reset_mock()
        entity._handle_coordinator_update()

        entity._trigger_event.assert_not_called()

        # Update with new timestamp - long press
        device.button_press = {"ts": "2023-01-01T12:01:00Z", "pressType": "long"}
        entity._handle_coordinator_update()

        assert entity._last_ts == "2023-01-01T12:01:00Z"
        entity._trigger_event.assert_called_once_with("long_press")


async def test_mt_button_event_initial_state(hass, mock_coordinator, mock_config_entry):
    """Test that existing events on startup are not replayed."""
    device = MagicMock()
    device.serial = "Q2XX-XXXX-XXXX"
    device.button_press = {"ts": "2023-01-01T12:00:00Z", "pressType": "short"}

    mock_coordinator.get_device.return_value = device

    with patch(
        "custom_components.meraki_ha.event.device.mt_button.resolve_device_info",
        return_value={"identifiers": {("meraki_ha", "Q2XX-XXXX-XXXX")}},
    ):
        entity = MerakiMtButtonEvent(mock_coordinator, device, mock_config_entry)
        entity.hass = hass
        entity.async_write_ha_state = MagicMock()
        entity._trigger_event = MagicMock()

        # Simulate async_added_to_hass
        await entity.async_added_to_hass()

        # Should have captured the timestamp
        assert entity._last_ts == "2023-01-01T12:00:00Z"

        # Coordinator update with same data should not trigger
        entity._handle_coordinator_update()
        entity._trigger_event.assert_not_called()
