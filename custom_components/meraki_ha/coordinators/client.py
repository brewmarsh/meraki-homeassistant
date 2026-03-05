"""Client coordinator for the Meraki HA integration."""

from __future__ import annotations

import logging
from typing import Any

from .base import MerakiBaseCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiClientCoordinator(MerakiBaseCoordinator[dict[str, Any]]):
    """A coordinator for Meraki client data."""

    def __init__(self, hass, entry) -> None:
        """Initialize the client coordinator."""
        super().__init__(hass, entry, name="client")
        self.last_successful_data: dict[str, Any] = {}

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch client data."""
        try:
            return await self.data_fetch_manager.get_all_data(self.last_successful_data)
        except Exception as err:
            data, _ = self.update_processor.process_failure(
                err, self.last_successful_data
            )
            return data
