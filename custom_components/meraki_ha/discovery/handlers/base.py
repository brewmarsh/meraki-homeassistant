"""
Base Device Handler

This module defines the BaseDeviceHandler class, which provides a common
interface for all device-specific handlers.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ....types import MerakiDevice
    from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)


class BaseDeviceHandler:
    """Base class for device-specific entity handlers."""

    def __init__(self, device: MerakiDevice) -> None:
        """Initialize the BaseDeviceHandler."""
        self.device = device

    def discover_entities(self) -> List[Entity]:
        """
        Discover entities for the device.

        This method should be implemented by subclasses to return a list
        of entities for the specific device type.
        """
        raise NotImplementedError("Subclasses must implement discover_entities")
