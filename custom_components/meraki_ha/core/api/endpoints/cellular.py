"""Cellular Gateway API endpoints."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)

from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..client import MerakiAPIClient


_LOGGER = logging.getLogger(__name__)


class CellularEndpoint:
    """Cellular Gateway API endpoint."""

    def __init__(self, api_client: MerakiAPIClient) -> None:
        """Initialize the Cellular Gateway endpoint."""
        self._api_client = api_client

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_organization_cellular_gateway_uplink_statuses(
        self,
    ) -> list[dict[str, Any]]:
        """
        Get uplink status for all cellular gateways in the organization.

        Returns
        -------
            A list of uplink statuses with signal info, provider, connection type, etc.

        """
        if self._api_client.dashboard is None:
            return []
        try:
            api = self._api_client.dashboard.cellularGateway
            statuses = await api.getOrganizationCellularGatewayUplinkStatuses(
                organizationId=self._api_client.organization_id,
                total_pages="all",
            )
            validated = validate_response(statuses)
            if not isinstance(validated, list):
                _LOGGER.warning(
                    "get_organization_cellular_gateway_uplink_statuses "
                    "did not return a list",
                )
                return []
            return validated
        except Exception as e:
            _LOGGER.debug("Could not fetch cellular gateway uplinks: %s", e)
            return []
