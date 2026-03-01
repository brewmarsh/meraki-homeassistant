"""Serialization helpers for Meraki HA."""

from __future__ import annotations

import dataclasses
from typing import Any


def to_serializable(obj: Any) -> Any:
    """Recursively convert objects to JSON-serializable formats."""
    if hasattr(obj, "to_dict"):
        return to_serializable(obj.to_dict())
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        # We don't use asdict directly because we want to recurse with our own logic
        # for nested objects that might not be dataclasses (like Exceptions)
        return {
            field.name: to_serializable(getattr(obj, field.name))
            for field in dataclasses.fields(obj)
        }
    if isinstance(obj, list):
        return [to_serializable(item) for item in obj]
    if isinstance(obj, dict):
        return {str(key): to_serializable(value) for key, value in obj.items()}
    if isinstance(obj, Exception):
        return {
            "error": True,
            "type": obj.__class__.__name__,
            "message": str(obj),
        }
    return obj
