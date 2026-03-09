"""Data utilities for Meraki integration."""

from typing import Any


def ensure_list_of_strings(data: list[Any] | None, key_to_extract: str = "name") -> list[str]:
    """Ensure that the input data is a list of strings.

    If an element is a dictionary, extract the value of key_to_extract.
    If the element is already a string, keep it.
    If the element is None or of another type, ignore it to maintain a clean string list.
    """
    if not data or not isinstance(data, list):
        return []

    result: list[str] = []
    for item in data:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, dict):
            value = item.get(key_to_extract)
            if value is not None:
                result.append(str(value))

    return result
