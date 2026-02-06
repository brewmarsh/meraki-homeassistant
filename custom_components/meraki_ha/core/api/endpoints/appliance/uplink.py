"""Appliance uplink endpoints."""

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


class ApplianceUplinkMixin:
    """Mixin for appliance uplink endpoints."""

    if TYPE_CHECKING:
        _api_client: MerakiApiClientProtocol

    @handle_meraki_errors
    @async_timed_cache()
    async def get_device_appliance_uplinks_settings(
        self,
        serial: str,
    ) -> dict[str, Any]:
        """
        Get uplinks settings for a device.

        Args:
            serial: The serial number of the device.

        Returns
        -------
            The uplinks settings.

        """
        uplinks = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getDeviceApplianceUplinksSettings,
            serial=serial,
        )
        validated = validate_response(uplinks)
        if not isinstance(validated, dict):
            _LOGGER.warning(
                "get_device_appliance_uplinks_settings did not return a dict",
            )
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_appliance_uplinks_loss_and_latency(
        self,
        network_id: str,
    ) -> list[dict[str, Any]]:
        """
        Get uplink loss and latency for all devices in a network.

        Args:
            network_id: The network ID.

        Returns
        -------
            A list of uplink loss and latency metrics.

        """
        # SDK method names vary across versions; try each known variant
        sdk_methods = [
            "getNetworkApplianceUplinksUplinksLossAndLatency",
            "getNetworkApplianceUplinksLossAndLatency",
            "getNetworkApplianceUplinksUsageHistory",
        ]

        method = None
        for method_name in sdk_methods:
            if hasattr(self._api_client.dashboard.appliance, method_name):
                method = getattr(self._api_client.dashboard.appliance, method_name)
                break

        if not method:
            _LOGGER.warning("Uplink performance method not found in Meraki SDK")
            return []

        performance = await self._api_client.run_sync(
            method,
            networkId=network_id,
        )
        validated = validate_response(performance)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_network_appliance_uplinks_loss_and_latency did not return a list",
            )
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_organization_appliance_uplink_statuses(self) -> list[dict[str, Any]]:
        """
        Get uplink status for all appliances in the organization.

        Returns
        -------
            A list of uplink statuses.

        """
        statuses = await self._api_client.run_sync(
            self._api_client.dashboard.appliance.getOrganizationApplianceUplinkStatuses,
            organizationId=self._api_client.organization_id,
            total_pages="all",
        )
        validated = validate_response(statuses)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_organization_appliance_uplink_statuses did not return a list",
            )
            return []
        return validated
