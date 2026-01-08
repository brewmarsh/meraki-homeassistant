"""SSID Firewall coordinator for the Meraki integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from ..api.client import MerakiAPIClient

_LOGGER = logging.getLogger(__name__)


class SsidFirewallCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for SSID firewall rules."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: MerakiAPIClient,
        network_id: str,
        ssid_number: int,
        scan_interval: int = 300,
        update_interval: int | None = None,
    ) -> None:
        """Initialize the SSID firewall coordinator."""
        self.api_client = api_client
        self.network_id = network_id
        self.ssid_number = ssid_number

        # Support both scan_interval and update_interval for compatibility
        interval = update_interval if update_interval is not None else scan_interval

        super().__init__(
            hass,
            _LOGGER,
            name=f"meraki_ssid_firewall_{network_id}_{ssid_number}",
            update_interval=timedelta(seconds=interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch SSID firewall data from the API."""
        try:
            wireless = self.api_client.wireless
            rules = await wireless.get_network_wireless_ssid_l7_firewall_rules(
                network_id=self.network_id,
                number=str(self.ssid_number),
            )
            return {"rules": rules}
        except Exception as err:
            raise UpdateFailed(f"Error fetching SSID firewall data: {err}") from err
