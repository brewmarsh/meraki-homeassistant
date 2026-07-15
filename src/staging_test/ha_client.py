"""Home Assistant WebSocket client for staging audits."""

import logging
from typing import Any

import aiohttp

_LOGGER = logging.getLogger(__name__)


class MerakiHaClient:
    """Client for Home Assistant WebSocket API."""

    def __init__(self, ha_url: str, ha_token: str) -> None:
        self.ha_url = ha_url
        self.ha_token = ha_token
        self.ws = None
        self.session = None

    async def connect(self) -> None:
        """Connect to Home Assistant."""
        self.session = aiohttp.ClientSession()
        # Convert http(s) to ws(s)
        ws_url = self.ha_url.replace("http", "ws") + "/api/websocket"
        self.ws = await self.session.ws_connect(ws_url)
        _LOGGER.debug("Connected to %s", ws_url)

        # Authenticate
        await self.ws.send_json({"type": "auth", "access_token": self.ha_token})
        auth_response = await self.ws.receive_json()
        if auth_response.get("type") != "auth_ok":
            raise Exception(f"Authentication failed: {auth_response}")
        _LOGGER.info("Authenticated successfully")

    async def get_states(self) -> list[dict[str, Any]]:
        """Fetch states via WebSocket."""
        await self.ws.send_json({"type": "get_states", "id": 1})
        response = await self.ws.receive_json()
        return response.get("result", [])

    async def close(self) -> None:
        """Close connection."""
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
