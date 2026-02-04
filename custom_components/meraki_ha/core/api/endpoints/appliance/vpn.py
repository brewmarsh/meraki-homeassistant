"""Appliance VPN endpoints."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.api.cache import async_timed_cache
from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

if TYPE_CHECKING:
    from custom_components.meraki_ha.core.api.protocol import MerakiApiClientProtocol

_LOGGER = logging.getLogger(__name__)


class ApplianceVpnMixin:
    """Mixin for appliance VPN endpoints."""

    if TYPE_CHECKING:
        _api_client: MerakiApiClientProtocol

    @handle_meraki_errors
    @async_timed_cache()
    async def get_vpn_status(self, network_id: str) -> dict[str, Any]:
        """
        Get site-to-site VPN status for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The VPN status.

        """
        status = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn,
            networkId=network_id,
        )
        validated = validate_response(status)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_vpn_status did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_vpn_status(self, network_id: str, **kwargs: Any) -> dict[str, Any]:
        """
        Update site-to-site VPN status for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated VPN status.

        """
        status = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(status)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_vpn_status did not return a dict")
            return {}
        return validated
