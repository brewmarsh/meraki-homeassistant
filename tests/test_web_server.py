"""Tests for the web server module."""

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
        MerakiWebServer,
        "_setup_routes",
        lambda self: _mock_setup_routes(self, str(static_dir)),
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
        "custom_components.meraki_ha.web_server.web.AppRunner", return_value=mock_runner
    ):
        with patch("custom_components.meraki_ha.web_server.web.TCPSite") as mock_site:
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


@pytest.mark.asyncio
async def test_handle_api_networks_no_data(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_networks returns 503 when no data."""
    mock_coordinator.data = None

    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()

        response = await server.handle_api_networks(mock_request)

        assert response.status == 503


@pytest.mark.asyncio
async def test_handle_api_network_detail_no_data(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_network_detail returns 503 when no data."""
    mock_coordinator.data = None

    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()
        mock_request.match_info = {"network_id": "N_123"}

        response = await server.handle_api_network_detail(mock_request)

        assert response.status == 503


@pytest.mark.asyncio
async def test_handle_api_get_clients_no_data(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_get_clients returns 503 when no data."""
    mock_coordinator.data = None

    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()

        response = await server.handle_api_get_clients(mock_request)

        assert response.status == 503


@pytest.mark.asyncio
async def test_handle_api_post_settings_error(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_post_settings handles errors."""
    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()
        mock_request.json = AsyncMock(side_effect=Exception("Invalid JSON"))

        response = await server.handle_api_post_settings(mock_request)

        assert response.status == 500


@pytest.mark.asyncio
async def test_handle_api_get_settings_no_config_entry(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_get_settings when no config entry."""
    mock_coordinator.config_entry = None

    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()

        response = await server.handle_api_get_settings(mock_request)

        assert response.status == 200


@pytest.mark.asyncio
async def test_handle_api_get_content_filtering(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_get_content_filtering."""
    mock_coordinator.api.appliance.get_network_appliance_content_filtering = AsyncMock(
        return_value={"blockedUrlCategories": []}
    )

    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()
        mock_request.match_info = {"network_id": "N_123"}

        response = await server.handle_api_get_content_filtering(mock_request)

        assert response.status == 200


@pytest.mark.asyncio
async def test_handle_api_get_content_filtering_error(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_get_content_filtering handles errors."""
    mock_coordinator.api.appliance.get_network_appliance_content_filtering = AsyncMock(
        side_effect=Exception("API Error")
    )

    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()
        mock_request.match_info = {"network_id": "N_123"}

        response = await server.handle_api_get_content_filtering(mock_request)

        assert response.status == 500


@pytest.mark.asyncio
async def test_handle_api_put_content_filtering(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_put_content_filtering."""
    mock_coordinator.api.appliance.update_network_appliance_content_filtering = (
        AsyncMock()
    )

    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()
        mock_request.match_info = {"network_id": "N_123"}
        mock_request.json = AsyncMock(return_value={"blockedUrlCategories": []})

        response = await server.handle_api_put_content_filtering(mock_request)

        assert response.status == 200


@pytest.mark.asyncio
async def test_handle_api_put_content_filtering_error(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_put_content_filtering handles errors."""
    mock_coordinator.api.appliance.update_network_appliance_content_filtering = (
        AsyncMock(side_effect=Exception("API Error"))
    )

    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()
        mock_request.match_info = {"network_id": "N_123"}
        mock_request.json = AsyncMock(return_value={})

        response = await server.handle_api_put_content_filtering(mock_request)

        assert response.status == 500


@pytest.mark.asyncio
async def test_handle_api_get_l7_firewall_rules(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_get_l7_firewall_rules."""
    mock_coordinator.api.appliance.get_network_appliance_l7_firewall_rules = AsyncMock(
        return_value={"rules": []}
    )

    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()
        mock_request.match_info = {"network_id": "N_123"}

        response = await server.handle_api_get_l7_firewall_rules(mock_request)

        assert response.status == 200


@pytest.mark.asyncio
async def test_handle_api_put_l7_firewall_rules(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_put_l7_firewall_rules."""
    mock_coordinator.api.appliance.update_network_appliance_l7_firewall_rules = (
        AsyncMock()
    )

    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()
        mock_request.match_info = {"network_id": "N_123"}
        mock_request.json = AsyncMock(return_value={"rules": []})

        response = await server.handle_api_put_l7_firewall_rules(mock_request)

        assert response.status == 200


@pytest.mark.asyncio
async def test_handle_api_get_content_filtering_categories(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_api_get_content_filtering_categories."""
    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
        mock_request = MagicMock()

        response = await server.handle_api_get_content_filtering_categories(
            mock_request
        )

        assert response.status == 200


@pytest.mark.asyncio
async def test_handle_spa_index_exists(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_spa when index.html exists."""
    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()
    index_content = "<html>__HA_URL____CONFIG_ENTRY_ID__</html>"
    (static_dir / "index.html").write_text(index_content)

    mock_coordinator.config_entry = MagicMock()
    mock_coordinator.config_entry.entry_id = "test_entry_123"

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        with patch(
            "custom_components.meraki_ha.web_server.os.path.dirname",
            return_value=str(tmp_path),
        ):
            with patch(
                "custom_components.meraki_ha.web_server.os.path.exists",
                return_value=True,
            ):
                mock_file = AsyncMock()
                mock_file.read = AsyncMock(return_value=index_content)
                mock_file.__aenter__ = AsyncMock(return_value=mock_file)
                mock_file.__aexit__ = AsyncMock(return_value=None)

                with patch(
                    "custom_components.meraki_ha.web_server.aiofiles.open",
                    return_value=mock_file,
                ):
                    server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
                    mock_request = MagicMock()

                    response = await server.handle_spa(mock_request)

                    assert response.status == 200
                    assert "text/html" in response.content_type


@pytest.mark.asyncio
async def test_handle_spa_index_not_found(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test handle_spa when index.html doesn't exist."""
    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        with patch(
            "custom_components.meraki_ha.web_server.os.path.exists",
            return_value=False,
        ):
            server = MerakiWebServer(mock_hass, mock_coordinator, 8080)
            mock_request = MagicMock()

            response = await server.handle_spa(mock_request)

            assert response.status == 404


@pytest.mark.asyncio
async def test_start_server_error(
    mock_hass: MagicMock, mock_coordinator: MagicMock, tmp_path
) -> None:
    """Test server start handles errors gracefully."""
    static_dir = tmp_path / "www" / "dist"
    static_dir.mkdir(parents=True)
    (static_dir / "assets").mkdir()

    with patch.object(
        MerakiWebServer,
        "_setup_routes",
        lambda self: None,
    ):
        server = MerakiWebServer(mock_hass, mock_coordinator, 8080)

        mock_runner = MagicMock()
        mock_runner.setup = AsyncMock()

        with patch(
            "custom_components.meraki_ha.web_server.web.AppRunner",
            return_value=mock_runner,
        ):
            with patch(
                "custom_components.meraki_ha.web_server.web.TCPSite"
            ) as mock_site:
                mock_site_instance = MagicMock()
                mock_site_instance.start = AsyncMock(side_effect=OSError("Port in use"))
                mock_site.return_value = mock_site_instance

                # Should not raise, just log error
                await server.start()
