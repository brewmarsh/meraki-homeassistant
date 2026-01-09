"""Tests for the options flow module."""

from unittest.mock import MagicMock

import pytest
import voluptuous as vol
from homeassistant.helpers import selector

from custom_components.meraki_ha.const import (
    CONF_ENABLED_NETWORKS,
    DOMAIN,
)
from custom_components.meraki_ha.options_flow import MerakiOptionsFlowHandler


@pytest.fixture
def mock_options_config_entry() -> MagicMock:
    """Create a mock config entry for options flow."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.options = {
        "scan_interval": 30,
        "enable_device_status": True,
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


def test_options_flow_init(mock_options_config_entry: MagicMock) -> None:
    """Test options flow initialization."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    assert handler.options == mock_options_config_entry.options
    assert handler.options["scan_interval"] == 30
    assert handler.options["enable_device_status"] is True


@pytest.mark.asyncio
async def test_async_step_init_with_user_input_moves_to_dashboard(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test options flow step init with user input moves to dashboard step."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    user_input = {
        "scan_interval": 60,
        "enable_device_status": False,
    }

    result = await handler.async_step_init(user_input)

    # Step init should move to dashboard step, returning a form
    assert result["type"].value == "form"
    assert result["step_id"] == "dashboard"


@pytest.mark.asyncio
async def test_async_step_dashboard_with_user_input_moves_to_camera(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test options flow step dashboard with user input moves to camera step."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    result = await handler.async_step_dashboard({"some_dashboard_option": True})

    # Dashboard step should move to camera step, returning a form
    assert result["type"].value == "form"
    assert result["step_id"] == "camera"


@pytest.mark.asyncio
async def test_async_step_camera_with_user_input_moves_to_mqtt(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test options flow step camera with user input moves to mqtt step."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    result = await handler.async_step_camera({"some_camera_option": True})

    # Camera step should move to mqtt step, returning a form
    assert result["type"].value == "form"
    assert result["step_id"] == "mqtt"


@pytest.mark.asyncio
async def test_async_step_mqtt_with_user_input_creates_entry(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test options flow step mqtt with user input creates entry."""
    from custom_components.meraki_ha.const import CONF_INTEGRATION_TITLE

    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    result = await handler.async_step_mqtt({"enable_mqtt": False})

    # MQTT step with input should create entry
    assert result["type"].value == "create_entry"
    assert result["title"] == CONF_INTEGRATION_TITLE


def test_populate_schema_defaults() -> None:
    """Test _populate_schema_defaults populates existing values."""
    mock_entry = MagicMock()
    mock_entry.options = {"scan_interval": 45}

    handler = MerakiOptionsFlowHandler(mock_entry)

    # Create a simple schema
    schema = vol.Schema(
        {
            vol.Required("scan_interval"): int,
            vol.Optional("other_option"): str,
        }
    )

    defaults = {"scan_interval": 45}
    network_options: list[selector.SelectOptionDict] = []

    result_schema = handler._populate_schema_defaults(schema, defaults, network_options)

    # Verify the schema was processed (returned as a Schema object)
    assert isinstance(result_schema, vol.Schema)


def test_populate_schema_defaults_with_networks() -> None:
    """Test _populate_schema_defaults includes network options."""
    mock_entry = MagicMock()
    mock_entry.options = {}

    handler = MerakiOptionsFlowHandler(mock_entry)

    # Create schema with network selector
    network_selector = selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[],
            multiple=True,
        )
    )

    schema = vol.Schema(
        {
            vol.Optional(CONF_ENABLED_NETWORKS): network_selector,
        }
    )

    defaults: dict[str, object] = {}
    network_options: list[selector.SelectOptionDict] = [
        selector.SelectOptionDict(label="Main Office", value="N_123"),
        selector.SelectOptionDict(label="Branch Office", value="N_456"),
    ]

    result_schema = handler._populate_schema_defaults(schema, defaults, network_options)

    assert isinstance(result_schema, vol.Schema)


@pytest.mark.asyncio
async def test_full_options_flow_creates_entry(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test complete options flow from start to entry creation."""
    # Start with initial options
    mock_options_config_entry.options = {
        "scan_interval": 30,
        "enable_device_status": True,
        "temperature_unit": "celsius",
    }

    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    # Step 1: init -> goes to dashboard
    result = await handler.async_step_init({"scan_interval": 120})
    assert result["step_id"] == "dashboard"

    # Step 2: dashboard -> goes to camera
    result = await handler.async_step_dashboard({})
    assert result["step_id"] == "camera"

    # Step 3: camera -> goes to mqtt
    result = await handler.async_step_camera({})
    assert result["step_id"] == "mqtt"

    # Step 4: mqtt -> creates entry
    result = await handler.async_step_mqtt({"enable_mqtt": False})
    assert result["type"].value == "create_entry"
    # New value should be applied
    assert result["data"]["scan_interval"] == 120
    # Existing values should be preserved
    assert result["data"]["enable_device_status"] is True
    assert result["data"]["temperature_unit"] == "celsius"


@pytest.mark.asyncio
async def test_mqtt_add_destination_action(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test MQTT add destination action navigates to destination form."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    # Select add action
    result = await handler.async_step_mqtt({"enable_mqtt": True, "action": "add"})

    # Should go to mqtt_destination step
    assert result["type"].value == "form"
    assert result["step_id"] == "mqtt_destination"
    # Should be in add mode (not editing)
    assert handler._editing_destination_index is None


@pytest.mark.asyncio
async def test_mqtt_edit_destination_action_with_destinations(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test MQTT edit action shows destination selection when destinations exist."""
    from custom_components.meraki_ha.const import CONF_MQTT_RELAY_DESTINATIONS

    mock_options_config_entry.options = {
        CONF_MQTT_RELAY_DESTINATIONS: [
            {"name": "Test Broker", "host": "mqtt.test.com", "port": 1883},
        ]
    }

    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    # Select edit action
    result = await handler.async_step_mqtt({"enable_mqtt": True, "action": "edit"})

    # Should go to mqtt_select_destination step
    assert result["type"].value == "form"
    assert result["step_id"] == "mqtt_select_destination"
    # Action should be stored
    assert handler._destination_action == "edit"


@pytest.mark.asyncio
async def test_mqtt_delete_destination_action(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test MQTT delete action removes destinations correctly."""
    from custom_components.meraki_ha.const import CONF_MQTT_RELAY_DESTINATIONS

    mock_options_config_entry.options = {
        CONF_MQTT_RELAY_DESTINATIONS: [
            {"name": "Broker A", "host": "a.test.com", "port": 1883},
            {"name": "Broker B", "host": "b.test.com", "port": 1883},
        ]
    }

    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    # Select delete action to go to selection
    result = await handler.async_step_mqtt({"enable_mqtt": True, "action": "delete"})
    assert result["step_id"] == "mqtt_select_destination"

    # Now submit the selection to delete the first broker
    result = await handler.async_step_mqtt_select_destination({"destinations": ["0"]})

    # Should return to mqtt step
    assert result["step_id"] == "mqtt"

    # Only one destination should remain
    remaining = handler.options[CONF_MQTT_RELAY_DESTINATIONS]
    assert len(remaining) == 1
    assert remaining[0]["name"] == "Broker B"


@pytest.mark.asyncio
async def test_mqtt_select_destination_returns_to_mqtt_if_empty(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test selecting destinations with empty list returns to mqtt step."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)
    handler._destination_action = "edit"

    # No destinations configured
    result = await handler.async_step_mqtt_select_destination()

    # Should return to mqtt step
    assert result["step_id"] == "mqtt"


@pytest.mark.asyncio
async def test_mqtt_add_destination_form_and_save(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test adding a new MQTT destination through the form."""
    from custom_components.meraki_ha.const import CONF_MQTT_RELAY_DESTINATIONS

    handler = MerakiOptionsFlowHandler(mock_options_config_entry)
    handler._editing_destination_index = None  # Add mode

    # Submit the destination form
    result = await handler.async_step_mqtt_destination(
        {
            "name": "New Broker",
            "host": "new.mqtt.com",
            "port": 1883,
            "username": "",
            "password": "",
            "use_tls": False,
            "topic_filter": "meraki/v1/mt/#",
        }
    )

    # Should return to mqtt step
    assert result["step_id"] == "mqtt"

    # Destination should be saved
    destinations = handler.options.get(CONF_MQTT_RELAY_DESTINATIONS, [])
    assert len(destinations) == 1
    assert destinations[0]["name"] == "New Broker"
    assert destinations[0]["host"] == "new.mqtt.com"
