"""Global fixtures for meraki_ha integration."""

import sys
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tests.const import (
    MOCK_ALL_DATA,
    MOCK_DEVICE_INIT,
    MOCK_GX_DEVICE_INIT,
    MOCK_MX_DEVICE_INIT,
    MOCK_NETWORK_INIT,
)


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
def mock_http(hass):
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
        "custom_components.meraki_ha.core.api.client.meraki.DashboardAPI"
    ) as mock_api:
        mock_dashboard = mock_api.return_value

        # Organizations
        mock_dashboard.organizations = MagicMock()
        mock_dashboard.organizations.getOrganizations.return_value = [
            {"id": "12345", "name": "Test Organization"}
        ]
        mock_dashboard.organizations.getOrganization.return_value = {
            "id": "12345",
            "name": "Test Organization",
        }
        mock_dashboard.organizations.getOrganizationNetworks.return_value = [
            MOCK_NETWORK_INIT
        ]
        mock_dashboard.organizations.getOrganizationDevices.return_value = [
            MOCK_DEVICE_INIT,
            MOCK_MX_DEVICE_INIT,
            MOCK_GX_DEVICE_INIT,
        ]
        mock_dashboard.organizations.getOrganizationDevicesStatuses.return_value = []
        (
            mock_dashboard.organizations.getOrganizationDevicesAvailabilities.return_value
        ) = []

        # Networks
        mock_dashboard.networks = MagicMock()
        # Some endpoints might still use this path depending on lib version
        mock_dashboard.networks.getOrganizationNetworks.return_value = [
            MOCK_NETWORK_INIT
        ]

        # Devices
        mock_dashboard.devices = MagicMock()
        mock_dashboard.devices.getOrganizationDevices.return_value = [
            MOCK_DEVICE_INIT,
            MOCK_MX_DEVICE_INIT,
            MOCK_GX_DEVICE_INIT,
        ]

        # Appliance
        mock_dashboard.appliance = MagicMock()
        mock_dashboard.appliance.getOrganizationApplianceUplinkStatuses.return_value = []
        mock_dashboard.appliance.getNetworkApplianceVlans.return_value = []
        mock_dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules.return_value = {}  # noqa: E501
        mock_dashboard.appliance.getNetworkApplianceTrafficShaping.return_value = {}
        mock_dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn.return_value = {}
        mock_dashboard.appliance.getNetworkApplianceContentFiltering.return_value = {}
        mock_dashboard.appliance.getNetworkApplianceSettings.return_value = {}
        mock_dashboard.appliance.getNetworkApplianceL7FirewallRules.return_value = {}
        mock_dashboard.appliance.getNetworkAppliancePorts.return_value = []

        # Sensor
        mock_dashboard.sensor = MagicMock()
        mock_dashboard.sensor.getOrganizationSensorReadingsLatest.return_value = []

        # Wireless
        mock_dashboard.wireless = MagicMock()
        mock_dashboard.wireless.getNetworkWirelessSsids.return_value = []
        mock_dashboard.wireless.getNetworkWirelessRfProfiles.return_value = []

        # Camera
        mock_dashboard.camera = MagicMock()
        mock_dashboard.camera.getDeviceCameraVideoSettings.return_value = {}
        mock_dashboard.camera.getDeviceCameraSense.return_value = {}
        mock_dashboard.camera.getDeviceCameraAnalyticsRecent.return_value = []

        # Switch
        mock_dashboard.switch = MagicMock()
        mock_dashboard.switch.getDeviceSwitchPortsStatuses.return_value = []

        yield mock_api
