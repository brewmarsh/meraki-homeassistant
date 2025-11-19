"""Meraki API endpoints for networks."""

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


class NetworkEndpoints:
    """Network-related endpoints."""

    def __init__(self, api_client: MerakiAPIClient) -> None:
        """
        Initialize the endpoint.

        Args:
        ----
            api_client: The Meraki API client.

        """
        self._api_client = api_client

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_clients(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get all clients in a network.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            A list of clients.

        """
        if self._api_client.dashboard is None:
            return []
        clients = await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkClients,
            networkId=network_id,
            total_pages="all",
        )
        validated = validate_response(clients)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_clients did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_traffic(
        self, network_id: str, device_type: str
    ) -> list[dict[str, Any]]:
        """
        Get traffic data for a network, filtered by device type.

        Args:
        ----
            network_id: The ID of the network.
            device_type: The type of device to filter by.

        Returns
        -------
            A list of traffic data.

        """
        if self._api_client.dashboard is None:
            return []
        traffic = await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkTraffic,
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
    async def get_webhooks(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get all webhooks for a network.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            A list of webhooks.

        """
        if self._api_client.dashboard is None:
            return []
        webhooks = await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkWebhooksHttpServers,
            networkId=network_id,
        )
        validated = validate_response(webhooks)
        if not isinstance(validated, list):
            _LOGGER.warning("get_webhooks did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    async def delete_webhook(self, network_id: str, webhook_id: str) -> None:
        """
        Delete a webhook from a network.

        Args:
        ----
            network_id: The ID of the network.
            webhook_id: The ID of the webhook.

        """
        if self._api_client.dashboard is None:
            return
        await self._api_client.run_sync(
            self._api_client.dashboard.networks.deleteNetworkWebhooksHttpServer,
            networkId=network_id,
            httpServerId=webhook_id,
        )

    @handle_meraki_errors
    async def find_webhook_by_url(
        self, network_id: str, url: str
    ) -> dict[str, Any] | None:
        """
        Find a webhook by its URL.

        Args:
        ----
            network_id: The ID of the network.
            url: The URL of the webhook.

        Returns
        -------
            The webhook details, or None if not found.

        """
        webhooks = await self.get_webhooks(network_id)
        for webhook in webhooks:
            if webhook.get("url") == url:
                return webhook
        return None

    @handle_meraki_errors
    async def register_webhook(self, webhook_url: str, secret: str) -> None:
        """
        Register a webhook with the Meraki API.

        Args:
        ----
            webhook_url: The URL of the webhook.
            secret: The secret for the webhook.

        """
        networks = await self._api_client.organization.get_organization_networks()
        for network in networks:
            network_id = network["id"]
            existing_webhook = await self.find_webhook_by_url(network_id, webhook_url)
            if existing_webhook:
                await self.delete_webhook(network_id, existing_webhook["id"])

            if self._api_client.dashboard is None:
                return
            await self._api_client.run_sync(
                self._api_client.dashboard.networks.createNetworkWebhooksHttpServer,
                networkId=network_id,
                url=webhook_url,
                sharedSecret=secret,
                name=f"Home Assistant Integration - {network.get('name', 'Unknown')}",
            )

    @handle_meraki_errors
    async def unregister_webhook(self, webhook_url: str) -> None:
        """
        Unregister a webhook with the Meraki API.

        Args:
        ----
            webhook_url: The URL of the webhook to unregister.

        """
        networks = await self._api_client.organization.get_organization_networks()
        for network in networks:
            network_id = network["id"]
            webhook_to_delete = await self.find_webhook_by_url(network_id, webhook_url)
            if webhook_to_delete and "id" in webhook_to_delete:
                _LOGGER.debug(
                    "Deleting webhook %s from network %s",
                    webhook_to_delete["id"],
                    network_id,
                )
                await self.delete_webhook(network_id, webhook_to_delete["id"])

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    async def get_network_camera_analytics_history(
        self, network_id: str, object_type: str
    ) -> list[dict[str, Any]]:
        """
        Get analytics history for a network.

        Args:
        ----
            network_id: The ID of the network.
            object_type: The type of object to get analytics for.

        Returns
        -------
            A list of analytics history.

        """
        if self._api_client.dashboard is None:
            return []
        history = await self._api_client.run_sync(
            self._api_client.dashboard.camera.getNetworkCameraAnalyticsRecent,
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
