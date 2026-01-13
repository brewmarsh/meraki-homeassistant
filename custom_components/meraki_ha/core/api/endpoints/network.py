"""Meraki API endpoints for networks."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
import meraki

from custom_components.meraki_ha.core.errors import MerakiTrafficAnalysisError
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
import meraki

from custom_components.meraki_ha.core.errors import MerakiTrafficAnalysisError
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
<<<<<<< HEAD
        self._dashboard = api_client.dashboard
=======
<<<<<<< HEAD
        self._dashboard = api_client.dashboard
=======
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

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
<<<<<<< HEAD
<<<<<<< HEAD
        clients = await self._api_client.run_sync(
            self._dashboard.networks.getNetworkClients,
=======
<<<<<<< HEAD
        clients = await self._api_client.run_sync(
            self._dashboard.networks.getNetworkClients,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return []
        clients = await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkClients,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
        traffic = await self._api_client.run_sync(
            self._dashboard.networks.getNetworkTraffic,
            networkId=network_id,
            deviceType=device_type,
            timespan=86400,  # 24 hours
        )
<<<<<<< HEAD
=======
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return []
        try:
            traffic = await self._api_client.run_sync(
                self._api_client.dashboard.networks.getNetworkTraffic,
                networkId=network_id,
                deviceType=device_type,
                timespan=86400,  # 24 hours
            )
        except meraki.APIError as e:
            if "Traffic Analysis with Hostname Visibility must be enabled" in str(e):
                _LOGGER.info(
                    "Traffic analysis is not enabled for network %s. "
                    "Please enable it at "
                    "https://documentation.meraki.com/MX/Design_and_Configure/Configuration_Guides/Firewall_and_Traffic_Shaping/Traffic_Analysis_and_Classification",
                    network_id,
                )
                raise MerakiTrafficAnalysisError(
                    f"Traffic analysis not enabled for network {network_id}"
                ) from e
            raise
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
<<<<<<< HEAD
        webhooks = await self._api_client.run_sync(
            self._dashboard.networks.getNetworkWebhooksHttpServers,
=======
<<<<<<< HEAD
        webhooks = await self._api_client.run_sync(
            self._dashboard.networks.getNetworkWebhooksHttpServers,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return []
        webhooks = await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkWebhooksHttpServers,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
<<<<<<< HEAD
        await self._api_client.run_sync(
            self._dashboard.networks.deleteNetworkWebhooksHttpServer,
=======
<<<<<<< HEAD
        await self._api_client.run_sync(
            self._dashboard.networks.deleteNetworkWebhooksHttpServer,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return
        await self._api_client.run_sync(
            self._api_client.dashboard.networks.deleteNetworkWebhooksHttpServer,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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

<<<<<<< HEAD
<<<<<<< HEAD
            await self._api_client.run_sync(
                self._dashboard.networks.createNetworkWebhooksHttpServer,
=======
<<<<<<< HEAD
            await self._api_client.run_sync(
                self._dashboard.networks.createNetworkWebhooksHttpServer,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            if self._api_client.dashboard is None:
                return
            await self._api_client.run_sync(
                self._api_client.dashboard.networks.createNetworkWebhooksHttpServer,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
                networkId=network_id,
                url=webhook_url,
                sharedSecret=secret,
                name=f"Home Assistant Integration - {network.get('name', 'Unknown')}",
            )

    @handle_meraki_errors
<<<<<<< HEAD
<<<<<<< HEAD
    async def unregister_webhook(self, webhook_id: str) -> None:
=======
<<<<<<< HEAD
    async def unregister_webhook(self, webhook_id: str) -> None:
=======
    async def unregister_webhook(self, webhook_url: str) -> None:
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
    async def unregister_webhook(self, webhook_url: str) -> None:
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        """
        Unregister a webhook with the Meraki API.

        Args:
        ----
<<<<<<< HEAD
<<<<<<< HEAD
            webhook_id: The ID of the webhook.
=======
<<<<<<< HEAD
            webhook_id: The ID of the webhook.
=======
            webhook_url: The URL of the webhook to unregister.
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
            webhook_url: The URL of the webhook to unregister.
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

        """
        networks = await self._api_client.organization.get_organization_networks()
        for network in networks:
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
            await self._api_client.run_sync(
                self._dashboard.networks.deleteNetworkWebhooksHttpServer,
                networkId=network["id"],
                httpServerId=webhook_id,
            )
<<<<<<< HEAD
=======
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
            network_id = network["id"]
            webhook_to_delete = await self.find_webhook_by_url(network_id, webhook_url)
            if webhook_to_delete and "id" in webhook_to_delete:
                _LOGGER.debug(
                    "Deleting webhook %s from network %s",
                    webhook_to_delete["id"],
                    network_id,
                )
                await self.delete_webhook(network_id, webhook_to_delete["id"])
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

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
<<<<<<< HEAD
<<<<<<< HEAD
        history = await self._api_client.run_sync(
            self._dashboard.camera.getNetworkCameraAnalyticsRecent,
=======
<<<<<<< HEAD
        history = await self._api_client.run_sync(
            self._dashboard.camera.getNetworkCameraAnalyticsRecent,
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
        if self._api_client.dashboard is None:
            return []
        history = await self._api_client.run_sync(
            self._api_client.dashboard.camera.getNetworkCameraAnalyticsRecent,
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)

    @handle_meraki_errors
    @async_timed_cache(timeout=300)
    async def get_network_group_policies(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get all group policies for a network.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            A list of group policies.

        """
        if self._api_client.dashboard is None:
            return []
        policies = await self._api_client.run_sync(
            self._api_client.dashboard.networks.getNetworkGroupPolicies,
            networkId=network_id,
        )
        validated = validate_response(policies)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_group_policies did not return a list.")
            return []
        return validated
<<<<<<< HEAD
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
=======
>>>>>>> 2aed98c0 (fix(config_flow): Resolve CI and HACS validation failures)
