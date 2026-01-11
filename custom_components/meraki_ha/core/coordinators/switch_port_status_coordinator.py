"""Switch port status coordinator for the Meraki integration."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ...async_logging import async_log_time
from ...helpers.logging_helper import MerakiLoggers

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from ...meraki_data_coordinator import MerakiDataCoordinator
    from ..repository import MerakiRepository

_LOGGER = MerakiLoggers.COORDINATOR


class SwitchPortStatusCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for switch port status data."""

    def __init__(
        self,
        hass: HomeAssistant,
        repository: MerakiRepository,
        main_coordinator: MerakiDataCoordinator,
        config_entry: ConfigEntry,
        update_interval: int = 60,
    ) -> None:
        """Initialize the switch port status coordinator."""
        self.repository = repository
        self.main_coordinator = main_coordinator
        self.config_entry = config_entry

        super().__init__(
            hass,
            _LOGGER,
            name="meraki_switch_port_status",
            update_interval=timedelta(seconds=update_interval),
        )

    @async_log_time(MerakiLoggers.COORDINATOR, slow_threshold=5.0)
    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch switch port status data."""
        port_statuses: dict[str, list[dict[str, Any]]] = {}

        if self.main_coordinator.data:
            devices = self.main_coordinator.data.get("devices", [])
            for device in devices:
                if device.get("productType") == "switch":
                    serial = device.get("serial")
                    if serial:
                        try:
                            statuses = (
                                await self.repository.async_get_switch_port_statuses(
                                    serial
                                )
                            )
                            if statuses:
                                port_statuses[serial] = statuses
                        except Exception as port_err:
                            _LOGGER.debug(
                                "Could not get port statuses for %s: %s",
                                serial,
                                port_err,
                            )

        return {"port_statuses": port_statuses}
