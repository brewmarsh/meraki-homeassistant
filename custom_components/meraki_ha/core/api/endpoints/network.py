"""Meraki API endpoints for networks."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from meraki.exceptions import AsyncAPIError

from ....async_logging import async_log_time
from ....helpers.logging_helper import MerakiLoggers
from ...errors import MerakiTrafficAnalysisError
from ...utils.api_utils import (
    handle_meraki_errors,
    validate_response,
)
from ..cache import async_timed_cache

if TYPE_CHECKING:
    from ..client import MerakiAPIClient


_LOGGER = MerakiLoggers.API


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
    @async_log_time(slow_threshold=3.0)
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
        api = self._api_client.dashboard.networks
        clients = await api.getNetworkClients(networkId=network_id, total_pages="all")
        validated = validate_response(clients)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_clients did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    @async_log_time(MerakiLoggers.API)
    async def get_network_client(
        self,
        network_id: str,
        client_id: str,
    ) -> dict[str, Any] | None:
        """Get a single client by MAC or ID."""
        if self._api_client.dashboard is None:
            return None
        api = self._api_client.dashboard.networks
        client = await api.getNetworkClient(
            networkId=network_id,
            clientId=client_id,
        )
        validated = validate_response(client)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_client did not return a dict.")
            return None
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=60)
    @async_log_time(slow_threshold=3.0)
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
        api = self._api_client.dashboard.networks
        try:
            traffic = await api.getNetworkTraffic(
                networkId=network_id,
                deviceType=device_type,
                timespan=86400,  # 24 hours
            )
        except AsyncAPIError as e:
            if "Traffic Analysis with Hostname Visibility must be enabled" in str(e):
                _LOGGER.info(
                    "Traffic analysis is not enabled for network %s. "
                    "Please enable it at "
                    "https://documentation.meraki.com/MX/Design_and_Configure/"
                    "Configuration_Guides/Firewall_and_Traffic_Shaping/"
                    "Traffic_Analysis_and_Classification",
                    network_id,
                )
                raise MerakiTrafficAnalysisError(
                    f"Traffic analysis not enabled for network {network_id}"
                ) from e
            raise
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
        api = self._api_client.dashboard.networks
        webhooks = await api.getNetworkWebhooksHttpServers(networkId=network_id)
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
        api = self._api_client.dashboard.networks
        await api.deleteNetworkWebhooksHttpServer(
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
    async def find_webhook_by_name(
        self, network_id: str, name: str
    ) -> dict[str, Any] | None:
        """
        Find a webhook by its name.

        Args:
        ----
            network_id: The ID of the network.
            name: The name of the webhook.

        Returns
        -------
            The webhook details, or None if not found.

        """
        webhooks = await self.get_webhooks(network_id)
        for webhook in webhooks:
            if webhook.get("name") == name:
                return webhook
        return None

    @handle_meraki_errors
    async def find_webhook_by_name_and_url(
        self, network_id: str, name: str, url: str
    ) -> dict[str, Any] | None:
        """
        Find a webhook by its name and URL.

        Args:
        ----
            network_id: The ID of the network.
            name: The name of the webhook.
            url: The URL of the webhook.

        Returns
        -------
            The webhook details, or None if not found.

        """
        webhooks = await self.get_webhooks(network_id)
        for webhook in webhooks:
            if webhook.get("name") == name and webhook.get("url") == url:
                return webhook
        return None

    @handle_meraki_errors
    async def register_webhook(
        self, webhook_url: str, secret: str, config_entry_id: str
    ) -> None:
        """
        Register a webhook with the Meraki API and subscribe to alerts.

        This performs two operations for each network:
        1. Creates an HTTP server (webhook endpoint) in the Meraki Dashboard
        2. Subscribes the webhook to receive default alerts

        Args:
        ----
            webhook_url: The URL of the webhook.
            secret: The secret for the webhook.
            config_entry_id: The config entry ID.

        """
        networks = await self._api_client.organization.get_organization_networks()
        webhook_name = f"Home Assistant Webhook - {config_entry_id}"

        for network in networks:
            network_id = network["id"]

            # Check for existing webhook with same name
            existing_webhook = await self.find_webhook_by_name(network_id, webhook_name)
            http_server_id = None

            if existing_webhook:
                # Check if URL matches - if so, we can reuse it
                if existing_webhook.get("url") == webhook_url:
                    http_server_id = existing_webhook.get("id")
                    _LOGGER.debug(
                        "Reusing existing webhook %s for network %s",
                        http_server_id,
                        network_id,
                    )
                else:
                    # URL changed, delete and recreate
                    await self.delete_webhook(network_id, existing_webhook["id"])
                    _LOGGER.debug(
                        "Deleted outdated webhook for network %s (URL changed)",
                        network_id,
                    )

            # Create new webhook if needed
            if not http_server_id:
                if self._api_client.dashboard is None:
                    return

                api = self._api_client.dashboard.networks
                try:
                    result = await api.createNetworkWebhooksHttpServer(
                        networkId=network_id,
                        url=webhook_url,
                        sharedSecret=secret,
                        name=webhook_name,
                    )
                    http_server_id = result.get("id") if result else None
                    _LOGGER.info(
                        "Created webhook HTTP server %s for network %s",
                        http_server_id,
                        network_id,
                    )
                except Exception as e:
                    _LOGGER.warning(
                        "Failed to create webhook for network %s: %s",
                        network_id,
                        e,
                    )
                    continue

            # Subscribe the webhook to receive alerts
            if http_server_id:
                await self.subscribe_webhook_to_alerts(network_id, http_server_id)

    @handle_meraki_errors
    async def unregister_webhook(self, config_entry_id: str) -> None:
        """
        Unregister a webhook with the Meraki API.

        Args:
        ----
            config_entry_id: The config entry ID of the webhook to unregister.

        """
        webhook_name = f"Home Assistant Webhook - {config_entry_id}"
        networks = await self._api_client.organization.get_organization_networks()
        for network in networks:
            network_id = network["id"]
            webhook_to_delete = await self.find_webhook_by_name(
                network_id, webhook_name
            )
            if webhook_to_delete and "id" in webhook_to_delete:
                _LOGGER.debug(
                    "Deleting webhook %s from network %s",
                    webhook_to_delete["id"],
                    network_id,
                )
                await self.delete_webhook(network_id, webhook_to_delete["id"])

    @handle_meraki_errors
    @async_timed_cache(timeout=300)
    async def get_group_policies(self, network_id: str) -> list[dict[str, Any]]:
        """
        Get group policies for a network.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            A list of group policies.

        """
        if self._api_client.dashboard is None:
            return []
        api = self._api_client.dashboard.networks
        policies = await api.getNetworkGroupPolicies(networkId=network_id)
        validated = validate_response(policies)
        if not isinstance(validated, list):
            _LOGGER.warning("get_group_policies did not return a list")
            return []
        return validated

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
        api = self._api_client.dashboard.camera
        history = await api.getNetworkCameraAnalyticsRecent(
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
        api = self._api_client.dashboard.networks
        policies = await api.getNetworkGroupPolicies(networkId=network_id)
        validated = validate_response(policies)
        if not isinstance(validated, list):
            _LOGGER.warning("get_network_group_policies did not return a list.")
            return []
        return validated

    @handle_meraki_errors
    async def provision_network_clients(
        self,
        network_id: str,
        clients: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Provision clients in a network."""
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.networks
        result = await api.provisionNetworkClients(
            networkId=network_id, clients=clients, **kwargs
        )
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning("provision_network_clients did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    @async_timed_cache(timeout=300)
    async def get_network_alerts_settings(self, network_id: str) -> dict[str, Any]:
        """
        Get alert settings for a network.

        Args:
        ----
            network_id: The ID of the network.

        Returns
        -------
            The alert settings for the network.

        """
        if self._api_client.dashboard is None:
            return {}
        api = self._api_client.dashboard.networks
        settings = await api.getNetworkAlertsSettings(networkId=network_id)
        validated = validate_response(settings)
        if not isinstance(validated, dict):
            _LOGGER.warning("get_network_alerts_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def update_network_alerts_settings(
        self,
        network_id: str,
        default_destinations: dict[str, Any] | None = None,
        alerts: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Update alert settings for a network.

        This configures which HTTP servers (webhooks) receive alerts
        and which alert types are enabled.

        Args:
        ----
            network_id: The ID of the network.
            default_destinations: Default destinations for alerts, including
                httpServerIds list.
            alerts: List of alert configurations with type and enabled status.

        Returns
        -------
            The updated alert settings.

        """
        if self._api_client.dashboard is None:
            return {}

        api = self._api_client.dashboard.networks
        kwargs: dict[str, Any] = {"networkId": network_id}

        if default_destinations is not None:
            kwargs["defaultDestinations"] = default_destinations
        if alerts is not None:
            kwargs["alerts"] = alerts

        result = await api.updateNetworkAlertsSettings(**kwargs)
        validated = validate_response(result)
        if not isinstance(validated, dict):
            _LOGGER.warning("update_network_alerts_settings did not return a dict.")
            return {}
        return validated

    @handle_meraki_errors
    async def subscribe_webhook_to_alerts(
        self,
        network_id: str,
        http_server_id: str,
        alert_types: list[str] | None = None,
    ) -> bool:
        """
        Subscribe a webhook HTTP server to receive alerts.

        Args:
        ----
            network_id: The ID of the network.
            http_server_id: The ID of the HTTP server (webhook).
            alert_types: Optional list of specific alert types to enable.
                If None, only configures the default destination.

        Returns
        -------
            True if successful, False otherwise.

        """
        try:
            # Get current alert settings
            current_settings = await self.get_network_alerts_settings(network_id)

            # Get current default destinations
            default_destinations = current_settings.get("defaultDestinations", {})
            current_http_servers = default_destinations.get("httpServerIds", [])

            # Add our HTTP server if not already present
            if http_server_id not in current_http_servers:
                current_http_servers.append(http_server_id)

            # Update default destinations to include our webhook
            new_default_destinations = {
                **default_destinations,
                "httpServerIds": current_http_servers,
            }

            # If specific alert types are requested, enable them
            alerts_config = None
            if alert_types:
                alerts_config = [
                    {"type": alert_type, "enabled": True} for alert_type in alert_types
                ]

            await self.update_network_alerts_settings(
                network_id,
                default_destinations=new_default_destinations,
                alerts=alerts_config,
            )

            _LOGGER.info(
                "Subscribed webhook %s to alerts for network %s",
                http_server_id,
                network_id,
            )
            return True
        except Exception as e:
            _LOGGER.error(
                "Failed to subscribe webhook to alerts for network %s: %s",
                network_id,
                e,
            )
            return False
