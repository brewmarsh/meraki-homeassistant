"""Tests for the _mappers utility module."""

from custom_components.meraki_ha.core.utils._const import DeviceType
from custom_components.meraki_ha.core.utils._mappers import (
    get_device_type_description,
    get_prefixes_for_device_type,
    get_supported_model_prefixes,
    map_meraki_model_to_device_type,
    validate_device_type,
    validate_model_string,
)


# ===== map_meraki_model_to_device_type Tests =====


def test_map_model_to_device_type_mr() -> None:
    """Test mapping MR model to wireless type."""
    assert map_meraki_model_to_device_type("MR33") == DeviceType.WIRELESS
    assert map_meraki_model_to_device_type("MR52") == DeviceType.WIRELESS


def test_map_model_to_device_type_ms() -> None:
    """Test mapping MS model to switch type."""
    assert map_meraki_model_to_device_type("MS120") == DeviceType.SWITCH
    assert map_meraki_model_to_device_type("MS350") == DeviceType.SWITCH


def test_map_model_to_device_type_mx() -> None:
    """Test mapping MX model to appliance type."""
    assert map_meraki_model_to_device_type("MX67") == DeviceType.APPLIANCE
    assert map_meraki_model_to_device_type("MX84") == DeviceType.APPLIANCE


def test_map_model_to_device_type_mv() -> None:
    """Test mapping MV model to camera type."""
    assert map_meraki_model_to_device_type("MV12") == DeviceType.CAMERA
    assert map_meraki_model_to_device_type("MV93") == DeviceType.CAMERA


def test_map_model_to_device_type_mt() -> None:
    """Test mapping MT model to sensor type."""
    assert map_meraki_model_to_device_type("MT10") == DeviceType.SENSOR
    assert map_meraki_model_to_device_type("MT20") == DeviceType.SENSOR


def test_map_model_to_device_type_mg() -> None:
    """Test mapping MG model to cellular type."""
    assert map_meraki_model_to_device_type("MG21") == DeviceType.CELLULAR
    assert map_meraki_model_to_device_type("MG51") == DeviceType.CELLULAR


def test_map_model_to_device_type_network() -> None:
    """Test mapping 'NETWORK' to network type."""
    assert map_meraki_model_to_device_type("NETWORK") == DeviceType.NETWORK
    assert map_meraki_model_to_device_type("network") == DeviceType.NETWORK


def test_map_model_to_device_type_unknown() -> None:
    """Test mapping unknown model to unknown type."""
    assert map_meraki_model_to_device_type("XYZ123") == DeviceType.UNKNOWN
    assert map_meraki_model_to_device_type("Unknown") == DeviceType.UNKNOWN


def test_map_model_to_device_type_none() -> None:
    """Test mapping None returns unknown."""
    assert map_meraki_model_to_device_type(None) == DeviceType.UNKNOWN


def test_map_model_to_device_type_empty() -> None:
    """Test mapping empty string returns unknown."""
    assert map_meraki_model_to_device_type("") == DeviceType.UNKNOWN


def test_map_model_to_device_type_case_insensitive() -> None:
    """Test mapping is case insensitive."""
    assert map_meraki_model_to_device_type("mr33") == DeviceType.WIRELESS
    assert map_meraki_model_to_device_type("MS120") == DeviceType.SWITCH


# ===== validate_model_string Tests =====


def test_validate_model_string_valid_mr() -> None:
    """Test validating MR model strings."""
    assert validate_model_string("MR33") is True
    assert validate_model_string("MR52") is True


def test_validate_model_string_valid_ms() -> None:
    """Test validating MS model strings."""
    assert validate_model_string("MS120") is True
    assert validate_model_string("MS350-24X") is True


def test_validate_model_string_network() -> None:
    """Test validating NETWORK string."""
    assert validate_model_string("NETWORK") is True
    assert validate_model_string("network") is True


def test_validate_model_string_empty() -> None:
    """Test validating empty string returns False."""
    assert validate_model_string("") is False


def test_validate_model_string_none_like() -> None:
    """Test validating invalid strings."""
    assert validate_model_string("invalid") is False


# ===== validate_device_type Tests =====


def test_validate_device_type_valid() -> None:
    """Test validating known device types."""
    assert validate_device_type(DeviceType.WIRELESS) is True
    assert validate_device_type(DeviceType.SWITCH) is True
    assert validate_device_type(DeviceType.APPLIANCE) is True
    assert validate_device_type(DeviceType.CAMERA) is True
    assert validate_device_type(DeviceType.SENSOR) is True


def test_validate_device_type_unknown_valid() -> None:
    """Test unknown is a valid device type."""
    assert validate_device_type(DeviceType.UNKNOWN) is True


def test_validate_device_type_invalid() -> None:
    """Test invalid device type returns False."""
    assert validate_device_type("invalid_type") is False
    assert validate_device_type("random") is False


# ===== get_device_type_description Tests =====


def test_get_device_type_description_wireless() -> None:
    """Test getting description for wireless type."""
    desc = get_device_type_description(DeviceType.WIRELESS)
    assert desc is not None
    assert len(desc) > 0


def test_get_device_type_description_switch() -> None:
    """Test getting description for switch type."""
    desc = get_device_type_description(DeviceType.SWITCH)
    assert desc is not None
    assert len(desc) > 0


def test_get_device_type_description_unknown() -> None:
    """Test getting description for unknown type."""
    desc = get_device_type_description(DeviceType.UNKNOWN)
    assert desc is not None


def test_get_device_type_description_invalid() -> None:
    """Test getting description for invalid type returns unknown description."""
    desc = get_device_type_description("invalid_type")
    expected = get_device_type_description(DeviceType.UNKNOWN)
    assert desc == expected


# ===== get_supported_model_prefixes Tests =====


def test_get_supported_model_prefixes() -> None:
    """Test getting all supported model prefixes."""
    prefixes = get_supported_model_prefixes()

    assert isinstance(prefixes, set)
    assert len(prefixes) > 0
    assert "MR" in prefixes
    assert "MS" in prefixes
    assert "MX" in prefixes


# ===== get_prefixes_for_device_type Tests =====


def test_get_prefixes_for_device_type_wireless() -> None:
    """Test getting prefixes for wireless type."""
    prefixes = get_prefixes_for_device_type(DeviceType.WIRELESS)

    assert isinstance(prefixes, set)
    assert "MR" in prefixes


def test_get_prefixes_for_device_type_switch() -> None:
    """Test getting prefixes for switch type."""
    prefixes = get_prefixes_for_device_type(DeviceType.SWITCH)

    assert isinstance(prefixes, set)
    assert "MS" in prefixes


def test_get_prefixes_for_device_type_invalid() -> None:
    """Test getting prefixes for invalid type returns empty set."""
    prefixes = get_prefixes_for_device_type("invalid_type")

    assert isinstance(prefixes, set)
    assert len(prefixes) == 0

