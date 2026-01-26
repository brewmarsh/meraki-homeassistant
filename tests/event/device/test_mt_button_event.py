"""Tests for the Meraki MT button event entity."""

from unittest.mock import MagicMock, patch

from homeassistant.components.event import EventDeviceClass

from custom_components.meraki_ha.event.device.mt_button import MerakiMtButtonEvent


async def test_mt_button_event_initialization(
    hass, mock_coordinator, mock_config_entry
):
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

        assert entity.unique_id == "Q2XX-XXXX-XXXX_button_event"
        assert entity.name == "Button Press"
        assert entity.device_class == EventDeviceClass.BUTTON
        assert entity.event_types == ["short_press", "long_press"]

    # CoordinatorEntity should not poll
    assert entity.should_poll is False


async def test_mt_button_event_update(
    hass, mock_coordinator, mock_config_entry
):
    """Test that events are triggered on update."""
    device = MagicMock()
    device.serial = "Q2XX-XXXX-XXXX"
    device.button_press = None

    # Ensure coordinator returns our device mock
    mock_coordinator.get_device.return_value = device

    with patch(
        "custom_components.meraki_ha.event.device.mt_button.resolve_device_info",
        return_value={"identifiers": {("meraki_ha", "Q2XX-XXXX-XXXX")}},
    ):
        entity = MerakiMtButtonEvent(mock_coordinator, device, mock_config_entry)
        entity.hass = hass
        entity.async_write_ha_state = MagicMock()
        entity._trigger_event = MagicMock()

        # Initial update - should set _last_ts but not trigger
        device.button_press = {"ts": "2023-01-01T00:00:00Z", "pressType": "short"}
        entity._handle_coordinator_update()

        assert entity._last_ts == "2023-01-01T00:00:00Z"
        entity._trigger_event.assert_not_called()

        # Update with new timestamp - trigger event
        device.button_press = {"ts": "2023-01-01T00:01:00Z", "pressType": "long"}

        entity._handle_coordinator_update()

        assert entity._last_ts == "2023-01-01T00:01:00Z"
        entity._trigger_event.assert_called_once_with(
            "long_press", {"press_type": "long", "ts": "2023-01-01T00:01:00Z"}
        )

        # Update with same timestamp - no event
        entity._trigger_event.reset_mock()
        entity._handle_coordinator_update()
        entity._trigger_event.assert_not_called()


async def test_mt_button_event_unknown_type(
    hass, mock_coordinator, mock_config_entry
):
    """Test handling of unknown event types."""
    device = MagicMock()
    device.serial = "Q2XX-XXXX-XXXX"
    device.button_press = None

    # Ensure coordinator returns our device mock
    mock_coordinator.get_device.return_value = device

    with patch(
        "custom_components.meraki_ha.event.device.mt_button.resolve_device_info",
        return_value={"identifiers": {("meraki_ha", "Q2XX-XXXX-XXXX")}},
    ):
        entity = MerakiMtButtonEvent(mock_coordinator, device, mock_config_entry)
        entity.hass = hass
        entity.async_write_ha_state = MagicMock() # Mock this to avoid NoEntitySpecifiedError
        entity._trigger_event = MagicMock()

        # Initial setup
        entity._last_ts = "2023-01-01T00:00:00Z"
        entity._is_first_update = False

        # Update with unknown type
        device.button_press = {"ts": "2023-01-01T00:02:00Z", "pressType": "triple"}

        entity._handle_coordinator_update()

        assert entity._last_ts == "2023-01-01T00:02:00Z"
        entity._trigger_event.assert_not_called()
