"""Test serialization helpers."""

import dataclasses
from typing import Any

from custom_components.meraki_ha.helpers.serialization import to_serializable


@dataclasses.dataclass
class MockData:
    """Mock dataclass for testing."""

    name: str
    value: int


@dataclasses.dataclass
class NestedMock:
    """Nested mock dataclass."""

    data: MockData
    err: Exception


class MockWithToDict:
    """Mock class with to_dict method."""

    def __init__(self, value: Any) -> None:
        """Initialize."""
        self.value = value

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict."""
        return {"value": self.value}


def test_to_serializable_basic():
    """Test to_serializable with basic types."""
    assert to_serializable(1) == 1
    assert to_serializable("test") == "test"
    assert to_serializable([1, 2]) == [1, 2]
    assert to_serializable({"key": "value"}) == {"key": "value"}


def test_to_serializable_dataclass():
    """Test to_serializable with dataclass."""
    data = MockData(name="test", value=123)
    assert to_serializable(data) == {"name": "test", "value": 123}


def test_to_serializable_to_dict():
    """Test to_serializable with to_dict method."""
    obj = MockWithToDict(value=1)
    assert to_serializable(obj) == {"value": 1}


def test_to_serializable_exception():
    """Test to_serializable with exception."""
    err = ValueError("Invalid value")
    result = to_serializable(err)
    assert result == {
        "error": True,
        "type": "ValueError",
        "message": "Invalid value",
    }


def test_to_serializable_recursive():
    """Test to_serializable recursively."""
    err = ValueError("boom")
    data = {
        "list": [MockData(name="sub", value=1), err],
        "dict": {"nested_err": err},
    }
    result = to_serializable(data)
    expected_err = {
        "error": True,
        "type": "ValueError",
        "message": "boom",
    }
    assert result == {
        "list": [{"name": "sub", "value": 1}, expected_err],
        "dict": {"nested_err": expected_err},
    }


def test_to_serializable_nested_dataclass_exception():
    """Test to_serializable with exception nested in dataclass."""
    err = ValueError("nested boom")
    data = MockData(name="sub", value=1)
    nested = NestedMock(data=data, err=err)
    result = to_serializable(nested)
    assert result == {
        "data": {"name": "sub", "value": 1},
        "err": {
            "error": True,
            "type": "ValueError",
            "message": "nested boom",
        },
    }


def test_to_serializable_nested_to_dict_exception():
    """Test to_serializable with exception nested in to_dict result."""
    err = ValueError("to_dict boom")
    obj = MockWithToDict(value=err)
    result = to_serializable(obj)
    assert result == {
        "value": {
            "error": True,
            "type": "ValueError",
            "message": "to_dict boom",
        },
    }


def test_to_serializable_dict_keys_stringified():
    """Test to_serializable stringifies dict keys."""
    data = {1: "one", 2: "two"}
    result = to_serializable(data)
    assert result == {"1": "one", "2": "two"}
