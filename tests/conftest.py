"""Global fixtures for meraki_ha integration."""

import sys
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.const import MOCK_ALL_DATA


@pytest.fixture(autouse=True)
def mock_aiortc():
    """Mock aiortc module to avoid installation issues."""
    if "aiortc" not in sys.modules:
        sys.modules["aiortc"] = MagicMock()
    if "aiortc.contrib" not in sys.modules:
        sys.modules["aiortc.contrib"] = MagicMock()
    if "aiortc.contrib.media" not in sys.modules:
        sys.modules["aiortc.contrib.media"] = MagicMock()


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


@pytest.fixture(autouse=True)
def bypass_platform_setup() -> Generator[None, None, None]:
    """Bypass platform setup to avoid hass_frontend dependency."""
    yield


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiDataUpdateCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = MOCK_ALL_DATA
    coordinator.async_request_refresh = AsyncMock()
    coordinator.async_write_ha_state = MagicMock()
    return coordinator


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry


@pytest.fixture
def mock_meraki_client():
    """Fixture for a mocked Meraki API client."""
    with patch(
        "custom_components.meraki_ha.authentication.meraki.AsyncDashboardAPI",
        autospec=True,
    ) as mock_api:
        mock_dashboard = mock_api.return_value.__aenter__.return_value
        mock_dashboard.organizations.getOrganizations = AsyncMock(
            return_value=[{"id": "12345", "name": "Test Organization"}]
        )
        mock_dashboard.networks.getOrganizationNetworks = AsyncMock(
            return_value=[{"id": "N_123", "name": "Test Network"}]
        )
        yield mock_api
