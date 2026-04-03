"""Tests for the validation utils."""

import pytest
import voluptuous as vol

from custom_components.meraki_ha.core.utils.validation_utils import (
    CONFIG_SCHEMA,
    OPTIONS_SCHEMA,
    validate_api_key,
    validate_org_id,
)


def test_validate_api_key():
    """Test the validate_api_key function."""
    with pytest.raises(vol.Invalid):
        validate_api_key("invalid")
    assert validate_api_key("0" * 40) == "0" * 40


def test_validate_org_id():
    """Test the validate_org_id function."""
    with pytest.raises(vol.Invalid):
        validate_org_id("invalid")
    assert validate_org_id("123456") == "123456"


def test_config_schema():
    """Test the CONFIG_SCHEMA."""
    with pytest.raises(vol.Invalid):
        CONFIG_SCHEMA({})
    with pytest.raises(vol.Invalid):
        CONFIG_SCHEMA({"api_key": "invalid", "organization_id": "123456"})
    with pytest.raises(vol.Invalid):
        CONFIG_SCHEMA({"api_key": "0" * 40, "organization_id": "invalid"})
    # Correct: use an integer for scan_interval so vol.Range works
    # Providing a valid integer (e.g., 60) for scan_interval
    assert CONFIG_SCHEMA(
        {"api_key": "0" * 40, "organization_id": "123456", "scan_interval": 60}
    ) == {
        "api_key": "0" * 40,
        "organization_id": "123456",
        "scan_interval": 60,
    }


def test_options_schema():
    """Test the OPTIONS_SCHEMA."""
    with pytest.raises(vol.Invalid):
        OPTIONS_SCHEMA({"scan_interval": 29})
    # Correct: use an integer for scan_interval so vol.Range(min=30) works
    # Providing a valid integer (e.g., 60) for scan_interval
    assert OPTIONS_SCHEMA({"scan_interval": 60}) == {"scan_interval": 60}
