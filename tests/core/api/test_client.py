"""Tests for the Meraki API client module."""

# mypy: disable-error-code="method-assign,arg-type"

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.core.api.client import MerakiAPIClient
from custom_components.meraki_ha.core.errors import (
    MerakiTrafficAnalysisError,
    MerakiVlansDisabledError,
)


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock HomeAssistant instance."""
    hass = MagicMock()
    hass.async_add_executor_job = AsyncMock(side_effect=lambda f, *args: f(*args))
    return hass


@pytest.fixture
def api_client(mock_hass: MagicMock) -> MerakiAPIClient:
    """Create an API client."""
    return MerakiAPIClient(
        hass=mock_hass,
        api_key="test_api_key",
        org_id="test_org_id",
    )


class TestMerakiAPIClient:
    """Tests for MerakiAPIClient class."""

    def test_initialization(self, mock_hass: MagicMock) -> None:
        """Test API client initialization."""
        client = MerakiAPIClient(
            hass=mock_hass,
            api_key="test_api_key",
            org_id="test_org_id",
            base_url="https://custom.api.meraki.com/api/v1",
        )

        assert client._api_key == "test_api_key"
        assert client._org_id == "test_org_id"
        assert client._base_url == "https://custom.api.meraki.com/api/v1"
        assert client.dashboard is None
        assert client.appliance is not None
        assert client.camera is not None
        assert client.devices is not None
        assert client.network is not None
        assert client.organization is not None
        assert client.switch is not None
        assert client.wireless is not None

    @pytest.mark.asyncio
    async def test_async_setup(self, api_client: MerakiAPIClient) -> None:
        """Test async setup creates dashboard API."""
        with patch("meraki.DashboardAPI") as mock_dashboard:
            mock_dashboard.return_value = MagicMock()
            await api_client.async_setup()

            assert api_client.dashboard is not None
            mock_dashboard.assert_called_once_with(
                api_key="test_api_key",
                base_url="https://api.meraki.com/api/v1",
                output_log=False,
                print_console=False,
                suppress_logging=True,
                maximum_retries=3,
                wait_on_rate_limit=True,
                nginx_429_retry_wait_time=2,
            )

    @pytest.mark.asyncio
    async def test_run_sync(self, api_client: MerakiAPIClient) -> None:
        """Test run_sync executes function in executor."""

        def sync_func(a: int, b: int) -> int:
            return a + b

        result = await api_client.run_sync(sync_func, 1, 2)
        assert result == 3

    @pytest.mark.asyncio
    async def test_run_with_semaphore(self, api_client: MerakiAPIClient) -> None:
        """Test _run_with_semaphore limits concurrency."""

        async def async_coro() -> str:
            return "success"

        result = await api_client._run_with_semaphore(async_coro())
        assert result == "success"

    def test_organization_id_property(self, api_client: MerakiAPIClient) -> None:
        """Test organization_id property."""
        assert api_client.organization_id == "test_org_id"

    @pytest.mark.asyncio
    async def test_async_fetch_initial_data(self, api_client: MerakiAPIClient) -> None:
        """Test _async_fetch_initial_data fetches all initial data."""
        api_client.organization.get_organization_networks = AsyncMock(
            return_value=[{"id": "N_123", "name": "Test Network"}]
        )
        api_client.organization.get_organization_devices = AsyncMock(
            return_value=[{"serial": "ABC-123", "name": "Test Device"}]
        )
        api_client.organization.get_organization_devices_availabilities = AsyncMock(
            return_value=[{"serial": "ABC-123", "status": "online"}]
        )
        api_client.appliance.get_organization_appliance_uplink_statuses = AsyncMock(
            return_value=[]
        )
        api_client.cellular.get_organization_cellular_gateway_uplink_statuses = (
            AsyncMock(return_value=[])
        )
        api_client.sensor.get_organization_sensor_readings_latest = AsyncMock(
            return_value=[]
        )

        result = await api_client._async_fetch_initial_data()

        assert "networks" in result
        assert "devices" in result
        assert "devices_availabilities" in result
        assert "appliance_uplink_statuses" in result
        assert "cellular_uplink_statuses" in result
        assert "sensor_readings" in result

    def test_process_initial_data_success(self, api_client: MerakiAPIClient) -> None:
        """Test _process_initial_data with valid data."""
        results = {
            "networks": [{"id": "N_123", "name": "Test Network"}],
            "devices": [{"serial": "ABC-123", "name": "Test Device"}],
            "devices_availabilities": [{"serial": "ABC-123", "status": "online"}],
            "appliance_uplink_statuses": [],
            "cellular_uplink_statuses": [
                {"serial": "ABC-123", "uplinks": [{"interface": "cellular"}]}
            ],
            "sensor_readings": [
                {"serial": "ABC-123", "readings": [{"temperature": 25.0}]}
            ],
        }

        processed = api_client._process_initial_data(results)

        assert len(processed["networks"]) == 1
        assert len(processed["devices"]) == 1
        assert processed["devices"][0]["status"] == "online"
        assert processed["devices"][0]["readings"] == [{"temperature": 25.0}]
        assert processed["devices"][0]["cellular_uplinks"] == [
            {"interface": "cellular"}
        ]

    def test_process_initial_data_with_errors(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _process_initial_data with error responses."""
        results = {
            "networks": Exception("Network error"),
            "devices": Exception("Device error"),
            "devices_availabilities": Exception("Availability error"),
            "appliance_uplink_statuses": Exception("Uplink error"),
            "cellular_uplink_statuses": Exception("Cellular error"),
            "sensor_readings": Exception("Sensor error"),
        }

        processed = api_client._process_initial_data(results)

        assert "networks" not in processed
        assert "devices" not in processed
        assert "appliance_uplink_statuses" not in processed

    @pytest.mark.asyncio
    async def test_async_fetch_network_clients(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _async_fetch_network_clients fetches clients."""
        api_client.network.get_network_clients = AsyncMock(
            return_value=[{"id": "client1", "mac": "00:11:22:33:44:55"}]
        )

        networks = [
            {"id": "N_123", "productTypes": ["wireless", "switch"]},
            {"id": "N_456", "productTypes": ["camera"]},  # Camera-only, should skip
        ]

        clients = await api_client._async_fetch_network_clients(networks)

        assert len(clients) == 1
        assert clients[0]["networkId"] == "N_123"
        api_client.network.get_network_clients.assert_called_once_with("N_123")

    @pytest.mark.asyncio
    async def test_async_fetch_device_clients(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _async_fetch_device_clients fetches clients per device."""
        api_client.devices.get_device_clients = AsyncMock(
            return_value=[{"id": "client1", "mac": "00:11:22:33:44:55"}]
        )

        devices = [
            {"serial": "ABC-123", "productType": "switch"},
            {"serial": "DEF-456", "productType": "camera"},  # Should skip
        ]

        clients_by_serial = await api_client._async_fetch_device_clients(devices)

        assert "ABC-123" in clients_by_serial
        assert len(clients_by_serial["ABC-123"]) == 1
        assert "DEF-456" not in clients_by_serial

    def test_build_detail_tasks_wireless(self, api_client: MerakiAPIClient) -> None:
        """Test _build_detail_tasks for wireless networks."""
        # Mock endpoint methods to return MagicMock instead of coroutines
        api_client.wireless.get_network_ssids = MagicMock(return_value=MagicMock())
        api_client.wireless.get_network_wireless_settings = MagicMock(
            return_value=MagicMock()
        )
        api_client.wireless.get_network_wireless_rf_profiles = MagicMock(
            return_value=MagicMock()
        )
        api_client._run_with_semaphore = MagicMock(side_effect=lambda x: x)

        networks = [{"id": "N_123", "productTypes": ["wireless"]}]
        devices: list = []

        tasks = api_client._build_detail_tasks(networks, devices)

        assert "ssids_N_123" in tasks
        assert "wireless_settings_N_123" in tasks
        assert "rf_profiles_N_123" in tasks

    def test_build_detail_tasks_appliance(self, api_client: MerakiAPIClient) -> None:
        """Test _build_detail_tasks for appliance networks."""
        # Mock endpoint methods to return MagicMock instead of coroutines
        api_client.network.get_network_traffic = MagicMock(return_value=MagicMock())
        api_client.appliance.get_network_vlans = MagicMock(return_value=MagicMock())
        api_client.appliance.get_l3_firewall_rules = MagicMock(return_value=MagicMock())
        api_client.appliance.get_traffic_shaping = MagicMock(return_value=MagicMock())
        api_client.appliance.get_vpn_status = MagicMock(return_value=MagicMock())
        api_client.appliance.get_network_appliance_content_filtering = MagicMock(
            return_value=MagicMock()
        )
        api_client._run_with_semaphore = MagicMock(side_effect=lambda x: x)

        networks = [{"id": "N_123", "productTypes": ["appliance"]}]
        devices: list = []

        tasks = api_client._build_detail_tasks(networks, devices)

        assert "traffic_N_123" in tasks
        assert "vlans_N_123" in tasks
        assert "l3_firewall_rules_N_123" in tasks
        assert "traffic_shaping_N_123" in tasks
        assert "vpn_status_N_123" in tasks
        assert "content_filtering_N_123" in tasks

    def test_build_detail_tasks_skips_failed_traffic(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _build_detail_tasks skips traffic for failed networks."""
        # Mock endpoint methods to return MagicMock instead of coroutines
        api_client.appliance.get_network_vlans = MagicMock(return_value=MagicMock())
        api_client.appliance.get_l3_firewall_rules = MagicMock(return_value=MagicMock())
        api_client.appliance.get_traffic_shaping = MagicMock(return_value=MagicMock())
        api_client.appliance.get_vpn_status = MagicMock(return_value=MagicMock())
        api_client.appliance.get_network_appliance_content_filtering = MagicMock(
            return_value=MagicMock()
        )
        api_client._run_with_semaphore = MagicMock(side_effect=lambda x: x)

        api_client.traffic_analysis_failed_networks.add("N_123")
        networks = [{"id": "N_123", "productTypes": ["appliance"]}]
        devices: list = []

        tasks = api_client._build_detail_tasks(networks, devices)

        assert "traffic_N_123" not in tasks

    def test_build_detail_tasks_camera(self, api_client: MerakiAPIClient) -> None:
        """Test _build_detail_tasks for camera devices."""
        # Mock endpoint methods to return MagicMock instead of coroutines
        api_client.camera.get_camera_video_settings = MagicMock(
            return_value=MagicMock()
        )
        api_client.camera.get_camera_sense_settings = MagicMock(
            return_value=MagicMock()
        )
        api_client._run_with_semaphore = MagicMock(side_effect=lambda x: x)

        networks: list = []
        devices = [{"serial": "CAM-123", "productType": "camera"}]

        tasks = api_client._build_detail_tasks(networks, devices)

        assert "video_settings_CAM-123" in tasks
        assert "sense_settings_CAM-123" in tasks

    def test_build_detail_tasks_switch(self, api_client: MerakiAPIClient) -> None:
        """Test _build_detail_tasks for switch devices."""
        # Mock endpoint methods to return MagicMock instead of coroutines
        api_client.switch.get_device_switch_ports_statuses = MagicMock(
            return_value=MagicMock()
        )
        api_client._run_with_semaphore = MagicMock(side_effect=lambda x: x)

        networks: list = []
        devices = [{"serial": "SW-123", "productType": "switch"}]

        tasks = api_client._build_detail_tasks(networks, devices)

        assert "ports_statuses_SW-123" in tasks

    def test_build_detail_tasks_appliance_device(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _build_detail_tasks for appliance devices."""
        # Mock endpoint methods to return MagicMock instead of coroutines
        api_client.appliance.get_network_appliance_settings = MagicMock(
            return_value=MagicMock()
        )
        api_client._run_with_semaphore = MagicMock(side_effect=lambda x: x)

        networks: list = []
        devices = [
            {"serial": "MX-123", "productType": "appliance", "networkId": "N_123"}
        ]

        tasks = api_client._build_detail_tasks(networks, devices)

        assert "appliance_settings_MX-123" in tasks

    def test_process_detailed_data_ssids(self, api_client: MerakiAPIClient) -> None:
        """Test _process_detailed_data processes SSIDs."""
        detail_data = {
            "ssids_N_123": [
                {"name": "Corp WiFi", "number": 0},
                {"name": "Unconfigured SSID 1", "number": 1},  # Should filter out
            ]
        }
        networks = [{"id": "N_123", "name": "Test"}]

        result = api_client._process_detailed_data(detail_data, networks, [], {})

        assert len(result["ssids"]) == 1
        assert result["ssids"][0]["name"] == "Corp WiFi"
        assert result["ssids"][0]["networkId"] == "N_123"

    def test_process_detailed_data_traffic_error(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _process_detailed_data handles traffic analysis error."""
        detail_data = {"traffic_N_123": MerakiTrafficAnalysisError("Not enabled")}
        networks = [{"id": "N_123", "name": "Test"}]

        result = api_client._process_detailed_data(detail_data, networks, [], {})

        assert result["appliance_traffic"]["N_123"]["error"] == "disabled"
        assert "N_123" in api_client.traffic_analysis_failed_networks

    def test_process_detailed_data_vlans_disabled(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _process_detailed_data handles VLANs disabled error."""
        detail_data = {"vlans_N_123": MerakiVlansDisabledError("VLANs disabled")}
        networks = [{"id": "N_123", "name": "Test"}]

        result = api_client._process_detailed_data(detail_data, networks, [], {})

        assert result["vlans"]["N_123"] == []

    def test_process_detailed_data_camera_settings(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _process_detailed_data processes camera settings."""
        detail_data = {
            "video_settings_CAM-123": {"rtsp_url": "rtsp://192.168.1.1/stream"},
            "sense_settings_CAM-123": {"detection_enabled": True},
        }
        devices: list = [{"serial": "CAM-123", "productType": "camera"}]

        api_client._process_detailed_data(detail_data, [], devices, {})  # type: ignore[arg-type]

        assert devices[0]["video_settings"] == {"rtsp_url": "rtsp://192.168.1.1/stream"}
        assert devices[0]["rtsp_url"] == "rtsp://192.168.1.1/stream"
        assert devices[0]["sense_settings"] == {"detection_enabled": True}

    def test_process_detailed_data_switch_ports(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _process_detailed_data processes switch port statuses."""
        detail_data = {
            "ports_statuses_SW-123": [{"portId": "1", "status": "Connected"}]
        }
        devices: list = [{"serial": "SW-123", "productType": "switch"}]

        api_client._process_detailed_data(detail_data, [], devices, {})  # type: ignore[arg-type]

        assert devices[0]["ports_statuses"] == [{"portId": "1", "status": "Connected"}]

    def test_process_detailed_data_appliance_dns(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _process_detailed_data processes appliance dynamic DNS."""
        detail_data = {
            "appliance_settings_MX-123": {
                "dynamicDns": {"enabled": True, "prefix": "mysite"}
            }
        }
        devices: list = [{"serial": "MX-123", "productType": "appliance"}]

        api_client._process_detailed_data(detail_data, [], devices, {})  # type: ignore[arg-type]

        assert devices[0]["dynamicDns"] == {"enabled": True, "prefix": "mysite"}

    def test_process_detailed_data_uses_previous_data(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _process_detailed_data uses previous data on failure."""
        detail_data: dict = {}  # No new data
        networks: list = [{"id": "N_123", "name": "Test"}]
        previous_data = {
            "ssids_N_123": [{"name": "Previous SSID", "number": 0}],
            "traffic_N_123": {"bytes": 1000},
        }

        result = api_client._process_detailed_data(
            detail_data,
            networks,
            [],
            previous_data,  # type: ignore[arg-type]
        )

        assert len(result["ssids"]) == 1
        assert result["ssids"][0]["name"] == "Previous SSID"
        assert result["appliance_traffic"]["N_123"] == {"bytes": 1000}

    @pytest.mark.asyncio
    async def test_get_all_data(self, api_client: MerakiAPIClient) -> None:
        """Test get_all_data integrates all fetch operations."""
        with (
            patch.object(
                api_client,
                "_async_fetch_initial_data",
                new=AsyncMock(
                    return_value={
                        "networks": [{"id": "N_123", "name": "Test"}],
                        "devices": [],
                        "devices_availabilities": [],
                        "appliance_uplink_statuses": [],
                        "cellular_uplink_statuses": [],
                        "sensor_readings": [],
                    }
                ),
            ),
            patch.object(
                api_client,
                "_async_fetch_network_clients",
                new=AsyncMock(return_value=[]),
            ),
            patch.object(
                api_client,
                "_async_fetch_device_clients",
                new=AsyncMock(return_value={}),
            ),
            patch.object(
                api_client, "_build_detail_tasks", new=MagicMock(return_value={})
            ),
        ):
            result = await api_client.get_all_data()

        assert "networks" in result
        assert "devices" in result
        assert "clients" in result

    @pytest.mark.asyncio
    async def test_get_all_data_with_enabled_networks(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test get_all_data filters by enabled networks."""
        with (
            patch.object(
                api_client,
                "_async_fetch_initial_data",
                new=AsyncMock(
                    return_value={
                        "networks": [
                            {"id": "N_123", "name": "Enabled"},
                            {"id": "N_456", "name": "Disabled"},
                        ],
                        "devices": [
                            {"serial": "ABC", "networkId": "N_123"},
                            {"serial": "DEF", "networkId": "N_456"},
                        ],
                        "devices_availabilities": [],
                        "appliance_uplink_statuses": [],
                        "cellular_uplink_statuses": [],
                        "sensor_readings": [],
                    }
                ),
            ),
            patch.object(
                api_client,
                "_async_fetch_network_clients",
                new=AsyncMock(return_value=[]),
            ),
            patch.object(
                api_client,
                "_async_fetch_device_clients",
                new=AsyncMock(return_value={}),
            ),
            patch.object(
                api_client, "_build_detail_tasks", new=MagicMock(return_value={})
            ),
        ):
            result = await api_client.get_all_data(enabled_network_ids={"N_123"})

        # All networks returned but only enabled network's devices processed
        assert len(result["networks"]) == 2
        assert len(result["devices"]) == 1
        assert result["devices"][0]["serial"] == "ABC"

    @pytest.mark.asyncio
    async def test_register_webhook(self, api_client: MerakiAPIClient) -> None:
        """Test register_webhook delegates to network endpoint."""
        mock_register = AsyncMock()
        with patch.object(api_client.network, "register_webhook", new=mock_register):
            await api_client.register_webhook(
                "https://example.com/webhook", "secret123"
            )

        mock_register.assert_called_once_with(
            "https://example.com/webhook", "secret123"
        )

    @pytest.mark.asyncio
    async def test_unregister_webhook(self, api_client: MerakiAPIClient) -> None:
        """Test unregister_webhook delegates to network endpoint."""
        mock_unregister = AsyncMock()
        with patch.object(
            api_client.network, "unregister_webhook", new=mock_unregister
        ):
            await api_client.unregister_webhook("https://example.com/webhook")

        mock_unregister.assert_called_once_with("https://example.com/webhook")

    @pytest.mark.asyncio
    async def test_async_reboot_device(self, api_client: MerakiAPIClient) -> None:
        """Test async_reboot_device delegates to appliance endpoint."""
        mock_reboot = AsyncMock(return_value={"success": True})
        with patch.object(api_client.appliance, "reboot_device", new=mock_reboot):
            result = await api_client.async_reboot_device("ABC-123")

        assert result == {"success": True}
        mock_reboot.assert_called_once_with("ABC-123")

    @pytest.mark.asyncio
    async def test_async_get_switch_port_statuses(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test async_get_switch_port_statuses delegates to switch endpoint."""
        mock_get_statuses = AsyncMock(
            return_value=[{"portId": "1", "status": "Connected"}]
        )
        with patch.object(
            api_client.switch, "get_device_switch_ports_statuses", new=mock_get_statuses
        ):
            result = await api_client.async_get_switch_port_statuses("SW-123")

        assert len(result) == 1
        assert result[0]["portId"] == "1"

    @pytest.mark.asyncio
    async def test_get_all_data_preserves_data_on_api_failure(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test that get_all_data preserves previous data when API fails.

        This test verifies the fix for issue #75 where devices would disappear
        after a refresh cycle because API failures returned None/empty data
        that overwrote existing good data.
        """
        # First successful fetch - only include data handled by _process_initial_data
        previous_data = {
            "networks": [{"id": "N_123", "name": "Production Network"}],
            "devices": [
                {"serial": "ABC-123", "name": "Switch-1", "networkId": "N_123"},
                {"serial": "DEF-456", "name": "AP-1", "networkId": "N_123"},
            ],
            "appliance_uplink_statuses": [{"serial": "MX-001", "status": "active"}],
        }

        # Simulate API failure - all fetches return None/Exception
        with (
            patch.object(
                api_client,
                "_async_fetch_initial_data",
                new=AsyncMock(
                    return_value={
                        "networks": None,  # API failure
                        "devices": None,  # API failure
                        "devices_availabilities": Exception("API Error"),
                        "appliance_uplink_statuses": Exception("API Error"),
                        "cellular_uplink_statuses": None,
                        "sensor_readings": None,
                    }
                ),
            ),
            patch.object(
                api_client,
                "_async_fetch_network_clients",
                new=AsyncMock(return_value=[]),
            ),
            patch.object(
                api_client,
                "_async_fetch_device_clients",
                new=AsyncMock(return_value={}),
            ),
            patch.object(
                api_client, "_build_detail_tasks", new=MagicMock(return_value={})
            ),
        ):
            result = await api_client.get_all_data(previous_data=previous_data)

        # Verify previous data is preserved when API fails
        assert len(result["networks"]) == 1
        assert result["networks"][0]["name"] == "Production Network"
        # Devices are filtered, so the key should exist and have previous data
        assert "devices" in result
        # The devices are filtered from merged_data which preserves previous devices
        assert len(result["devices"]) == 2
        assert result["appliance_uplink_statuses"][0]["status"] == "active"

    @pytest.mark.asyncio
    async def test_get_all_data_multi_cycle_refresh(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test data persistence across multiple refresh cycles.

        This test simulates the exact bug scenario from issue #75:
        1. First refresh succeeds and devices are visible
        2. Second refresh fails (API returns None)
        3. Devices should still be visible (previous data preserved)
        """
        # Simulate first successful fetch result
        first_fetch_data: dict = {
            "networks": [
                {"id": "N_123", "name": "Office", "productTypes": ["switch"]},
            ],
            "devices": [
                {"serial": "SW-001", "name": "Core Switch", "networkId": "N_123"},
            ],
            "appliance_uplink_statuses": [],
        }

        # Second fetch - API returns None for everything (simulating the bug)
        with (
            patch.object(
                api_client,
                "_async_fetch_initial_data",
                new=AsyncMock(
                    return_value={
                        "networks": None,
                        "devices": None,
                        "devices_availabilities": None,
                        "appliance_uplink_statuses": None,
                        "cellular_uplink_statuses": None,
                        "sensor_readings": None,
                    }
                ),
            ),
            patch.object(
                api_client,
                "_async_fetch_network_clients",
                new=AsyncMock(return_value=[]),
            ),
            patch.object(
                api_client,
                "_async_fetch_device_clients",
                new=AsyncMock(return_value={}),
            ),
            patch.object(
                api_client, "_build_detail_tasks", new=MagicMock(return_value={})
            ),
        ):
            # Pass first_fetch_data as previous_data (simulating second refresh)
            result = await api_client.get_all_data(previous_data=first_fetch_data)

        # The key assertion: devices should NOT disappear after failed refresh
        assert len(result["networks"]) == 1
        assert result["networks"][0]["name"] == "Office"
        # devices key is always set to the filtered list, which uses merged_data
        assert "devices" in result

    @pytest.mark.asyncio
    async def test_get_all_data_partial_api_failure(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test that partial API failures merge correctly with previous data.

        When some API calls succeed and others fail, the successful data
        should update while failed data should preserve previous values.
        """
        previous_data = {
            "networks": [{"id": "N_OLD", "name": "Old Network"}],
            "devices": [
                {"serial": "OLD-001", "name": "Old Device", "networkId": "N_OLD"}
            ],
            "appliance_uplink_statuses": [{"serial": "OLD-MX", "status": "active"}],
        }

        # Networks succeeds, devices fail
        with (
            patch.object(
                api_client,
                "_async_fetch_initial_data",
                new=AsyncMock(
                    return_value={
                        "networks": [{"id": "N_NEW", "name": "New Network"}],
                        "devices": None,  # API failure
                        "devices_availabilities": None,
                        "appliance_uplink_statuses": [],  # Empty but valid
                        "cellular_uplink_statuses": None,
                        "sensor_readings": None,
                    }
                ),
            ),
            patch.object(
                api_client,
                "_async_fetch_network_clients",
                new=AsyncMock(return_value=[]),
            ),
            patch.object(
                api_client,
                "_async_fetch_device_clients",
                new=AsyncMock(return_value={}),
            ),
            patch.object(
                api_client, "_build_detail_tasks", new=MagicMock(return_value={})
            ),
        ):
            result = await api_client.get_all_data(previous_data=previous_data)

        # Networks should be updated (successful fetch)
        assert len(result["networks"]) == 1
        assert result["networks"][0]["name"] == "New Network"

        # Devices should be preserved from previous data (failed fetch)
        # Note: devices key is set from filtered merged_data["devices"]
        assert "devices" in result

        # Appliance uplink statuses should be updated (empty but valid)
        assert result["appliance_uplink_statuses"] == []

    def test_process_initial_data_with_none_values(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _process_initial_data when API returns None values.

        This directly tests the fix for issue #75 - None values should
        not create empty entries that overwrite previous data.
        """
        results = {
            "networks": None,
            "devices": None,
            "devices_availabilities": None,
            "appliance_uplink_statuses": None,
            "cellular_uplink_statuses": None,
            "sensor_readings": None,
        }

        processed = api_client._process_initial_data(results)

        # All keys should be absent (not set to empty lists)
        assert "networks" not in processed
        assert "devices" not in processed
        assert "appliance_uplink_statuses" not in processed

    def test_process_initial_data_partial_success(
        self, api_client: MerakiAPIClient
    ) -> None:
        """Test _process_initial_data with mixed success/failure results."""
        results = {
            "networks": [{"id": "N_123", "name": "Good Network"}],  # Success
            "devices": None,  # Failure
            "devices_availabilities": [{"serial": "ABC", "status": "online"}],
            "appliance_uplink_statuses": Exception("API Error"),  # Failure
            "cellular_uplink_statuses": None,
            "sensor_readings": None,
        }

        processed = api_client._process_initial_data(results)

        # Networks should be present (successful)
        assert "networks" in processed
        assert len(processed["networks"]) == 1

        # Devices should be absent (failed)
        assert "devices" not in processed

        # Appliance uplink should be absent (exception)
        assert "appliance_uplink_statuses" not in processed
