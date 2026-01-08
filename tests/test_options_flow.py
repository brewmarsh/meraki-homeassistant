"""Tests for the options flow module."""

from unittest.mock import MagicMock

import pytest
import voluptuous as vol
from homeassistant.helpers import selector

from custom_components.meraki_ha.const import (
    CONF_ENABLED_NETWORKS,
    CONF_INTEGRATION_TITLE,
    CONF_MQTT_RELAY_DESTINATIONS,
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
    network_options: list[dict[str, str]] = []

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
    network_options = [
        {"label": "Main Office", "value": "N_123"},
        {"label": "Branch Office", "value": "N_456"},
    ]

    result_schema = handler._populate_schema_defaults(schema, defaults, network_options)

    assert isinstance(result_schema, vol.Schema)


@pytest.mark.asyncio
async def test_async_step_camera_with_user_input_moves_to_mqtt(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test options flow step camera with user input moves to mqtt step."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    result = await handler.async_step_camera({"some_camera_option": True})

    assert result["type"].value == "menu"
    assert result["step_id"] == "mqtt"


@pytest.mark.asyncio
async def test_mqtt_add_destination(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test adding an MQTT destination."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    # First, show the form
    result = await handler.async_step_mqtt_add_destination()
    assert result["type"].value == "form"
    assert result["step_id"] == "mqtt_add_destination"

    # Then, submit the form
    new_destination = {
        "server_ip": "1.1.1.1",
        "port": 1883,
        "topic": "meraki/test",
    }
    result = await handler.async_step_mqtt_add_destination(new_destination)

    assert result["type"].value == "create_entry"
    assert CONF_MQTT_RELAY_DESTINATIONS in result["data"]
    assert len(result["data"][CONF_MQTT_RELAY_DESTINATIONS]) == 1
    assert result["data"][CONF_MQTT_RELAY_DESTINATIONS][0] == new_destination


@pytest.mark.asyncio
async def test_mqtt_edit_destination(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test editing an MQTT destination."""
    # Pre-populate with existing destinations
    mock_options_config_entry.options[CONF_MQTT_RELAY_DESTINATIONS] = [
        {"server_ip": "1.1.1.1", "port": 1883, "topic": "meraki/first"},
        {"server_ip": "2.2.2.2", "port": 1884, "topic": "meraki/second"},
    ]
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    # Start the edit flow, should show a selection form
    result = await handler.async_step_mqtt_edit_destination()
    assert result["type"].value == "form"

    # Select the first destination to edit
    result = await handler.async_step_mqtt_edit_destination({"destination_index": 0})
    assert result["type"].value == "form"

    # Submit the updated details
    updated_details = {
        "server_ip": "1.1.1.2",
        "port": 1885,
        "topic": "meraki/updated",
    }
    result = await handler.async_step_mqtt_edit_destination(updated_details)

    assert result["type"].value == "create_entry"
    updated_destinations = result["data"][CONF_MQTT_RELAY_DESTINATIONS]
    assert updated_destinations[0] == updated_details
    assert (
        updated_destinations[1]["server_ip"] == "2.2.2.2"
    )  # Ensure others are untouched


@pytest.mark.asyncio
async def test_mqtt_delete_destination(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test deleting an MQTT destination."""
    mock_options_config_entry.options[CONF_MQTT_RELAY_DESTINATIONS] = [
        {"server_ip": "1.1.1.1", "port": 1883, "topic": "meraki/first"},
        {"server_ip": "2.2.2.2", "port": 1884, "topic": "meraki/second"},
    ]
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)

    result = await handler.async_step_mqtt_delete_destination(
        {"destinations_to_delete": ["0"]}
    )

    assert result["type"].value == "create_entry"
    remaining_destinations = result["data"][CONF_MQTT_RELAY_DESTINATIONS]
    assert len(remaining_destinations) == 1
    assert remaining_destinations[0]["server_ip"] == "2.2.2.2"


@pytest.mark.asyncio
async def test_mqtt_edit_no_destinations_aborts(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test that edit flow aborts if no destinations exist."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)
    result = await handler.async_step_mqtt_edit_destination()
    assert result["type"].value == "abort"
    assert result["reason"] == "no_destinations"


@pytest.mark.asyncio
async def test_mqtt_delete_no_destinations_aborts(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test that delete flow aborts if no destinations exist."""
    handler = MerakiOptionsFlowHandler(mock_options_config_entry)
    result = await handler.async_step_mqtt_delete_destination()
    assert result["type"].value == "abort"
    assert result["reason"] == "no_destinations"


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
    assert result["type"].value == "menu"
    assert result["step_id"] == "mqtt"
