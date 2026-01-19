"""Global fixtures for meraki_ha integration."""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest

from tests.const import MOCK_ALL_DATA


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations: None,
) -> Generator[None, None, None]:
    """
    Enable custom integrations defined in the test dir.

    Args:
        enable_custom_integrations: The fixture to enable custom integrations.

    """
    yield


<<<<<<< HEAD
@pytest.fixture(autouse=True)
def bypass_platform_setup() -> Generator[None, None, None]:
    """Bypass platform setup to avoid hass_frontend dependency."""
    from unittest.mock import patch
    with patch("homeassistant.setup.async_setup_component", return_value=True):
        yield


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
=======
@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiDataCoordinator."""
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = MOCK_ALL_DATA
    coordinator.async_request_refresh = AsyncMock()
    coordinator.async_write_ha_state = MagicMock()
<<<<<<< HEAD
=======
    coordinator.is_update_pending = MagicMock(return_value=False)
    coordinator.register_update_pending = MagicMock()
    coordinator.async_request_refresh = AsyncMock()
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
    return coordinator


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry
<<<<<<< HEAD
=======


@pytest.fixture(autouse=True)
def mock_dns_resolution(monkeypatch):
    """Mock DNS resolution to prevent test crashes."""
    monkeypatch.setattr("aiodns.DNSResolver", MagicMock())


@pytest.fixture(autouse=True)
def prevent_socket_and_camera_load() -> Generator[None, None, None]:
    """Patch asyncio to prevent opening a real socket."""
    from unittest.mock import MagicMock, patch

    with (
        patch(
            "asyncio.base_events.BaseEventLoop.create_server", new_callable=AsyncMock
        ),
        patch("turbojpeg.TurboJPEG", MagicMock()),
    ):
        yield
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)
