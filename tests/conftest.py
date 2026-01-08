import sys
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

# Mock the webrtc component for tests since it's a future feature
mock_webrtc = MagicMock()
sys.modules['homeassistant.components.webrtc'] = mock_webrtc
mock_webrtc.async_handle_webrtc_offer = MagicMock()


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


@pytest.fixture
def mock_meraki_api_client():
    """Mock Meraki API client for testing."""
    client = MagicMock()
    # Configure mock client as needed for specific tests
    return client


@pytest.fixture
def mock_config_entry():
    """Mock Home Assistant config entry for testing."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.options = {}  # Default empty options
    entry.data = {
        "api_key": "test_api_key",
        "organization_id": "test_org_id",
        "debug_enabled": False,
        "api_endpoint": "https://api.meraki.com/api/v1",
    }
    return entry


@pytest.fixture
def mock_hass():
    """Mock Home Assistant object."""
    hass = MagicMock(spec=HomeAssistant)
    hass.async_add_executor_job = MagicMock(side_effect=lambda func, *args: func(*args))
    hass.async_create_task = MagicMock()
    return hass


@pytest.fixture
def mock_coordinator(mock_hass, mock_meraki_api_client, mock_config_entry):
    """Mock MerakiDataCoordinator for testing."""
    from custom_components.meraki_ha.meraki_data_coordinator import (
        MerakiDataCoordinator,
    )
    coordinator = MerakiDataCoordinator(
        mock_hass, mock_meraki_api_client, mock_config_entry
    )
    coordinator.async_set_updated_data = AsyncMock() # Add this line
    return coordinator


@pytest.fixture
def mock_camera_service():
    """Mock CameraService for testing."""
    service = MagicMock()
    service.generate_snapshot = AsyncMock(return_value="http://mock_snapshot_url")
    return service

@pytest.fixture(autouse=True)
def prevent_socket_and_camera_load() -> Generator[None, None, None]:
    """Patch asyncio to prevent opening a real socket."""
    with (
        patch(
            "asyncio.base_events.BaseEventLoop.create_server", new_callable=AsyncMock
        ),
        patch("turbojpeg.TurboJPEG", MagicMock()),
        patch("aiodns.DNSResolver", MagicMock()),
    ):
        yield
