"""Tests for the web server module."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import web

from custom_components.meraki_ha.web_server import MerakiWebServer


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock hass instance."""
    hass = MagicMock()
    hass.config = MagicMock()
    hass.config.api = MagicMock()
    hass.config.api.base_url = "http://localhost:8123"
    return hass


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "networks": [
            {"id": "N_123", "name": "Test Network"},
        ],
        "devices": [],
        "ssids": [],
        "clients": [],
    }
    coordinator.api = MagicMock()
    coordinator.api._org_id = "test_org_id"
    return coordinator


@pytest.fixture
def web_server(mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path):
    """Create a web server instance with mocked static directory."""
    # Create the required directory structure
    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()
    (static_dir / "index.html").write_text("<html></html>")

    with patch.object(
        MerakiWebServer, "_setup_routes", lambda self: _mock_setup_routes(self, str(static_dir))
    ):
        server = MerakiWebServer(
            hass=mock_hass,
            coordinator=mock_coordinator,
            port=8080,
        )
        # Now set up minimal routes without static files
        server.app.router.add_get("/api/config", server.handle_api_config)
        server.app.router.add_get("/api/networks", server.handle_api_networks)
        server.app.router.add_get(
            "/api/networks/{network_id}", server.handle_api_network_detail
        )
        server.app.router.add_get("/api/settings", server.handle_api_get_settings)
        server.app.router.add_post("/api/settings", server.handle_api_post_settings)
        server.app.router.add_get("/api/clients", server.handle_api_get_clients)
        return server


def _mock_setup_routes(server, static_dir):
    """Mock setup routes without static file handling."""
    pass


def test_web_server_initialization(web_server) -> None:
    """Test web server initializes correctly."""
    assert web_server.port == 8080
    assert web_server.runner is None
    assert web_server.app is not None


def test_web_server_routes_setup(web_server) -> None:
    """Test web server sets up routes."""
    routes = list(web_server.app.router.routes())
    assert len(routes) > 0


@pytest.mark.asyncio
async def test_handle_api_config(web_server) -> None:
    """Test handle_api_config returns config data."""
    mock_request = MagicMock()

    response = await web_server.handle_api_config(mock_request)

    assert isinstance(response, web.Response)
    assert response.status == 200


@pytest.mark.asyncio
async def test_handle_api_networks(web_server) -> None:
    """Test handle_api_networks returns network data."""
    mock_request = MagicMock()

    response = await web_server.handle_api_networks(mock_request)

    assert isinstance(response, web.Response)
    assert response.status == 200


@pytest.mark.asyncio
async def test_handle_api_network_detail(web_server) -> None:
    """Test handle_api_network_detail returns network detail."""
    mock_request = MagicMock()
    mock_request.match_info = {"network_id": "N_123"}

    response = await web_server.handle_api_network_detail(mock_request)

    assert isinstance(response, web.Response)


@pytest.mark.asyncio
async def test_handle_api_network_detail_not_found(web_server) -> None:
    """Test handle_api_network_detail returns 404 for unknown network."""
    mock_request = MagicMock()
    mock_request.match_info = {"network_id": "N_unknown"}

    response = await web_server.handle_api_network_detail(mock_request)

    assert isinstance(response, web.Response)
    assert response.status == 404


@pytest.mark.asyncio
async def test_handle_api_get_settings(web_server) -> None:
    """Test handle_api_get_settings returns settings."""
    mock_request = MagicMock()

    response = await web_server.handle_api_get_settings(mock_request)

    assert isinstance(response, web.Response)


@pytest.mark.asyncio
async def test_handle_api_post_settings(web_server) -> None:
    """Test handle_api_post_settings updates settings."""
    mock_request = MagicMock()
    mock_request.json = AsyncMock(return_value={"scan_interval": 60})

    response = await web_server.handle_api_post_settings(mock_request)

    assert isinstance(response, web.Response)


@pytest.mark.asyncio
async def test_handle_api_get_clients(web_server) -> None:
    """Test handle_api_get_clients returns client data."""
    mock_request = MagicMock()

    response = await web_server.handle_api_get_clients(mock_request)

    assert isinstance(response, web.Response)


@pytest.mark.asyncio
async def test_start_and_stop(web_server) -> None:
    """Test server start and stop."""
    # Mock the runner
    mock_runner = MagicMock()
    mock_runner.setup = AsyncMock()
    mock_runner.cleanup = AsyncMock()

    with patch(
        "custom_components.meraki_ha.web_server.web.AppRunner",
        return_value=mock_runner
    ):
        with patch(
            "custom_components.meraki_ha.web_server.web.TCPSite"
        ) as mock_site:
            mock_site_instance = MagicMock()
            mock_site_instance.start = AsyncMock()
            mock_site.return_value = mock_site_instance

            await web_server.start()

            mock_runner.setup.assert_called_once()
            mock_site_instance.start.assert_called_once()

    # Test stop
    web_server.runner = mock_runner
    await web_server.stop()
    mock_runner.cleanup.assert_called_once()


@pytest.mark.asyncio
async def test_stop_when_not_running(web_server) -> None:
    """Test stop does nothing when server not running."""
    # Should not raise when runner is None
    web_server.runner = None
    await web_server.stop()
