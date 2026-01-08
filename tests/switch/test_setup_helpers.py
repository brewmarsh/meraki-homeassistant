"""Tests for the switch setup_helpers module."""

from unittest.mock import MagicMock

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import CONF_ENABLE_VLAN_MANAGEMENT
from custom_components.meraki_ha.switch.setup_helpers import (
    _setup_ap_led_switches,
    _setup_camera_switches,
    _setup_mt40_switches,
    _setup_ssid_switches,
    _setup_vlan_switches,
    async_setup_switches,
)


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "devices": [],
        "networks": [],
        "ssids": [],
        "vlans": {},
    }
    coordinator.api = MagicMock()
    return coordinator


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Create a mock config entry."""
    entry = MagicMock()
    entry.options = {}
    return entry


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock hass instance."""
    return MagicMock(spec=HomeAssistant)


@pytest.fixture
def mock_meraki_client() -> MagicMock:
    """Create a mock Meraki API client."""
    return MagicMock()


class TestSetupVlanSwitches:
    """Tests for _setup_vlan_switches function."""

    def test_vlan_management_disabled(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test no switches created when VLAN management disabled."""
        mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: False}
        added: set[str] = set()

        result = _setup_vlan_switches(mock_config_entry, mock_coordinator, added)

        assert result == []

    def test_vlan_management_enabled_with_vlans(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test switches created for VLANs when enabled."""
        mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: True}
        mock_coordinator.data = {
            "vlans": {
                "N_123": [
                    {"id": 1, "name": "VLAN 1", "dhcpHandling": "Run a DHCP server"},
                    {"id": 2, "name": "VLAN 2", "dhcpHandling": "Run a DHCP server"},
                ]
            }
        }
        added: set[str] = set()

        result = _setup_vlan_switches(mock_config_entry, mock_coordinator, added)

        assert len(result) == 2
        assert "meraki_vlan_N_123_1_dhcp" in added
        assert "meraki_vlan_N_123_2_dhcp" in added

    def test_vlan_without_id_skipped(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test VLANs without ID are skipped."""
        mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: True}
        mock_coordinator.data = {
            "vlans": {
                "N_123": [{"name": "VLAN without ID", "dhcpHandling": "Run a DHCP"}]
            }
        }
        added: set[str] = set()

        result = _setup_vlan_switches(mock_config_entry, mock_coordinator, added)

        assert result == []

    def test_non_list_vlans_skipped(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test non-list VLANs data is skipped."""
        mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: True}
        mock_coordinator.data = {"vlans": {"N_123": "not a list"}}
        added: set[str] = set()

        result = _setup_vlan_switches(mock_config_entry, mock_coordinator, added)

        assert result == []

    def test_duplicate_vlan_not_added(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test duplicate VLANs are not added twice."""
        mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: True}
        mock_coordinator.data = {"vlans": {"N_123": [{"id": 1, "name": "VLAN 1"}]}}
        added = {"meraki_vlan_N_123_1_dhcp"}

        result = _setup_vlan_switches(mock_config_entry, mock_coordinator, added)

        assert result == []


class TestSetupSsidSwitches:
    """Tests for _setup_ssid_switches function."""

    def test_ssid_switches_created(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test SSID switches are created."""
        mock_coordinator.data = {
            "ssids": [
                {"networkId": "N_123", "number": 0, "name": "Corporate"},
                {"networkId": "N_123", "number": 1, "name": "Guest"},
            ]
        }
        added: set[str] = set()

        result = _setup_ssid_switches(mock_config_entry, mock_coordinator, added)

        # 2 SSIDs * 2 switches (enabled + broadcast) = 4
        assert len(result) == 4
        assert "ssid-N_123-0-enabled-switch" in added
        assert "ssid-N_123-0-broadcast-switch" in added
        assert "ssid-N_123-1-enabled-switch" in added
        assert "ssid-N_123-1-broadcast-switch" in added

    def test_ssid_without_number_skipped(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test SSIDs without number are skipped."""
        mock_coordinator.data = {"ssids": [{"networkId": "N_123", "name": "No number"}]}
        added: set[str] = set()

        result = _setup_ssid_switches(mock_config_entry, mock_coordinator, added)

        assert result == []

    def test_duplicate_ssid_not_added(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test duplicate SSIDs are not added twice."""
        mock_coordinator.data = {
            "ssids": [{"networkId": "N_123", "number": 0, "name": "Corporate"}]
        }
        added = {"ssid-N_123-0-enabled-switch", "ssid-N_123-0-broadcast-switch"}

        result = _setup_ssid_switches(mock_config_entry, mock_coordinator, added)

        assert result == []


class TestSetupCameraSwitches:
    """Tests for _setup_camera_switches function."""

    def test_camera_switches_created(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test camera switches are created."""
        mock_coordinator.data = {
            "devices": [
                {"serial": "CAM-1234", "productType": "camera", "model": "MV12W"},
            ]
        }
        added: set[str] = set()

        result = _setup_camera_switches(mock_config_entry, mock_coordinator, added)

        assert len(result) == 1
        assert "CAM-1234_analytics_switch" in added

    def test_non_camera_devices_skipped(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test non-camera devices are skipped."""
        mock_coordinator.data = {
            "devices": [
                {"serial": "SW-1234", "productType": "switch", "model": "MS225"},
            ]
        }
        added: set[str] = set()

        result = _setup_camera_switches(mock_config_entry, mock_coordinator, added)

        assert result == []

    def test_duplicate_camera_not_added(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test duplicate cameras are not added twice."""
        mock_coordinator.data = {
            "devices": [{"serial": "CAM-1234", "productType": "camera"}]
        }
        added = {"CAM-1234_analytics_switch"}

        result = _setup_camera_switches(mock_config_entry, mock_coordinator, added)

        assert result == []


class TestSetupMt40Switches:
    """Tests for _setup_mt40_switches function."""

    def test_mt40_switches_created(
        self,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
        mock_meraki_client: MagicMock,
    ) -> None:
        """Test MT40 switches are created."""
        mock_coordinator.data = {
            "devices": [
                {"serial": "MT-1234", "model": "MT40", "name": "Smart Outlet"},
            ]
        }
        added: set[str] = set()

        result = _setup_mt40_switches(
            mock_config_entry, mock_coordinator, added, mock_meraki_client
        )

        assert len(result) == 1
        assert "MT-1234_outlet_switch" in added

    def test_non_mt40_devices_skipped(
        self,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
        mock_meraki_client: MagicMock,
    ) -> None:
        """Test non-MT40 devices are skipped."""
        mock_coordinator.data = {
            "devices": [
                {"serial": "MT-1234", "model": "MT10", "name": "Temp Sensor"},
            ]
        }
        added: set[str] = set()

        result = _setup_mt40_switches(
            mock_config_entry, mock_coordinator, added, mock_meraki_client
        )

        assert result == []

    def test_duplicate_mt40_not_added(
        self,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
        mock_meraki_client: MagicMock,
    ) -> None:
        """Test duplicate MT40s are not added twice."""
        mock_coordinator.data = {"devices": [{"serial": "MT-1234", "model": "MT40"}]}
        added = {"MT-1234_outlet_switch"}

        result = _setup_mt40_switches(
            mock_config_entry, mock_coordinator, added, mock_meraki_client
        )

        assert result == []


class TestSetupApLedSwitches:
    """Tests for _setup_ap_led_switches function."""

    def test_ap_led_switches_created(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test AP LED switches are created for wireless networks."""
        mock_coordinator.data = {
            "networks": [
                {"id": "N_123", "name": "Main", "productTypes": ["wireless"]},
            ]
        }
        added: set[str] = set()

        result = _setup_ap_led_switches(mock_config_entry, mock_coordinator, added)

        assert len(result) == 1
        assert "meraki_N_123_ap_leds" in added

    def test_non_wireless_networks_skipped(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test non-wireless networks are skipped."""
        mock_coordinator.data = {
            "networks": [
                {"id": "N_123", "name": "Switches", "productTypes": ["switch"]},
            ]
        }
        added: set[str] = set()

        result = _setup_ap_led_switches(mock_config_entry, mock_coordinator, added)

        assert result == []

    def test_duplicate_network_not_added(
        self, mock_config_entry: MagicMock, mock_coordinator: MagicMock
    ) -> None:
        """Test duplicate networks are not added twice."""
        mock_coordinator.data = {
            "networks": [{"id": "N_123", "name": "Main", "productTypes": ["wireless"]}]
        }
        added = {"meraki_N_123_ap_leds"}

        result = _setup_ap_led_switches(mock_config_entry, mock_coordinator, added)

        assert result == []


class TestAsyncSetupSwitches:
    """Tests for async_setup_switches function."""

    def test_no_coordinator_data(
        self,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
        mock_meraki_client: MagicMock,
    ) -> None:
        """Test no switches created when coordinator has no data."""
        mock_coordinator.data = None

        result = async_setup_switches(
            mock_hass, mock_config_entry, mock_coordinator, mock_meraki_client
        )

        assert result == []

    def test_all_switch_types_setup(
        self,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
        mock_meraki_client: MagicMock,
    ) -> None:
        """Test all switch types are set up."""
        mock_config_entry.options = {CONF_ENABLE_VLAN_MANAGEMENT: True}
        mock_coordinator.data = {
            "devices": [
                {"serial": "CAM-1234", "productType": "camera", "model": "MV12W"},
                {"serial": "MT-1234", "model": "MT40", "name": "Outlet"},
            ],
            "networks": [
                {"id": "N_123", "name": "Main", "productTypes": ["wireless"]},
            ],
            "ssids": [
                {"networkId": "N_123", "number": 0, "name": "Corporate"},
            ],
            "vlans": {"N_123": [{"id": 1, "name": "VLAN 1"}]},
        }

        result = async_setup_switches(
            mock_hass, mock_config_entry, mock_coordinator, mock_meraki_client
        )

        # 1 VLAN + 2 SSID (enabled+broadcast) + 1 camera + 1 MT40 + 1 AP LED = 6
        assert len(result) == 6
