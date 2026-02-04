"""Appliance firewall endpoints."""

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


class ApplianceFirewallMixin:
    """Mixin for appliance firewall endpoints."""

    if TYPE_CHECKING:
        _api_client: MerakiApiClientProtocol

    @handle_meraki_errors
    @async_timed_cache()
    async def get_l3_firewall_rules(self, network_id: str) -> dict[str, Any]:
        """
        Get L3 firewall rules for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The L3 firewall rules.

        """
        rules = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules,
            networkId=network_id,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_l3_firewall_rules did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    async def update_l3_firewall_rules(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update L3 firewall rules for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated L3 firewall rules.

        """
        rules = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_l3_firewall_rules did not return a dict")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_appliance_l7_firewall_rules(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """
        Get L7 firewall rules for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The L7 firewall rules.

        """
        rules = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getNetworkApplianceL7FirewallRules,
            networkId=network_id,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_l7_firewall_rules did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_appliance_l7_firewall_rules(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update L7 firewall rules for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated L7 firewall rules.

        """
        rules = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.updateNetworkApplianceL7FirewallRules,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(rules)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "update_network_appliance_l7_firewall_rules did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache()
    async def get_network_appliance_content_filtering(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """
        Get content filtering settings for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The content filtering settings.

        """
        result = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getNetworkApplianceContentFiltering,
            networkId=network_id,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_content_filtering did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=3600)
    async def get_network_appliance_content_filtering_categories(
        self,
        network_id: str,
    ) -> dict[str, Any]:
        """
        Get content filtering categories for a network.

        Args:
            network_id: The ID of the network.

        Returns
        -------
            The content filtering categories.

        """
        result = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getNetworkApplianceContentFilteringCategories,
            networkId=network_id,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_network_appliance_content_filtering_categories "
                "did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_appliance_content_filtering(
        self,
        network_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Update content filtering for a network.

        Args:
            network_id: The ID of the network.
            **kwargs: Additional arguments.

        Returns
        -------
            The updated content filtering settings.

        """
        result = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.updateNetworkApplianceContentFiltering,
            networkId=network_id,
            **kwargs,
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "update_network_appliance_content_filtering did not return a dict",
            )
            return {}
        return validated
