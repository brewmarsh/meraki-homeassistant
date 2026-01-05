"""Switch port status coordinator for the Meraki integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from ..repository import MerakiRepository

_LOGGER = logging.getLogger(__name__)


class SwitchPortStatusCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for switch port status data."""

    def __init__(
        self,
        hass: HomeAssistant,
        repository: MerakiRepository,
        update_interval: int = 60,
    ) -> None:
        """Initialize the switch port status coordinator."""
        self.repository = repository

        super().__init__(
            hass,
            _LOGGER,
            name="meraki_switch_port_status",
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch switch port status data."""
        try:
            # Get all switch devices and their port statuses
            port_statuses: dict[str, list[dict[str, Any]]] = {}
            devices = await self.repository.get_devices()

            for device in devices:
                if device.get("productType") == "switch":
                    serial = device.get("serial")
                    if serial:
                        try:
                            statuses = await self.repository.get_switch_port_statuses(
                                serial
                            )
                            port_statuses[serial] = statuses
                        except Exception as port_err:
                            _LOGGER.debug(
                                "Could not get port statuses for %s: %s",
                                serial,
                                port_err,
                            )

            return {"port_statuses": port_statuses}
        except Exception as err:
            raise UpdateFailed(f"Error fetching switch port data: {err}") from err

