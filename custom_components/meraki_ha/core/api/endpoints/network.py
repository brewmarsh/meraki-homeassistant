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
    async def getNetworkClients(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all clients in a network."""
        clients = await self._api_client._run_sync(
            self._dashboard.networks.getNetworkClients, networkId=network_id
        )
        validated = validate_response(clients)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_clients did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def getNetworkTraffic(
        self, network_id: str, device_type: str
    ) -> List[Dict[str, Any]]:
        """Get traffic data for a network, filtered by device type."""
        traffic = await self._api_client._run_sync(
            self._dashboard.networks.getNetworkTraffic,
            networkId=network_id,
            deviceType=device_type,
            timespan=86400,  # 24 hours
        )
        validated = validate_response(traffic)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_traffic did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=10)
    async def getWebhooks(self, network_id: str) -> List[Dict[str, Any]]:
        """Get all webhooks for a network."""
        webhooks = await self._api_client._run_sync(
            self._dashboard.networks.getNetworkWebhooksHttpServers,
            networkId=network_id,
        )
        validated = validate_response(webhooks)
        if not isinstance(validated, list):
            _LOGGER.warning("get_webhooks did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    async def deleteWebhook(self, network_id: str, webhook_id: str) -> None:
        """Delete a webhook from a network."""
        await self._api_client._run_sync(
            self._dashboard.networks.deleteNetworkWebhooksHttpServer,
            networkId=network_id,
            httpServerId=webhook_id,
        )

    @handle_meraki_errors
    async def findWebhookByUrl(
        self, network_id: str, url: str
    ) -> Optional[Dict[str, Any]]:
        """Find a webhook by its URL."""
        try:
            webhooks = await self.getWebhooks(network_id)
            for webhook in webhooks:
                if webhook.get("url") == url:
                    return webhook
        except Exception:
            pass
        return None

    @handle_meraki_errors
    async def registerWebhook(self, webhook_url: str, secret: str) -> None:
        """Register a webhook with the Meraki API."""
        networks = await self._api_client.organization.getOrganizationNetworks()
        for network in networks:
            network_id = network["id"]
            existing_webhook = await self.findWebhookByUrl(network_id, webhook_url)
            if existing_webhook:
                await self.deleteWebhook(network_id, existing_webhook["id"])

            await self._api_client._run_sync(
                self._dashboard.networks.createNetworkWebhooksHttpServer,
                networkId=network_id,
                url=webhook_url,
                sharedSecret=secret,
                name=f"Home Assistant Integration - {network.get('name', 'Unknown')}",
            )

    @handle_meraki_errors
    async def unregisterWebhook(self, webhook_id: str) -> None:
        """Unregister a webhook with the Meraki API."""
        networks = await self._api_client.organization.getOrganizationNetworks()
        for network in networks:
            await self._api_client._run_sync(
                self._dashboard.networks.deleteNetworkWebhooksHttpServer,
                networkId=network["id"],
                httpServerId=webhook_id,
            )

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def getNetworkCameraAnalyticsHistory(
        self, network_id: str, object_type: str
    ) -> List[Dict[str, Any]]:
        """Get analytics history for a network."""
        history = await self._api_client._run_sync(
            self._dashboard.camera.get_network_camera_analytics_recent,
            networkId=network_id,
            objectType=object_type,
        )
        validated = validate_response(history)
        if not isinstance(validated, list):
            _LOGGER.warning(
                "get_network_camera_analytics_history did not return a list."
            )
            return []
        return validated
