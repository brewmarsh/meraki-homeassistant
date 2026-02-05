"""Meraki API endpoints for networks."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

import meraki

from custom_components.meraki_ha.core.utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)
from ...errors import MerakiVlansDisabledError
from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..protocol import MerakiApiClientProtocol

_LOGGER = logging.getLogger(__name__)


class NetworkEndpoints:
    """Network-related endpoints."""

    def __init__(self, api_client: MerakiApiClientProtocol) -> None:
        """Initialize the endpoint."""
        self._api_client = api_client

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_clients(
        self,
        network_id: str,
        timespan: int | None = None,
        perPage: int | None = None,
        statuses: list[str] | None = None,
        total_pages: int | str = "all",
    ) -> list[dict[str, Any]]:
        """Get all clients in a network."""
        kwargs: dict[str, Any] = {
            "networkId": network_id,
            "total_pages": total_pages,
        }
        if timespan:
            kwargs["timespan"] = timespan
        if perPage:
            kwargs["perPage"] = perPage
        if statuses:
            kwargs["statuses"] = statuses

        clients = await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkClients,
            **kwargs,
        )
        validated = validate_response(clients)
        return validated if isinstance(validated, list) else []

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_traffic(
        self, network_id: str, device_type: str
    ) -> list[dict[str, Any]]:
        """Get traffic data for a network, filtered by device type."""
        traffic = await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkTraffic,
            networkId=network_id,
            deviceType=device_type,
            timespan=86400,  # 24 hours
        )
        validated = validate_response(traffic)
        return validated if isinstance(validated, list) else []

    @handle_meraki_errors
    @async_timed_cache(timeout=10)
    async def get_webhooks(self, network_id: str) -> list[dict[str, Any]]:
        """Get all webhooks for a network."""
        webhooks = await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkWebhooksHttpServers,
            networkId=network_id,
        )
        validated = validate_response(webhooks)
        return validated if isinstance(validated, list) else []

    @handle_meraki_errors
    async def delete_webhook(self, network_id: str, webhook_id: str) -> None:
        """Delete a webhook from a network."""
        await self._api_client.run_sync(
            self._api_client.dashboard.networks.deleteNetworkWebhooksHttpServer,
            networkId=network_id,
            httpServerId=webhook_id,
        )

    @handle_meraki_errors
    async def find_webhook_by_name_and_url(
        self, network_id: str, name: str, url: str
    ) -> dict[str, Any] | None:
        """Find a webhook by its name and URL."""
        webhooks = await self.get_webhooks(network_id)
        for webhook in webhooks:
            if webhook.get("name") == name and webhook.get("url") == url:
                return webhook
        return None

    @handle_meraki_errors
    async def register_webhook(
        self, webhook_url: str, secret: str, config_entry_id: str
    ) -> None:
        """Register or update a webhook with the Meraki API."""
        networks = await self._api_client.organization.get_organization_networks()
        for network in networks:
            network_id = network["id"]
            webhook_name = f"Home Assistant Webhook - {config_entry_id}"
            
            existing = await self.find_webhook_by_name_and_url(
                network_id, webhook_name, webhook_url
            )
            if existing:
                await self.delete_webhook(network_id, existing["id"])

            await self._api_client.run_sync(
                self._api_client.dashboard.networks.createNetworkWebhooksHttpServer,
                networkId=network_id,
                url=webhook_url,
                sharedSecret=secret,
                name=webhook_name,
            )

    async def get_vlan_data(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get VLAN data for a network with fallback and safety logic.
        
        This method uses product type verification and safe attribute lookup 
        to prevent AttributeError crashes and reduce 429 rate-limiting.
        """
        # 1. Product Type Guard: Only appliances (MX) support this endpoint
        networks = await self._api_client.organization.get_organization_networks()
        network = next((n for n in networks if n["id"] == network_id), None)
        
        if network and "appliance" not in network.get("productTypes", []):
            _LOGGER.debug("Skipping VLAN fetch for non-appliance network %s", network_id)
            return []

        # 2. SDK Safety Guard: Check if the appliance module and method exist
        # This replaces the failing 'networks.getNetworkVlans' call
        appliance = getattr(self._api_client.dashboard, "appliance", None)
        vlan_method = getattr(appliance, "getNetworkApplianceVlans", None)
        
        if not vlan_method:
            _LOGGER.debug("VLAN method not found in SDK for network %s", network_id)
            return []

        try:
            res = await self._api_client.run_sync(
                vlan_method,
                networkId=network_id,
            )
            validated = validate_response(res)
            return cast(list[dict[str, Any]], validated) if isinstance(validated, list) else []
            
        except (meraki.APIError, MerakiVlansDisabledError, AttributeError) as e:
            # Handle specific 400 error indicating VLANs are disabled
            if "vlans are not enabled" in str(e).lower():
                _LOGGER.info("VLANs disabled for network %s (Status 400)", network_id)
            else:
                _LOGGER.debug("VLAN fetch error for %s: %s", network_id, e)
            return []

    @handle_meraki_errors
    @async_timed_cache(timeout=300)
    async def get_group_policies(self, network_id: str) -> list[dict[str, Any]]:
        """Get group policies for a network."""
        policies = await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkGroupPolicies,
            networkId=network_id,
        )
        validated = validate_response(policies)
        return validated if isinstance(validated, list) else []

    @handle_meraki_errors
    async def get_network_events(self, network_id: str, **kwargs) -> dict[str, Any]:
        """Fetch events for a network."""
        # Map snake_case to camelCase for common arguments
        key_map = {
            "product_type": "productType",
            "included_event_types": "includedEventTypes",
            "excluded_event_types": "excludedEventTypes",
            "device_serial": "deviceSerial",
            "sm_owner_id": "smOwnerId",
            "sm_device_mac": "smDeviceMac",
            "sm_user_tags": "smUserTags",
            "starting_after": "startingAfter",
            "ending_before": "endingBefore",
            "per_page": "perPage",
        }

        filtered_kwargs = {}
        for k, v in kwargs.items():
            if v is not None:
                new_key = key_map.get(k, k)
                filtered_kwargs[new_key] = v

        return await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkEvents,
            network_id,
            **filtered_kwargs,
        )