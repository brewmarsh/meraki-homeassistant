"""Meraki API endpoints for networks."""

import logging
from typing import Any, Dict, List, Optional

from ...utils.api_utils import handle_meraki_errors, validate_response
from ..cache import async_timed_cache

_LOGGER = logging.getLogger(__name__)


class NetworkEndpoints:
    """Network-related endpoints."""

    def __init__(self, api_client):
        """Initialize the endpoint."""
        self._api_client = api_client
        self._dashboard = api_client._dashboard

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_clients(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all clients in a network."""
        _LOGGER.debug("Getting clients for network: %s", network_id)
        clients = await self._api_client._run_sync(
            self._dashboard.networks.getNetworkClients, networkId=network_id
        )
        validated = validate_response(clients)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_clients did not return a list.")
            return []
        return validated




    @handle_meraki_errors
    @async_timed_cache(timeout=10)
    async def get_webhooks(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all webhooks for a network."""
        _LOGGER.debug("Getting webhooks for network %s", network_id)
        webhooks = await self._api_client._run_sync(
            self._dashboard.networks.getNetworkWebhooksHttpServers,
            networkId=network_id,
        )
        return validate_response(webhooks)

    @handle_meraki_errors
    async def delete_webhook(self, network_id: str, webhook_id: str) -> None:
        """Delete a webhook from a network."""
        _LOGGER.debug("Deleting webhook %s from network %s", webhook_id, network_id)
        await self._api_client._run_sync(
            self._dashboard.networks.deleteNetworkWebhooksHttpServer,
            networkId=network_id,
            httpServerId=webhook_id,
        )

    @handle_meraki_errors
    async def find_webhook_by_url(
        self, network_id: str, url: str
    ) -> Optional[Dict[str, Any]]:
        """Find a webhook by its URL."""
        try:
            webhooks = await self.get_webhooks(network_id)
            for webhook in webhooks:
                if webhook.get("url") == url:
                    return webhook
        except Exception:
            pass
        return None

    @handle_meraki_errors
    async def register_webhook(self, webhook_url: str, secret: str) -> None:
        """Register a webhook with the Meraki API."""
        _LOGGER.debug("Registering webhook: %s", webhook_url)
        networks = await self.get_networks()
        for network in networks:
            network_id = network["id"]
            existing_webhook = await self.find_webhook_by_url(network_id, webhook_url)
            if existing_webhook:
                _LOGGER.debug("Found existing webhook, updating...")
                await self.delete_webhook(network_id, existing_webhook["id"])

            _LOGGER.debug("Creating webhook in network %s", network_id)
            await self._api_client._run_sync(
                self._dashboard.networks.createNetworkWebhooksHttpServer,
                networkId=network_id,
                url=webhook_url,
                sharedSecret=secret,
                name=f"Home Assistant Integration - {network.get('name', 'Unknown')}",
            )

    @handle_meraki_errors
    async def unregister_webhook(self, webhook_id: str) -> None:
        """Unregister a webhook with the Meraki API."""
        _LOGGER.debug("Unregistering webhook: %s", webhook_id)
        networks = await self.get_networks()
        for network in networks:
            await self._api_client._run_sync(
                self._dashboard.networks.deleteNetworkWebhooksHttpServer,
                networkId=network["id"],
                httpServerId=webhook_id,
            )
