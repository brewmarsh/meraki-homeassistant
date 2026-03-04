"""Global fixtures for meraki_ha integration."""

import sys
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from tests.const import (
    MOCK_ALL_DATA,
    MOCK_DEVICE_INIT,
    MOCK_GX_DEVICE_INIT,
    MOCK_MX_DEVICE_INIT,
    MOCK_NETWORK_INIT,
)


@pytest.fixture(autouse=True)
def mock_meraki() -> None:
    """Mock meraki module to avoid installation issues."""
    if "meraki" not in sys.modules:
        mock_meraki_module = MagicMock()
        mock_exceptions_module = MagicMock()

        # Create a mock exception class
        class MockAPIError(Exception):
            pass

        mock_exceptions_module.APIError = MockAPIError

        # Link them
        mock_meraki_module.exceptions = mock_exceptions_module

        sys.modules["meraki"] = mock_meraki_module
        sys.modules["meraki.exceptions"] = mock_exceptions_module


@pytest.fixture(autouse=True)
def mock_aiortc() -> None:
    """Mock aiortc module to avoid installation issues."""
    if "aiortc" not in sys.modules:
        sys.modules["aiortc"] = MagicMock()
    if "aiortc.contrib" not in sys.modules:
        sys.modules["aiortc.contrib"] = MagicMock()
    if "aiortc.contrib.media" not in sys.modules:
        sys.modules["aiortc.contrib.media"] = MagicMock()


@pytest.fixture(autouse=True)
def mock_http(hass: HomeAssistant) -> None:
    """Mock the http component."""
    hass.http = MagicMock()
    hass.http.register_view = MagicMock()
    hass.http.async_register_static_paths = AsyncMock()


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
    with patch("homeassistant.setup.async_setup_component", return_value=True):
        yield


@pytest.fixture(name="mock_coordinator")  # type: ignore[untyped-decorator]
def fixture_mock_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiMainCoordinator."""
    coordinator = MagicMock()
    coordinator.config_entry.options = {}
    coordinator.data = MOCK_ALL_DATA
    coordinator.async_write_ha_state = MagicMock()
    coordinator.is_update_pending = MagicMock(return_value=False)
    coordinator.register_pending_update = MagicMock()
    return coordinator


@pytest.fixture(name="mock_config_entry")  # type: ignore[untyped-decorator]
def fixture_mock_config_entry() -> MagicMock:
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock()
    entry.options = {}
    return entry


@pytest.fixture(name="mock_meraki_client")  # type: ignore[untyped-decorator]
def fixture_mock_meraki_client() -> Generator[MagicMock, None, None]:
    """Fixture for a mocked Meraki API client."""
    with patch(
        "custom_components.meraki_ha.core.api.client.meraki.DashboardAPI"
    ) as mock_api:
        mock_dashboard = mock_api.return_value

        org_data = {"id": "12345", "name": "Test Organization"}
        networks = [MOCK_NETWORK_INIT]
        devices = [MOCK_DEVICE_INIT, MOCK_MX_DEVICE_INIT, MOCK_GX_DEVICE_INIT]

        mock_dashboard.organizations.configure_mock(
            **{
                "getOrganizations.return_value": [org_data],
                "getOrganization.return_value": org_data,
                "getOrganizationNetworks.return_value": networks,
                "getOrganizationDevices.return_value": devices,
                "getOrganizationDevicesStatuses.return_value": [],
                "getOrganizationDevicesAvailabilities.return_value": [],
            }
        )
        mock_dashboard.networks.getOrganizationNetworks.return_value = networks
        mock_dashboard.devices.getOrganizationDevices.return_value = devices

        mock_dashboard.appliance.configure_mock(
            **{
                "getOrganizationApplianceUplinkStatuses.return_value": [],
                "getNetworkApplianceVlans.return_value": [],
                "getNetworkApplianceFirewallL3FirewallRules.return_value": {},
                "getNetworkApplianceTrafficShaping.return_value": {},
                "getNetworkApplianceVpnSiteToSiteVpn.return_value": {},
                "getNetworkApplianceContentFiltering.return_value": {},
                "getNetworkApplianceSettings.return_value": {},
                "getNetworkApplianceL7FirewallRules.return_value": {},
                "getNetworkAppliancePorts.return_value": [],
            }
        )

        mock_dashboard.sensor.getOrganizationSensorReadingsLatest.return_value = []
        mock_dashboard.switch.getDeviceSwitchPortsStatuses.return_value = []

        mock_dashboard.wireless.configure_mock(
            **{
                "getNetworkWirelessSsids.return_value": [],
                "getNetworkWirelessRfProfiles.return_value": [],
            }
        )

        mock_dashboard.camera.configure_mock(
            **{
                "getDeviceCameraVideoSettings.return_value": {},
                "getDeviceCameraSense.return_value": {},
                "getDeviceCameraAnalyticsRecent.return_value": [],
            }
        )

        yield mock_api
