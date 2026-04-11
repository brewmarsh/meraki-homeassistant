"""Appliance traffic endpoints."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.api.cache import async_timed_cache
from custom_components.meraki_ha.core.utils.api import (
    handle_meraki_errors,
    validate_response,
)

if TYPE_CHECKING:
    from custom_components.meraki_ha.core.api.protocol import MerakiApiClientProtocol

_LOGGER = logging.getLogger(__name__)


class ApplianceTrafficMixin:
    """Mixin for appliance traffic endpoints."""

    if TYPE_CHECKING:
        _api_client: MerakiApiClientProtocol

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_appliance_traffic(
        self,
        network_id: str,
        timespan: int = 86400,
    ) -> list[dict[str, Any]]:
        """
        Get traffic data for a network appliance.

        Args:
            network_id: The ID of the network.
            timespan: The timespan for the traffic data.

        Returns
        -------
            A list of traffic data.

        """
        traffic = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getNetworkApplianceTraffic,
            networkId=network_id,
            timespan=timespan,
        )
        validated = validate_response(traffic)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_appliance_traffic did not return a list")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_traffic_shaping(self, network_id: str) -> dict[str, Any]:
        """
        Get traffic shaping settings for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The traffic shaping settings.

        """
        settings = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getNetworkApplianceTrafficShaping,
            networkId=network_id,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_traffic_shaping did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_traffic_shaping(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update traffic shaping settings for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated traffic shaping settings.

        """
        settings = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.updateNetworkApplianceTrafficShaping,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_traffic_shaping did not return a dict")
            return {}
        return validated
