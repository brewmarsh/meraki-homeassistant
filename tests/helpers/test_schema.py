"""Test the schema helpers."""

import voluptuous as vol
from homeassistant.helpers import selector
from custom_components.meraki_ha.helpers.schema import populate_schema_defaults
from custom_components.meraki_ha.const import CONF_IGNORED_NETWORKS

def test_populate_schema_defaults():
    """Test populating schema defaults."""
    schema = vol.Schema({
        vol.Required("test_option", default="default"): str,
        vol.Optional(CONF_IGNORED_NETWORKS): selector.SelectSelector(
            selector.SelectSelectorConfig(options=[])
        ),
    })

    defaults = {
        "test_option": "new_value",
    }

    network_options = [
        {"label": "Network 1", "value": "net1"},
        {"label": "Network 2", "value": "net2"},
    ]

    new_schema = populate_schema_defaults(schema, defaults, network_options)

    # Check if default value is updated
    for key, value in new_schema.schema.items():
        if key.schema == "test_option":
            assert key.default() == "new_value"

        if key.schema == CONF_IGNORED_NETWORKS:
            assert isinstance(value, selector.SelectSelector)
            assert value.config["options"] == network_options

def test_populate_schema_defaults_no_defaults():
    """Test populating schema defaults with no defaults provided."""
    schema = vol.Schema({
        vol.Required("test_option", default="default"): str,
    })

    defaults = {}
    network_options = []

    new_schema = populate_schema_defaults(schema, defaults, network_options)

    for key, value in new_schema.schema.items():
        if key.schema == "test_option":
            assert key.default() == "default"
