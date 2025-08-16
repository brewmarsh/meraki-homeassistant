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

        # API routes
        self.app.router.add_get("/api/config", self.handle_api_config)
        self.app.router.add_get("/api/networks", self.handle_api_networks)
        self.app.router.add_get("/api/networks/{network_id}", self.handle_api_network_detail)
        self.app.router.add_get("/api/clients", self.handle_api_clients)
        self.app.router.add_get("/api/clients/{client_mac}", self.handle_api_client_detail)

        # Static asset route
        self.app.router.add_static("/", static_dir, name="static")

        # Route for serving index.html for any other path, to support client-side routing
        self.app.router.add_route("*", "/{path:.*}", self.handle_static)

    async def handle_static(self, request: web.Request) -> web.FileResponse:
        """Serve index.html for SPA routing."""
        static_dir = os.path.join(os.path.dirname(__file__), "web_ui", "dist")
        return web.FileResponse(os.path.join(static_dir, "index.html"))

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

    async def handle_api_client_detail(self, request: web.Request) -> web.Response:
        """Handle requests for a single client's data."""
        client_mac = request.match_info.get("client_mac")
        if not self.coordinator.data or not client_mac:
            return web.json_response({"error": "Data not available"}, status=503)

        client = next((c for c in self.coordinator.data.get("clients", []) if c.get("mac") == client_mac), None)

        if client:
            return web.json_response(client)
        return web.json_response({"error": "Client not found"}, status=404)

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
