"""A self-hosted web server for the Meraki integration."""

import logging
import os
from typing import Union
from aiohttp import web
from homeassistant.core import HomeAssistant

from .core.coordinators.meraki_data_coordinator import MerakiDataCoordinator

_LOGGER = logging.getLogger(__name__)


class MerakiWebServer:
    """A class to manage the Meraki aiohttp web server."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: MerakiDataCoordinator,
        port: int,
    ):
        """Initialize the web server."""
        self.hass = hass
        self.coordinator = coordinator
        self.port = port
        self.runner = None
        self.app = web.Application()
        self._setup_routes()

    def _setup_routes(self):
        """Set up the routes for the web application."""
        static_dir = os.path.join(os.path.dirname(__file__), "www", "dist")
        assets_dir = os.path.join(static_dir, "assets")

        # API routes
        self.app.router.add_get("/api/config", self.handle_api_config)
        self.app.router.add_get("/api/networks", self.handle_api_networks)
        self.app.router.add_get(
            "/api/networks/{network_id}", self.handle_api_network_detail
        )

        # Settings endpoints
        self.app.router.add_get("/api/settings", self.handle_api_get_settings)
        self.app.router.add_post("/api/settings", self.handle_api_post_settings)

        # Parental Controls endpoints
        self.app.router.add_get(
            "/api/parental_controls/resources",
            self.handle_api_get_parental_controls_resources,
        )
        self.app.router.add_get("/api/clients", self.handle_api_get_clients)
        self.app.router.add_get(
            "/api/networks/{network_id}/appliance/contentFiltering",
            self.handle_api_get_content_filtering,
        )
        self.app.router.add_put(
            "/api/networks/{network_id}/appliance/contentFiltering",
            self.handle_api_put_content_filtering,
        )
        self.app.router.add_get(
            "/api/contentFiltering/categories",
            self.handle_api_get_content_filtering_categories,
        )
        self.app.router.add_get(
            "/api/networks/{network_id}/ssids/{ssid_number}/contentFiltering",
            self.handle_api_get_ssid_content_filtering,
        )
        self.app.router.add_put(
            "/api/networks/{network_id}/ssids/{ssid_number}/contentFiltering",
            self.handle_api_put_ssid_content_filtering,
        )
        self.app.router.add_get(
            "/api/networks/{network_id}/appliance/firewall/l7FirewallRules",
            self.handle_api_get_l7_firewall_rules,
        )
        self.app.router.add_put(
            "/api/networks/{network_id}/appliance/firewall/l7FirewallRules",
            self.handle_api_put_l7_firewall_rules,
        )

        # Static asset route (for JS, CSS, etc.)
        self.app.router.add_static("/assets", assets_dir, name="assets")

        # Serve index.html for the root and any other non-API, non-asset path
        self.app.router.add_get("/{path:.*}", self.handle_spa)
        self.app.router.add_get("/", self.handle_spa)

    async def handle_spa(
        self, request: web.Request
    ) -> Union[web.FileResponse, web.Response]:
        """Serve the single-page application's entry point (index.html)."""
        static_dir = os.path.join(os.path.dirname(__file__), "www", "dist")
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r") as f:
                content = f.read()

            ha_url = str(self.hass.config.api.base_url)
            content = content.replace("__HA_URL__", ha_url)

            config_entry_id = self.coordinator.config_entry.entry_id
            content = content.replace("__CONFIG_ENTRY_ID__", config_entry_id)

            return web.Response(text=content, content_type="text/html")
        return web.Response(
            text="Web UI files not found. Have you built the frontend?", status=404
        )

    async def handle_api_config(self, request: web.Request) -> web.Response:
        """Handle requests for the integration's configuration."""
        # Placeholder
        return web.json_response(
            {"organization_id": self.coordinator.api_client.org_id}
        )

    async def handle_api_networks(self, request: web.Request) -> web.Response:
        """Handle requests for network data."""
        # Placeholder
        if not self.coordinator.data:
            return web.json_response({"error": "Data not available"}, status=503)
        return web.json_response(self.coordinator.data.get("networks", []))

    async def handle_api_get_settings(self, request: web.Request) -> web.Response:
        """Handle requests to get the current integration settings."""
        return web.json_response(dict(self.coordinator.config_entry.options))

    async def handle_api_post_settings(self, request: web.Request) -> web.Response:
        """Handle requests to update the integration settings."""
        try:
            new_options = await request.json()
            # It's good practice to merge with existing options, though client should send all
            updated_options = {**self.coordinator.config_entry.options, **new_options}
            self.hass.config_entries.async_update_entry(
                self.coordinator.config_entry, options=updated_options
            )
            return web.json_response({"status": "success"}, status=200)
        except Exception as e:
            _LOGGER.error("Failed to update settings: %s", e, exc_info=True)
            return web.json_response({"error": str(e)}, status=500)

    async def handle_api_network_detail(self, request: web.Request) -> web.Response:
        """Handle requests for a single network's data."""
        network_id = request.match_info.get("network_id")
        if not self.coordinator.data or not network_id:
            return web.json_response({"error": "Data not available"}, status=503)

        network = next(
            (
                n
                for n in self.coordinator.data.get("networks", [])
                if n.get("id") == network_id
            ),
            None,
        )

        if network:
            return web.json_response(network)
        return web.json_response({"error": "Network not found"}, status=404)

    async def handle_api_get_parental_controls_resources(
        self, request: web.Request
    ) -> web.Response:
        """Get a list of all networks and SSIDs that support content filtering."""
        resources = []
        domain = self.coordinator.config_entry.domain
        entry_data = self.hass.data[domain][self.coordinator.config_entry.entry_id]

        # Add network-level resources
        if "network_content_filtering_coordinators" in entry_data:
            for network_id, coordinator in entry_data[
                "network_content_filtering_coordinators"
            ].items():
                network_info = self.coordinator.get_network(network_id)
                if network_info:
                    resources.append(
                        {
                            "type": "network",
                            "network_id": network_id,
                            "name": network_info.get("name", "Unknown Network"),
                        }
                    )

        # Add SSID-level resources
        if "ssid_content_filtering_coordinators" in entry_data:
            for coordinator_key, coordinator in entry_data[
                "ssid_content_filtering_coordinators"
            ].items():
                network_id = coordinator.network_id
                ssid_number = coordinator.ssid_number
                ssid_info = self.coordinator.get_ssid(network_id, ssid_number)
                if ssid_info:
                    resources.append(
                        {
                            "type": "ssid",
                            "network_id": network_id,
                            "ssid_number": ssid_number,
                            "name": ssid_info.get("name", f"SSID {ssid_number}"),
                        }
                    )

        return web.json_response(resources)

    async def handle_api_get_clients(self, request: web.Request) -> web.Response:
        """Handle requests for client data."""
        if not self.coordinator.data or "clients" not in self.coordinator.data:
            return web.json_response({"error": "Data not available"}, status=503)
        return web.json_response(self.coordinator.data.get("clients", []))

    async def handle_api_get_content_filtering(
        self, request: web.Request
    ) -> web.Response:
        """Handle requests for content filtering settings."""
        network_id = request.match_info.get("network_id")
        try:
            settings = await self.coordinator.api_client.appliance.get_network_appliance_content_filtering(
                networkId=network_id
            )
            return web.json_response(settings)
        except Exception as e:
            _LOGGER.error(
                "Failed to get content filtering settings: %s", e, exc_info=True
            )
            return web.json_response({"error": str(e)}, status=500)

    async def handle_api_put_content_filtering(
        self, request: web.Request
    ) -> web.Response:
        """Handle requests to update content filtering settings."""
        network_id = request.match_info.get("network_id")
        try:
            new_settings = await request.json()
            await self.coordinator.api_client.appliance.update_network_appliance_content_filtering(
                networkId=network_id, **new_settings
            )
            return web.json_response({"status": "success"}, status=200)
        except Exception as e:
            _LOGGER.error(
                "Failed to update content filtering settings: %s", e, exc_info=True
            )
            return web.json_response({"error": str(e)}, status=500)

    async def handle_api_get_l7_firewall_rules(
        self, request: web.Request
    ) -> web.Response:
        """Handle requests for L7 firewall rules."""
        network_id = request.match_info.get("network_id")
        try:
            rules = await self.coordinator.api_client.appliance.get_network_appliance_firewall_l7_firewall_rules(
                networkId=network_id
            )
            return web.json_response(rules)
        except Exception as e:
            _LOGGER.error("Failed to get L7 firewall rules: %s", e, exc_info=True)
            return web.json_response({"error": str(e)}, status=500)

    async def handle_api_put_l7_firewall_rules(
        self, request: web.Request
    ) -> web.Response:
        """Handle requests to update L7 firewall rules."""
        network_id = request.match_info.get("network_id")
        try:
            new_rules = await request.json()
            await self.coordinator.api_client.appliance.update_network_appliance_firewall_l7_firewall_rules(
                networkId=network_id, **new_rules
            )
            return web.json_response({"status": "success"}, status=200)
        except Exception as e:
            _LOGGER.error("Failed to update L7 firewall rules: %s", e, exc_info=True)
            return web.json_response({"error": str(e)}, status=500)

    async def start(self):
        """Start the web server."""
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, "0.0.0.0", self.port)
        try:
            await site.start()
            _LOGGER.info("Meraki web UI server started at http://0.0.0.0:%d", self.port)
        except Exception as e:
            _LOGGER.error("Failed to start Meraki web UI server: %s", e)

    async def stop(self):
        """Stop the web server."""
        if self.runner:
            await self.runner.cleanup()
            _LOGGER.info("Meraki web UI server stopped.")

    async def handle_api_get_ssid_content_filtering(
        self, request: web.Request
    ) -> web.Response:
        """Handle requests for SSID-specific content filtering settings."""
        network_id = request.match_info.get("network_id")
        ssid_number = request.match_info.get("ssid_number")
        coordinator_key = f"{network_id}_{ssid_number}"

        domain = self.coordinator.config_entry.domain
        entry_data = self.hass.data[domain][self.coordinator.config_entry.entry_id]
        coordinator = entry_data.get("ssid_content_filtering_coordinators", {}).get(
            coordinator_key
        )

        if not coordinator or not coordinator.data:
            return web.json_response(
                {"error": "SSID content filtering data not available"}, status=404
            )

        return web.json_response(coordinator.data.get("contentFiltering", {}))

    async def handle_api_put_ssid_content_filtering(
        self, request: web.Request
    ) -> web.Response:
        """Handle requests to update SSID-specific content filtering settings."""
        network_id = request.match_info.get("network_id")
        ssid_number = request.match_info.get("ssid_number")
        coordinator_key = f"{network_id}_{ssid_number}"

        domain = self.coordinator.config_entry.domain
        entry_data = self.hass.data[domain][self.coordinator.config_entry.entry_id]
        coordinator = entry_data.get("ssid_content_filtering_coordinators", {}).get(
            coordinator_key
        )

        if not coordinator:
            return web.json_response(
                {"error": "SSID coordinator not found"}, status=404
            )

        try:
            new_settings = await request.json()
            await coordinator.async_update_content_filtering(**new_settings)
            return web.json_response({"status": "success"}, status=200)
        except Exception as e:
            _LOGGER.error(
                "Failed to update SSID content filtering settings: %s", e, exc_info=True
            )
            return web.json_response({"error": str(e)}, status=500)

    async def handle_api_get_content_filtering_categories(
        self, request: web.Request
    ) -> web.Response:
        """Return the list of Meraki content filtering categories."""
        # This data is static, so we can just return it from the const file.
        # In a real app, this might come from the API if it can change.
        from .const import MERAKI_CONTENT_FILTERING_CATEGORIES

        return web.json_response(MERAKI_CONTENT_FILTERING_CATEGORIES)
