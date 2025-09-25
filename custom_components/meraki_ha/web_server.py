"""
This module implements the aiohttp web server for the Meraki Home Assistant integration.
"""
import logging
from pathlib import Path
from aiohttp import web
from homeassistant.core import HomeAssistant
from .coordinator import MerakiDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class WebServer:
    """A class to manage the aiohttp web server."""

    def __init__(self, hass: HomeAssistant, coordinator: MerakiDataUpdateCoordinator, port: int):
        """Initialize the web server."""
        self.hass = hass
        self.coordinator = coordinator
        self.port = port
        self.runner = None
        self.static_dir = Path(__file__).parent / "www" / "dist"

    async def start(self):
        """Start the web server."""
        app = web.Application()
        app.router.add_get("/", self.handle_index)
        app.router.add_get("/api/config", self.get_config)
        app.router.add_get("/api/networks", self.get_networks)
        app.router.add_get("/api/clients", self.get_clients)
        app.router.add_get("/api/networks/{network_id}", self.get_network)
        app.router.add_get("/api/clients/{client_mac}", self.get_client)
        app.router.add_static("/", self.static_dir, name="static")

        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, "0.0.0.0", self.port)
        await site.start()
        _LOGGER.info(f"Meraki web UI started on http://0.0.0.0:{self.port}")

    async def stop(self):
        """Stop the web server."""
        if self.runner:
            await self.runner.cleanup()
            _LOGGER.info("Meraki web UI stopped.")

    async def handle_index(self, request):
        """Serve the index.html file."""
        return web.FileResponse(self.static_dir / 'index.html')

    async def get_config(self, request):
        """Handle GET /api/config."""
        return web.json_response(self.coordinator.data)

    async def get_networks(self, request):
        """Handle GET /api/networks."""
        return web.json_response(self.coordinator.data.get("networks", []))

    async def get_clients(self, request):
        """Handle GET /api/clients."""
        return web.json_response(self.coordinator.data.get("clients", []))

    async def get_network(self, request):
        """Handle GET /api/networks/{id}."""
        network_id = request.match_info["network_id"]
        networks = self.coordinator.data.get("networks", [])
        network = next((n for n in networks if n["id"] == network_id), None)
        if network:
            return web.json_response(network)
        return web.Response(status=404, text="Network not found")

    async def get_client(self, request):
        """Handle GET /api/clients/{mac}."""
        client_mac = request.match_info["client_mac"]
        clients = self.coordinator.data.get("clients", [])
        client = next((c for c in clients if c["mac"] == client_mac), None)
        if client:
            return web.json_response(client)
        return web.Response(status=404, text="Client not found")