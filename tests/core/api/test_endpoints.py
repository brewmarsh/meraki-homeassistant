"""Tests for API endpoints."""

from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.core.api.endpoints.appliance import ApplianceEndpoints
from custom_components.meraki_ha.core.api.endpoints.camera import CameraEndpoints
from custom_components.meraki_ha.core.api.endpoints.cellular import CellularEndpoint
from custom_components.meraki_ha.core.api.endpoints.devices import DevicesEndpoints
from custom_components.meraki_ha.core.api.endpoints.network import NetworkEndpoints
from custom_components.meraki_ha.core.api.endpoints.organization import (
    OrganizationEndpoints,
)
from custom_components.meraki_ha.core.api.endpoints.switch import SwitchEndpoints
from custom_components.meraki_ha.core.api.endpoints.wireless import WirelessEndpoints


@pytest.fixture
def mock_api_client() -> MagicMock:
    """Create a mock API client."""
    client = MagicMock()
    client.dashboard = MagicMock()
    client._org_id = "org_123"
    client._hass = MagicMock()
    client.run_sync = MagicMock()
    return client


class TestNetworkEndpoints:
    """Tests for network API endpoints."""

    def test_initialization(self, mock_api_client: MagicMock) -> None:
        """Test network endpoint initialization."""
        endpoint = NetworkEndpoints(mock_api_client)

        assert endpoint is not None
        assert endpoint._api_client is mock_api_client


class TestDeviceEndpoints:
    """Tests for device API endpoints."""

    def test_initialization(self, mock_api_client: MagicMock) -> None:
        """Test device endpoint initialization."""
        endpoint = DevicesEndpoints(mock_api_client)

        assert endpoint is not None
        assert endpoint._api_client is mock_api_client


class TestApplianceEndpoints:
    """Tests for appliance API endpoints."""

    def test_initialization(self, mock_api_client: MagicMock) -> None:
        """Test appliance endpoint initialization."""
        # ApplianceEndpoints also needs hass
        endpoint = ApplianceEndpoints(mock_api_client, mock_api_client._hass)

        assert endpoint is not None
        assert endpoint._api_client is mock_api_client


class TestCameraEndpoints:
    """Tests for camera API endpoints."""

    def test_initialization(self, mock_api_client: MagicMock) -> None:
        """Test camera endpoint initialization."""
        endpoint = CameraEndpoints(mock_api_client)

        assert endpoint is not None
        assert endpoint._api_client is mock_api_client


class TestWirelessEndpoints:
    """Tests for wireless API endpoints."""

    def test_initialization(self, mock_api_client: MagicMock) -> None:
        """Test wireless endpoint initialization."""
        endpoint = WirelessEndpoints(mock_api_client)

        assert endpoint is not None
        assert endpoint._api_client is mock_api_client


class TestSwitchEndpoints:
    """Tests for switch API endpoints."""

    def test_initialization(self, mock_api_client: MagicMock) -> None:
        """Test switch endpoint initialization."""
        endpoint = SwitchEndpoints(mock_api_client)

        assert endpoint is not None
        assert endpoint._api_client is mock_api_client


class TestCellularEndpoints:
    """Tests for cellular API endpoints."""

    def test_initialization(self, mock_api_client: MagicMock) -> None:
        """Test cellular endpoint initialization."""
        endpoint = CellularEndpoint(mock_api_client)

        assert endpoint is not None
        assert endpoint._api_client is mock_api_client


class TestOrganizationEndpoints:
    """Tests for organization API endpoints."""

    def test_initialization(self, mock_api_client: MagicMock) -> None:
        """Test organization endpoint initialization."""
        endpoint = OrganizationEndpoints(mock_api_client)

        assert endpoint is not None
        assert endpoint._api_client is mock_api_client
