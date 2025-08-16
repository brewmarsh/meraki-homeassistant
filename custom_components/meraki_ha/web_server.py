"""A self-hosted web server for the Meraki integration."""

import logging
import os
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
        static_dir = os.path.join(os.path.dirname(__file__), "web_ui", "dist")
        assets_dir = os.path.join(static_dir, "assets")

        # API routes
        self.app.router.add_get("/api/config", self.handle_api_config)
        self.app.router.add_get("/api/networks", self.handle_api_networks)
        self.app.router.add_get("/api/networks/{network_id}", self.handle_api_network_detail)
        self.app.router.add_get("/api/clients", self.handle_api_clients)
        self.app.router.add_get("/api/clients/{client_mac}", self.handle_api_client_detail)

        # Static asset route (for JS, CSS, etc.)
        self.app.router.add_static("/assets", assets_dir, name="assets")

        # Serve index.html for the root and any other non-API, non-asset path
        self.app.router.add_get("/{path:.*}", self.handle_spa)
        self.app.router.add_get("/", self.handle_spa)


    async def handle_spa(self, request: web.Request) -> web.FileResponse:
        """Serve the single-page application's entry point (index.html)."""
        static_dir = os.path.join(os.path.dirname(__file__), "web_ui", "dist")
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return web.FileResponse(index_path)
        return web.Response(text="Web UI files not found. Have you built the frontend?", status=404)

    async def handle_api_config(self, request: web.Request) -> web.Response:
        """Handle requests for the integration's configuration."""
        # Placeholder
        return web.json_response({"organization_id": self.coordinator.api_client.org_id})

    async def handle_api_networks(self, request: web.Request) -> web.Response:
        """Handle requests for network data."""
        # Placeholder
        if not self.coordinator.data:
            return web.json_response({"error": "Data not available"}, status=503)
        return web.json_response(self.coordinator.data.get("networks", []))

    async def handle_api_client_detail(self, request: web.Request) -> web.Response:
        """Handle requests for a single client's data."""
        client_mac = request.match_info.get("client_mac")
        if not self.coordinator.data or not client_mac:
            return web.json_response({"error": "Data not available"}, status=503)

        client = next((c for c in self.coordinator.data.get("clients", []) if c.get("mac") == client_mac), None)

        if client:
            return web.json_response(client)
        return web.json_response({"error": "Client not found"}, status=404)

    async def handle_api_clients(self, request: web.Request) -> web.Response:
        """Handle requests for client data."""
        # Placeholder
        if not self.coordinator.data:
            return web.json_response({"error": "Data not available"}, status=503)
        return web.json_response(self.coordinator.data.get("clients", []))

    async def handle_api_network_detail(self, request: web.Request) -> web.Response:
        """Handle requests for a single network's data."""
        network_id = request.match_info.get("network_id")
        if not self.coordinator.data or not network_id:
            return web.json_response({"error": "Data not available"}, status=503)

        network = next((n for n in self.coordinator.data.get("networks", []) if n.get("id") == network_id), None)

        if network:
            return web.json_response(network)
        return web.json_response({"error": "Network not found"}, status=404)

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
