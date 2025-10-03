"""Helper function for setting up all number entities."""

from typing import List
from homeassistant.helpers.entity import Entity


def async_setup_numbers(*args, **kwargs) -> List[Entity]:
    """Set up all number entities from the central coordinator."""
    return []