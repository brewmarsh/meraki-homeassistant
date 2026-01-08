"""Tests for the options flow module."""

from unittest.mock import MagicMock

import pytest
import voluptuous as vol
from homeassistant.helpers import selector

from custom_components.meraki_ha.const import (
    CONF_ENABLED_NETWORKS,
    CONF_MQTT_RELAY_DESTINATIONS,
    DOMAIN,
)
from custom_components.meraki_ha.options_flow import MerakiOptionsFlowHandler


@pytest.fixture
def mock_options_config_entry() -> MagicMock:
    """Create a mock config entry for options flow."""

    def _mock_entry(options: dict | None = None) -> MagicMock:
        entry = MagicMock()
        entry.entry_id = "test_entry_id"
        entry.options = options or {
            "scan_interval": 30,
            "enable_device_status": True,
        }
        return entry

    return _mock_entry


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
    entry = mock_options_config_entry()
    handler = MerakiOptionsFlowHandler(entry)

    assert handler.options == entry.options
    assert handler.options["scan_interval"] == 30
    assert handler.options["enable_device_status"] is True


@pytest.mark.asyncio
async def test_async_step_init_with_user_input_moves_to_dashboard(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test options flow step init with user input moves to dashboard step."""
    entry = mock_options_config_entry()
    handler = MerakiOptionsFlowHandler(entry)

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
    entry = mock_options_config_entry()
    handler = MerakiOptionsFlowHandler(entry)

    result = await handler.async_step_dashboard({"some_dashboard_option": True})

    # Dashboard step should move to camera step, returning a form
    assert result["type"].value == "form"
    assert result["step_id"] == "camera"


@pytest.mark.asyncio
async def test_async_step_camera_with_user_input_moves_to_mqtt(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test options flow step camera with user input moves to mqtt step."""
    entry = mock_options_config_entry()
    handler = MerakiOptionsFlowHandler(entry)

    result = await handler.async_step_camera({"some_camera_option": True})

    # Camera step should move to mqtt step, returning a menu
    assert result["type"].value == "menu"
    assert result["step_id"] == "mqtt"


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
async def test_full_options_flow_creates_entry(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test complete options flow from start to entry creation."""
    # Start with initial options
    entry = mock_options_config_entry(
        {
            "scan_interval": 30,
            "enable_device_status": True,
            "temperature_unit": "celsius",
        }
    )

    handler = MerakiOptionsFlowHandler(entry)

    # Step 1: init -> goes to dashboard
    result = await handler.async_step_init({"scan_interval": 120})
    assert result["step_id"] == "dashboard"

    # Step 2: dashboard -> goes to camera
    result = await handler.async_step_dashboard({})
    assert result["step_id"] == "camera"

    # Step 3: camera -> goes to mqtt
    result = await handler.async_step_camera({})
    assert result["step_id"] == "mqtt"

    # Step 4: mqtt -> creates entry (simulating choosing an option)
    # Here we'll simulate adding a destination
    result = await handler.async_step_mqtt_add_destination(
        {"server_ip": "1.2.3.4", "port": 1883, "topic": "meraki/events"}
    )
    assert result["type"].value == "create_entry"

    # New value should be applied
    assert result["data"]["scan_interval"] == 120
    # Existing values should be preserved
    assert result["data"]["enable_device_status"] is True
    assert result["data"]["temperature_unit"] == "celsius"


@pytest.mark.asyncio
async def test_mqtt_edit_destination_flow(mock_options_config_entry: MagicMock) -> None:
    """Test the complete flow for editing an MQTT destination."""
    entry = mock_options_config_entry(
        {
            CONF_MQTT_RELAY_DESTINATIONS: [
                {"server_ip": "1.1.1.1", "port": 1883, "topic": "topic1"},
                {"server_ip": "2.2.2.2", "port": 1884, "topic": "topic2"},
            ]
        }
    )
    handler = MerakiOptionsFlowHandler(entry)

    # Start the edit flow, should show a selection form
    result = await handler.async_step_mqtt_edit_destination()
    assert result["type"].value == "form"
    assert "destination_index" in result["data_schema"].schema

    # Simulate user selecting the first destination (index 0)
    result = await handler.async_step_mqtt_edit_destination(
        {"destination_index": 0}
    )
    assert result["type"].value == "form"
    assert "server_ip" in result["data_schema"].schema
    # Check that the form is pre-filled
    server_ip_marker = next(
        key for key in result["data_schema"].schema if key.schema == "server_ip"
    )
    assert (
        server_ip_marker.default() == "1.1.1.1"
    ), "Form should be pre-filled with the correct IP"

    # Simulate user submitting new details
    updated_details = {
        "server_ip": "1.1.1.10",
        "port": 1885,
        "topic": "topic1_updated",
    }
    result = await handler.async_step_mqtt_edit_destination(updated_details)
    assert result["type"].value == "create_entry"
    # Verify that the destination was updated
    updated_destinations = result["data"][CONF_MQTT_RELAY_DESTINATIONS]
    assert updated_destinations[0] == updated_details
    assert (
        updated_destinations[1]["server_ip"] == "2.2.2.2"
    )  # Ensure others are untouched


@pytest.mark.asyncio
async def test_mqtt_delete_destination_flow(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test the complete flow for deleting MQTT destinations."""
    entry = mock_options_config_entry(
        {
            CONF_MQTT_RELAY_DESTINATIONS: [
                {"server_ip": "1.1.1.1", "port": 1883, "topic": "topic1"},
                {"server_ip": "2.2.2.2", "port": 1884, "topic": "topic2"},
                {"server_ip": "3.3.3.3", "port": 1885, "topic": "topic3"},
            ]
        }
    )
    handler = MerakiOptionsFlowHandler(entry)

    # Start the delete flow, should show a multi-select form
    result = await handler.async_step_mqtt_delete_destination()
    assert result["type"].value == "form"
    assert "destinations_to_delete" in result["data_schema"].schema

    # Simulate user selecting the first and third destinations to delete
    result = await handler.async_step_mqtt_delete_destination(
        {"destinations_to_delete": ["0", "2"]}
    )
    assert result["type"].value == "create_entry"
    # Verify that the correct destinations were deleted
    remaining_destinations = result["data"][CONF_MQTT_RELAY_DESTINATIONS]
    assert len(remaining_destinations) == 1
    assert remaining_destinations[0]["server_ip"] == "2.2.2.2"


@pytest.mark.asyncio
async def test_mqtt_edit_delete_with_no_destinations_aborts(
    mock_options_config_entry: MagicMock,
) -> None:
    """Test that edit/delete flows abort if no destinations are configured."""
    entry = mock_options_config_entry({CONF_MQTT_RELAY_DESTINATIONS: []})
    handler = MerakiOptionsFlowHandler(entry)

    # Edit flow should abort
    result = await handler.async_step_mqtt_edit_destination()
    assert result["type"].value == "abort"
    assert result["reason"] == "no_destinations"

    # Delete flow should abort
    result = await handler.async_step_mqtt_delete_destination()
    assert result["type"].value == "abort"
    assert result["reason"] == "no_destinations"
