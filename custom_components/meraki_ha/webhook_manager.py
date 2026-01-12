"""Manages Meraki webhook registration and unregistration."""

from __future__ import annotations

import secrets
from datetime import datetime
from typing import TYPE_CHECKING, Any

from meraki.exceptions import AsyncAPIError

from .const import (
    CONF_ENABLED_NETWORKS,
    CONF_WEBHOOK_ALERT_TYPES,
    CONF_WEBHOOK_AUTO_REGISTER,
    CONF_WEBHOOK_EXTERNAL_URL,
    CONF_WEBHOOK_SHARED_SECRET,
    DEFAULT_WEBHOOK_ALERT_TYPES,
    DEFAULT_WEBHOOK_AUTO_REGISTER,
)
from .core.errors import MerakiConnectionError
from .helpers.logging_helper import MerakiLoggers
from .webhook import get_webhook_url

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from .core.api import MerakiAPIClient


_LOGGER = MerakiLoggers.ALERTS

# Mapping of user-friendly alert type names to Meraki API alert type identifiers
ALERT_TYPE_MAPPING: dict[str, str] = {
    "APs went down": "gatewayDown",
    "APs came up": "gatewayUp",
    "Switches went down": "switchDown",
    "Switches came up": "switchUp",
    "Gateways went down": "applianceDown",
    "Gateways came up": "applianceUp",
    "Cameras went down": "cameraDown",
    "Cameras came up": "cameraUp",
    "Sensors went offline": "sensorDown",
    "Sensors came online": "sensorUp",
    "Device rebooted": "deviceRebooted",
    "Settings changed": "settingsChanged",
    "SSID settings changed": "ssidSettingsChanged",
    "VLAN settings changed": "vlanSettingsChanged",
    "Firewall rule changed": "firewallRuleChanged",
    "Client connectivity changed": "clientConnectivityChange",
    "New client connected": "newClientConnected",
    "Client blocked": "clientBlocked",
    "Rogue AP detected": "rogueAp",
    "Intrusion detected": "intrusionDetected",
    "Malware detected": "malwareDetected",
    "Temperature threshold exceeded": "sensorTemperatureThreshold",
    "Humidity threshold exceeded": "sensorHumidityThreshold",
    "Water detected": "sensorWaterDetection",
    "Door opened/closed": "sensorDoorChange",
    "Power outage detected": "sensorPowerOutage",
}


class WebhookManager:
    """Manages the lifecycle of Meraki webhooks."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: MerakiAPIClient,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the WebhookManager.

        Args:
        ----
            hass: The Home Assistant instance.
            api_client: The Meraki API client.
            config_entry: The config entry for the integration.

        """
        self.hass = hass
        self.api = api_client
        self.entry = config_entry
        self._http_server_ids: dict[str, str] = {}  # network_id -> http_server_id
        self._last_webhook_received: datetime | None = None
        self._webhook_count: int = 0
        self._registration_errors: list[str] = []

    def _get_enabled_networks(self) -> list[str]:
        """Get the list of enabled network IDs from config entry."""
        enabled = self.entry.options.get(CONF_ENABLED_NETWORKS, [])
        if isinstance(enabled, list):
            return enabled
        return []

    def _get_alert_types(self) -> list[str]:
        """Get the list of alert types to subscribe to from config entry."""
        alert_types = self.entry.options.get(
            CONF_WEBHOOK_ALERT_TYPES, DEFAULT_WEBHOOK_ALERT_TYPES
        )
        if isinstance(alert_types, list):
            return alert_types
        return []

    def _get_secret(self) -> str:
        """Get or generate the webhook shared secret."""
        secret = self.entry.options.get(CONF_WEBHOOK_SHARED_SECRET)
        if not secret:
            # Check if stored in entry data
            secret = self.entry.data.get("secret")
        if not secret:
            # Generate a new secret
            secret = secrets.token_hex(16)
        return secret

    @property
    def is_auto_register_enabled(self) -> bool:
        """Check if auto-registration is enabled."""
        return self.entry.options.get(
            CONF_WEBHOOK_AUTO_REGISTER, DEFAULT_WEBHOOK_AUTO_REGISTER
        )

    @property
    def webhook_status(self) -> dict[str, Any]:
        """Get the current webhook status for display in UI."""
        if self._registration_errors:
            return {
                "status": "error",
                "message": f"⚠️ Registration errors: {len(self._registration_errors)}",
                "errors": self._registration_errors,
            }

        if not self._http_server_ids:
            return {
                "status": "not_registered",
                "message": "❌ Webhooks not registered",
            }

        if self._last_webhook_received:
            age_seconds = (datetime.now() - self._last_webhook_received).total_seconds()
            if age_seconds < 900:  # 15 minutes
                return {
                    "status": "active",
                    "message": f"✅ Webhooks active ({self._webhook_count} received)",
                    "last_received": self._last_webhook_received.isoformat(),
                }
            else:
                minutes = int(age_seconds / 60)
                return {
                    "status": "stale",
                    "message": f"⚠️ No webhooks received in {minutes} minutes",
                    "last_received": self._last_webhook_received.isoformat(),
                }

        return {
            "status": "registered",
            "message": f"✅ Registered in {len(self._http_server_ids)} networks",
        }

    def mark_webhook_received(self) -> None:
        """Mark that a webhook was received (for status tracking)."""
        self._last_webhook_received = datetime.now()
        self._webhook_count += 1

    async def async_register_webhooks(self) -> bool:
        """Register webhooks with the Meraki Dashboard.

        This performs two main actions:
        1. Creates an HTTP server in the Meraki Dashboard to receive webhooks.
        2. Subscribes to the selected alert types and points them to the new server.

        Returns
        -------
            True if registration was successful, False otherwise.

        """
        if not self.is_auto_register_enabled:
            _LOGGER.info("Webhook auto-registration is disabled.")
            return True

        custom_url = self.entry.options.get(CONF_WEBHOOK_EXTERNAL_URL)
        try:
            webhook_url = get_webhook_url(
                self.hass, self.entry.entry_id, custom_url or None
            )
        except MerakiConnectionError as e:
            _LOGGER.error("Cannot determine webhook URL: %s", e)
            self._registration_errors.append(str(e))
            return False

        secret = self._get_secret()
        enabled_networks = self._get_enabled_networks()
        alert_types = self._get_alert_types()

        if not enabled_networks:
            _LOGGER.warning(
                "No networks enabled for webhooks. "
                "Please enable networks in integration options."
            )
            return True  # Not an error, just nothing to do

        if not alert_types:
            _LOGGER.info(
                "No alert types selected for webhooks. "
                "Webhook server will be created but no alerts subscribed."
            )

        self._registration_errors = []
        success_count = 0

        for network_id in enabled_networks:
            try:
                # Step 1: Create or update HTTP Server
                http_server_id = await self._ensure_http_server(
                    network_id, webhook_url, secret
                )
                if not http_server_id:
                    continue

                self._http_server_ids[network_id] = http_server_id

                # Step 2: Subscribe to alerts if any are configured
                if alert_types:
                    await self._subscribe_to_alerts(
                        network_id, http_server_id, alert_types
                    )

                success_count += 1
                _LOGGER.info(
                    "Successfully registered webhooks for network %s", network_id
                )

            except AsyncAPIError as e:
                error_str = str(e)
                if "403" in error_str or "Forbidden" in error_str:
                    msg = (
                        f"Read-only API key: Cannot auto-register webhooks for "
                        f"network {network_id}. Please configure manually."
                    )
                    _LOGGER.warning(msg)
                    self._registration_errors.append(msg)
                else:
                    msg = f"Failed to register webhooks for network {network_id}: {e}"
                    _LOGGER.error(msg)
                    self._registration_errors.append(msg)
            except Exception as e:
                msg = (
                    f"Unexpected error during webhook registration "
                    f"for {network_id}: {e}"
                )
                _LOGGER.error(msg)
                self._registration_errors.append(msg)

        _LOGGER.info(
            "Webhook registration complete: %d/%d networks successful",
            success_count,
            len(enabled_networks),
        )
        return success_count > 0 or not enabled_networks

    async def _ensure_http_server(
        self, network_id: str, webhook_url: str, secret: str
    ) -> str | None:
        """Ensure an HTTP server exists for the webhook, creating if needed."""
        webhook_name = f"Home Assistant - {self.entry.entry_id[:8]}"

        # Check for existing webhook with same name
        existing = await self.api.network.find_webhook_by_name(network_id, webhook_name)
        if existing:
            existing_id = existing.get("id")
            if existing.get("url") == webhook_url:
                _LOGGER.debug(
                    "Reusing existing webhook %s for network %s",
                    existing_id,
                    network_id,
                )
                return existing_id
            else:
                # URL changed, delete and recreate
                await self.api.network.delete_webhook(network_id, existing_id)
                _LOGGER.debug(
                    "Deleted outdated webhook for network %s (URL changed)",
                    network_id,
                )

        # Create new HTTP server
        if self.api.dashboard is None:
            return None

        result = await self.api.dashboard.networks.createNetworkWebhooksHttpServer(
            networkId=network_id,
            url=webhook_url,
            sharedSecret=secret,
            name=webhook_name,
        )
        http_server_id = result.get("id") if result else None
        if http_server_id:
            _LOGGER.info(
                "Created webhook HTTP server %s for network %s",
                http_server_id,
                network_id,
            )
        return http_server_id

    async def _subscribe_to_alerts(
        self,
        network_id: str,
        http_server_id: str,
        alert_types: list[str],
    ) -> None:
        """Subscribe the HTTP server to receive specified alert types."""
        # Convert user-friendly names to API identifiers
        api_alerts = []
        for alert_type in alert_types:
            api_type = ALERT_TYPE_MAPPING.get(alert_type)
            if api_type:
                api_alerts.append({"type": api_type, "enabled": True})
            else:
                _LOGGER.warning("Unknown alert type: %s", alert_type)

        if not api_alerts:
            return

        # Get current settings to preserve other destinations
        current = await self.api.network.get_network_alerts_settings(network_id)
        current_destinations = current.get("defaultDestinations", {})
        current_http_servers = current_destinations.get("httpServerIds", [])

        # Add our server if not present
        if http_server_id not in current_http_servers:
            current_http_servers.append(http_server_id)

        await self.api.network.update_network_alerts_settings(
            network_id,
            default_destinations={
                **current_destinations,
                "httpServerIds": current_http_servers,
            },
            alerts=api_alerts,
        )
        _LOGGER.debug(
            "Subscribed to %d alert types for network %s",
            len(api_alerts),
            network_id,
        )

    async def async_unregister_webhooks(self) -> None:
        """Unregister and clean up webhooks from the Meraki Dashboard."""
        if not self._http_server_ids:
            _LOGGER.debug("No HTTP servers registered, skipping unregistration.")
            return

        for network_id, http_server_id in self._http_server_ids.items():
            try:
                await self.api.network.delete_webhook(network_id, http_server_id)
                _LOGGER.info(
                    "Successfully unregistered webhook for network %s", network_id
                )
            except Exception as e:
                _LOGGER.error(
                    "Failed to unregister webhook for network %s: %s", network_id, e
                )

        self._http_server_ids = {}

    def _get_ha_webhook_url(self) -> str | None:
        """Get the webhook URL for Home Assistant."""
        custom_url = self.entry.options.get(CONF_WEBHOOK_EXTERNAL_URL)
        try:
            return get_webhook_url(self.hass, self.entry.entry_id, custom_url or None)
        except Exception as e:
            _LOGGER.error("Could not determine Home Assistant webhook URL: %s", e)
            return None

    def get_manual_setup_instructions(self) -> dict[str, Any]:
        """Get manual setup instructions for read-only API key scenario."""
        webhook_url = self._get_ha_webhook_url()
        secret = self._get_secret()
        alert_types = self._get_alert_types()

        return {
            "webhook_url": webhook_url or "Unable to determine URL",
            "shared_secret": secret,
            "alert_types": alert_types,
            "instructions": [
                "1. Go to Network-wide > Alerts > HTTP Servers in Meraki Dashboard",
                "2. Click 'Add an HTTP server'",
                "3. Name: Home Assistant",
                f"4. URL: {webhook_url}",
                f"5. Shared Secret: {secret}",
                "6. Go to Network-wide > Alerts > Alert settings",
                "7. Enable the alerts you want and assign to 'Home Assistant' server",
            ],
        }
