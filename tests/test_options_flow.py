"""Tests for the options flow module."""

from typing import Any
from unittest.mock import MagicMock

import pytest
from homeassistant.config_entries import ConfigFlowResult

from custom_components.meraki_ha.const import (
    CONF_ENABLED_NETWORKS,
    CONF_MQTT_RELAY_DESTINATIONS,
    DOMAIN,
)
from custom_components.meraki_ha.options_flow import MerakiOptionsFlowHandler


def create_options_flow_handler(
    options: dict[str, Any] | None = None,
    hass: MagicMock | None = None,
    entry_id: str = "test_entry_id",
) -> MerakiOptionsFlowHandler:
    """Create an options flow handler with mocked config entry.

    This helper simulates how Home Assistant sets up the options flow:
    1. Creates the handler without passing config_entry
    2. Sets up hass and handler properties as the framework would
    3. Mocks config_entry property to return a mock with the given options
    """
    if options is None:
        options = {"scan_interval": 30}

    handler = MerakiOptionsFlowHandler()

    # Create mock config entry
    mock_entry = MagicMock()
    mock_entry.entry_id = entry_id
    mock_entry.options = options

    # Set up hass mock if not provided
    if hass is None:
        hass = MagicMock()
        mock_coordinator = MagicMock()
        mock_coordinator.data = {
            "networks": [
                {"id": "N_123", "name": "Main Office"},
                {"id": "N_456", "name": "Branch Office"},
            ]
        }
        hass.data = {
            DOMAIN: {
                entry_id: {
                    "coordinator": mock_coordinator,
                }
            }
        }
        # Mock config_entries.async_get_known_entry to return our mock entry
        hass.config_entries.async_get_known_entry.return_value = mock_entry

    handler.hass = hass

    # Set the handler property (this is what the framework sets - it's the entry ID)
    handler.handler = entry_id

    # Mock the config_entry property to return our mock
    # We need to patch it on the instance
    handler._config_entry = mock_entry

    return handler


@pytest.fixture
def mock_options_config_entry() -> MagicMock:
    """Create a mock config entry for options flow."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.options = {
        "scan_interval": 30,
    }
    return entry


@pytest.fixture
def mock_hass_with_coordinator() -> MagicMock:
    """Create a mock hass with coordinator data."""
    hass = MagicMock()
    mock_coordinator = MagicMock()
    mock_coordinator.data = {
        "networks": [
            {"id": "N_123", "name": "Main Office"},
            {"id": "N_456", "name": "Branch Office"},
        ]
    }
    hass.data = {
        DOMAIN: {
            "test_entry_id": {
                "coordinator": mock_coordinator,
            }
        }
    }
    return hass


def test_options_flow_init() -> None:
    """Test options flow initialization with the new pattern."""
    handler = MerakiOptionsFlowHandler()

    # Initially options should be empty (lazy loading)
    assert handler._options == {}
    assert handler._options_initialized is False


def test_options_flow_init_with_config_entry() -> None:
    """Test that options are loaded lazily from config_entry."""
    handler = create_options_flow_handler(options={"scan_interval": 30})

    # After proper setup, options should be accessible
    assert handler.options["scan_interval"] == 30


@pytest.mark.asyncio
async def test_async_step_init_shows_menu() -> None:
    """Test the init step shows the main menu."""
    handler = create_options_flow_handler()
    result: ConfigFlowResult = await handler.async_step_init()

    assert result["type"].value == "menu"
    assert result["step_id"] == "init"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "menu_option, expected_step_id",
    [
        ("network_selection", "network_selection"),
        ("polling", "polling"),
        ("camera", "camera"),
        ("mqtt", "mqtt"),
        ("display_preferences", "display_preferences"),
    ],
)
async def test_menu_options_navigate_to_correct_step(
    menu_option: str,
    expected_step_id: str,
) -> None:
    """Test that menu options navigate to the correct form."""
    handler = create_options_flow_handler()
    result: ConfigFlowResult = await getattr(handler, f"async_step_{menu_option}")()

    assert result["type"].value == "form"
    assert result["step_id"] == expected_step_id


@pytest.mark.asyncio
async def test_network_selection_step() -> None:
    """Test the network selection step saves data and creates entry."""
    handler = create_options_flow_handler()

    user_input = {
        CONF_ENABLED_NETWORKS: ["N_123"],
        "enable_device_tracker": False,
    }

    result: ConfigFlowResult = await handler.async_step_network_selection(user_input)

    assert result["type"].value == "create_entry"
    assert handler.options[CONF_ENABLED_NETWORKS] == ["N_123"]
    assert handler.options["enable_device_tracker"] is False


@pytest.mark.asyncio
async def test_polling_step() -> None:
    """Test the polling step saves data and creates entry."""
    handler = create_options_flow_handler()

    user_input = {
        "scan_interval": 120,
        "network_scan_interval": 600,
    }
    result: ConfigFlowResult = await handler.async_step_polling(user_input)
    assert result["type"].value == "create_entry"
    assert handler.options["scan_interval"] == 120
    assert handler.options["network_scan_interval"] == 600


@pytest.mark.asyncio
async def test_camera_step() -> None:
    """Test the camera step saves data and creates entry."""
    handler = create_options_flow_handler()

    user_input = {"camera_snapshot_interval": 60}
    result: ConfigFlowResult = await handler.async_step_camera(user_input)

    assert result["type"].value == "create_entry"
    assert handler.options["camera_snapshot_interval"] == 60


@pytest.mark.asyncio
async def test_display_preferences_step() -> None:
    """Test the display preferences step saves data and creates entry."""
    handler = create_options_flow_handler()

    user_input = {"dashboard_view_mode": "type"}
    result: ConfigFlowResult = await handler.async_step_display_preferences(user_input)

    assert result["type"].value == "create_entry"
    assert handler.options["dashboard_view_mode"] == "type"


@pytest.mark.asyncio
async def test_notifications_step_shows_form() -> None:
    """Test the notifications step shows a form with coming soon message."""
    handler = create_options_flow_handler()

    result: ConfigFlowResult = await handler.async_step_notifications()

    assert result["type"].value == "form"
    assert result["step_id"] == "notifications"
    # Verify coming soon message is in placeholders
    placeholders = result.get("description_placeholders")
    assert placeholders is not None
    assert "message" in placeholders


@pytest.mark.asyncio
async def test_notifications_step_returns_to_menu() -> None:
    """Test the notifications step returns to menu when submitted."""
    handler = create_options_flow_handler()

    result: ConfigFlowResult = await handler.async_step_notifications({})

    assert result["type"].value == "menu"
    assert result["step_id"] == "init"


# --- MQTT Destination Management ---


@pytest.mark.asyncio
async def test_mqtt_add_destination_action() -> None:
    """Test MQTT 'add' action navigates to the destination form."""
    handler = create_options_flow_handler()
    result: ConfigFlowResult = await handler.async_step_mqtt(
        {"enable_mqtt": True, "action": "add"}
    )
    assert result["type"].value == "form"
    assert result["step_id"] == "mqtt_destination"
    assert handler._editing_destination_index is None


@pytest.mark.asyncio
async def test_mqtt_edit_destination_action_with_destinations() -> None:
    """Test MQTT 'edit' action navigates to destination selection."""
    handler = create_options_flow_handler(
        options={
            "scan_interval": 30,
            CONF_MQTT_RELAY_DESTINATIONS: [
                {"name": "Test Broker", "host": "mqtt.test.com"}
            ],
        }
    )

    result: ConfigFlowResult = await handler.async_step_mqtt(
        {"enable_mqtt": True, "action": "edit"}
    )

    assert result["type"].value == "form"
    assert result["step_id"] == "mqtt_select_destination"
    assert handler._destination_action == "edit"


@pytest.mark.asyncio
async def test_mqtt_delete_destination_action() -> None:
    """Test MQTT 'delete' action and removal of destinations."""
    handler = create_options_flow_handler(
        options={
            "scan_interval": 30,
            CONF_MQTT_RELAY_DESTINATIONS: [
                {"name": "Broker A", "host": "a.test.com"},
                {"name": "Broker B", "host": "b.test.com"},
            ],
        }
    )

    # Trigger delete action
    result: ConfigFlowResult = await handler.async_step_mqtt(
        {"enable_mqtt": True, "action": "delete"}
    )
    assert result["step_id"] == "mqtt_select_destination"

    # Select and submit the destination to delete
    result = await handler.async_step_mqtt_select_destination({"destinations": ["0"]})

    assert result["step_id"] == "mqtt"
    remaining = handler.options[CONF_MQTT_RELAY_DESTINATIONS]
    assert len(remaining) == 1
    assert remaining[0]["name"] == "Broker B"


@pytest.mark.asyncio
async def test_mqtt_select_destination_with_empty_list_returns_to_mqtt() -> None:
    """Test selecting a destination when none exist returns to the MQTT menu."""
    handler = create_options_flow_handler()
    handler._destination_action = "edit"
    result: ConfigFlowResult = await handler.async_step_mqtt_select_destination()

    assert result["step_id"] == "mqtt"


@pytest.mark.asyncio
async def test_mqtt_add_new_destination_and_save() -> None:
    """Test adding a new MQTT destination via the form and saving."""
    handler = create_options_flow_handler()
    handler._editing_destination_index = None  # Add mode

    destination_data = {
        "name": "New Broker",
        "host": "new.mqtt.com",
        "port": 1883,
    }
    result: ConfigFlowResult = await handler.async_step_mqtt_destination(
        destination_data
    )

    assert result["step_id"] == "mqtt"
    destinations = handler.options.get(CONF_MQTT_RELAY_DESTINATIONS, [])
    assert len(destinations) == 1
    assert destinations[0]["name"] == "New Broker"
    assert destinations[0]["host"] == "new.mqtt.com"


@pytest.mark.asyncio
async def test_mqtt_destination_missing_host_shows_error() -> None:
    """Test MQTT destination form shows error when host is missing."""
    handler = create_options_flow_handler()
    handler._editing_destination_index = None

    result: ConfigFlowResult = await handler.async_step_mqtt_destination(
        {"name": "Test Broker", "host": "", "port": 1883}
    )

    assert result["type"].value == "form"
    assert result["step_id"] == "mqtt_destination"
    errors = result.get("errors")
    assert errors is not None
    assert errors.get("base") == "host_required"


@pytest.mark.asyncio
async def test_mqtt_destination_missing_name_shows_error() -> None:
    """Test MQTT destination form shows error when name is missing."""
    handler = create_options_flow_handler()
    handler._editing_destination_index = None

    result: ConfigFlowResult = await handler.async_step_mqtt_destination(
        {"name": "", "host": "mqtt.test.com", "port": 1883}
    )

    assert result["type"].value == "form"
    assert result["step_id"] == "mqtt_destination"
    errors = result.get("errors")
    assert errors is not None
    assert errors.get("base") == "name_required"


@pytest.mark.asyncio
async def test_mqtt_destination_invalid_port_shows_error() -> None:
    """Test MQTT destination form shows error when port is invalid."""
    handler = create_options_flow_handler()
    handler._editing_destination_index = None

    result: ConfigFlowResult = await handler.async_step_mqtt_destination(
        {"name": "Test", "host": "mqtt.test.com", "port": "invalid"}
    )

    assert result["type"].value == "form"
    assert result["step_id"] == "mqtt_destination"
    errors = result.get("errors")
    assert errors is not None
    assert errors.get("base") == "invalid_port"


@pytest.mark.asyncio
async def test_mqtt_edit_existing_destination() -> None:
    """Test editing an existing MQTT destination."""
    handler = create_options_flow_handler(
        options={
            "scan_interval": 30,
            CONF_MQTT_RELAY_DESTINATIONS: [
                {"name": "Original", "host": "original.com", "port": 1883}
            ],
        }
    )
    handler._editing_destination_index = 0  # Edit mode for first destination

    result: ConfigFlowResult = await handler.async_step_mqtt_destination(
        {"name": "Updated", "host": "updated.com", "port": 8883}
    )

    assert result["step_id"] == "mqtt"
    destinations = handler.options.get(CONF_MQTT_RELAY_DESTINATIONS, [])
    assert len(destinations) == 1
    assert destinations[0]["name"] == "Updated"
    assert destinations[0]["host"] == "updated.com"
    assert destinations[0]["port"] == 8883


@pytest.mark.asyncio
async def test_mqtt_save_without_action() -> None:
    """Test saving MQTT settings without any relay management action."""
    handler = create_options_flow_handler()

    result: ConfigFlowResult = await handler.async_step_mqtt(
        {"enable_mqtt": True, "action": "save"}
    )

    assert result["type"].value == "create_entry"
    assert handler.options.get("enable_mqtt") is True


@pytest.mark.asyncio
async def test_mqtt_delete_multiple_destinations() -> None:
    """Test deleting multiple MQTT destinations at once."""
    handler = create_options_flow_handler(
        options={
            "scan_interval": 30,
            CONF_MQTT_RELAY_DESTINATIONS: [
                {"name": "Broker A", "host": "a.test.com"},
                {"name": "Broker B", "host": "b.test.com"},
                {"name": "Broker C", "host": "c.test.com"},
            ],
        }
    )
    handler._destination_action = "delete"

    # Delete first and third destinations
    result: ConfigFlowResult = await handler.async_step_mqtt_select_destination(
        {"destinations": ["0", "2"]}
    )

    assert result["step_id"] == "mqtt"
    remaining = handler.options[CONF_MQTT_RELAY_DESTINATIONS]
    assert len(remaining) == 1
    assert remaining[0]["name"] == "Broker B"


@pytest.mark.asyncio
async def test_mqtt_edit_selection_navigates_to_destination_form() -> None:
    """Test selecting a destination for edit navigates to the form."""
    handler = create_options_flow_handler(
        options={
            "scan_interval": 30,
            CONF_MQTT_RELAY_DESTINATIONS: [
                {"name": "Broker A", "host": "a.test.com", "port": 1883}
            ],
        }
    )
    handler._destination_action = "edit"

    result: ConfigFlowResult = await handler.async_step_mqtt_select_destination(
        {"destinations": ["0"]}
    )

    assert result["type"].value == "form"
    assert result["step_id"] == "mqtt_destination"
    assert handler._editing_destination_index == 0


@pytest.mark.asyncio
async def test_mqtt_edit_no_selection_returns_to_mqtt() -> None:
    """Test edit with no selection returns to MQTT menu."""
    handler = create_options_flow_handler(
        options={
            "scan_interval": 30,
            CONF_MQTT_RELAY_DESTINATIONS: [{"name": "Broker A", "host": "a.test.com"}],
        }
    )
    handler._destination_action = "edit"

    result: ConfigFlowResult = await handler.async_step_mqtt_select_destination(
        {"destinations": []}
    )

    assert result["step_id"] == "mqtt"


@pytest.mark.asyncio
async def test_network_selection_with_empty_coordinator_data() -> None:
    """Test network selection step with empty coordinator data."""
    hass = MagicMock()
    mock_coordinator = MagicMock()
    mock_coordinator.data = {}
    mock_entry = MagicMock()
    mock_entry.entry_id = "test_entry_id"
    mock_entry.options = {"scan_interval": 30}

    hass.data = {
        DOMAIN: {
            "test_entry_id": {
                "coordinator": mock_coordinator,
            }
        }
    }
    hass.config_entries.async_get_known_entry.return_value = mock_entry

    handler = MerakiOptionsFlowHandler()
    handler.hass = hass
    handler.handler = "test_entry_id"
    handler._config_entry = mock_entry

    result: ConfigFlowResult = await handler.async_step_network_selection()

    assert result["type"].value == "form"
    assert result["step_id"] == "network_selection"


# --- Tests for async_get_options_flow ---


def test_async_get_options_flow_returns_handler() -> None:
    """Test that async_get_options_flow returns a MerakiOptionsFlowHandler."""
    from custom_components.meraki_ha.config_flow import MerakiConfigFlow

    mock_entry = MagicMock()
    mock_entry.entry_id = "test_entry_id"
    mock_entry.options = {"scan_interval": 30}

    handler = MerakiConfigFlow.async_get_options_flow(mock_entry)

    assert isinstance(handler, MerakiOptionsFlowHandler)
    # Verify it was created without passing config_entry
    assert handler._options == {}
    assert handler._options_initialized is False


# --- Integration test that simulates real HA behavior ---


@pytest.mark.asyncio
async def test_options_flow_simulates_real_ha_behavior() -> None:
    """Test that options flow works when set up like HA does.

    This test simulates the actual HA flow:
    1. async_get_options_flow() is called with config_entry
    2. Framework sets flow.hass and flow.handler after creation
    3. async_step_init is called
    """
    from custom_components.meraki_ha.config_flow import MerakiConfigFlow

    # Step 1: Create mock config entry
    mock_entry = MagicMock()
    mock_entry.entry_id = "test_entry_id"
    mock_entry.options = {"scan_interval": 60, "enable_mqtt": True}

    # Step 2: Get the options flow handler (simulates what HA does)
    handler = MerakiConfigFlow.async_get_options_flow(mock_entry)

    # Step 3: Simulate what the HA framework does after creating the flow
    mock_hass = MagicMock()
    mock_coordinator = MagicMock()
    mock_coordinator.data = {"networks": []}
    mock_hass.data = {
        DOMAIN: {
            "test_entry_id": {
                "coordinator": mock_coordinator,
            }
        }
    }
    mock_hass.config_entries.async_get_known_entry.return_value = mock_entry

    handler.hass = mock_hass
    handler.handler = "test_entry_id"
    # In real HA, the config_entry property uses handler to look up the entry
    # For testing, we set _config_entry directly
    handler._config_entry = mock_entry

    # Step 4: Now the flow should work
    result = await handler.async_step_init()
    assert result["type"].value == "menu"
    assert result["step_id"] == "init"

    # Verify options are loaded correctly
    assert handler.options["scan_interval"] == 60
    assert handler.options["enable_mqtt"] is True
