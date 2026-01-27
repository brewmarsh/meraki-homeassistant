import dataclasses
from typing import Any


def to_serializable(obj: Any) -> Any:
    """Recursively convert dataclasses to dictionaries for serialization."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    if isinstance(obj, list):
        return [to_serializable(item) for item in obj]
    if isinstance(obj, dict):
        return {key: to_serializable(value) for key, value in obj.items()}
    return obj
