"""Meraki API endpoints for appliances."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.core import HomeAssistant

from .firewall import ApplianceFirewallMixin
from .settings import ApplianceSettingsMixin
from .traffic import ApplianceTrafficMixin
from .uplink import ApplianceUplinkMixin
from .vpn import ApplianceVpnMixin

if TYPE_CHECKING:
    from custom_components.meraki_ha.core.api.protocol import MerakiApiClientProtocol


class ApplianceEndpoints(
    ApplianceTrafficMixin,
    ApplianceFirewallMixin,
    ApplianceUplinkMixin,
    ApplianceVpnMixin,
    ApplianceSettingsMixin,
):
    """Appliance-related endpoints."""

    def __init__(
        self, api_client: MerakiApiClientProtocol, hass: HomeAssistant
    ) -> None:
        """
        Initialize the endpoint.

        Args:
            api_client: The Meraki API client.
            hass: The Home Assistant instance.

        """
        self._api_client = api_client
        self._hass = hass
