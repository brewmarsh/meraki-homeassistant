"""Tests for Meraki client sensor entities.

These tests verify that client sensor entities correctly extract data
from the Meraki API and link to appropriate devices.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock, patch

import pytest

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.sensor.client import (
    MerakiClientConnectedDeviceSensor,
    MerakiClientConnectionTypeSensor,
    MerakiClientReceivedBytesSensor,
    MerakiClientSentBytesSensor,
    MerakiClientSSIDSensor,
    MerakiClientVLANSensor,
)

if TYPE_CHECKING:
    pass


# Sample client data for testing
MOCK_CLIENT_DATA: dict[str, Any] = {
    "id": "k12345",
    "mac": "aa:bb:cc:dd:ee:ff",
    "description": "Test Client",
    "ip": "192.168.1.100",
    "ip6": None,
    "vlan": 10,
    "ssid": "TestNetwork",
    "switchport": None,
    "manufacturer": "Apple",
    "os": "macOS",
    "user": None,
    "dhcpHostname": "test-client",
    "recentDeviceName": "Office-AP1",
    "recentDeviceSerial": "QXYZ-1234-ABCD",
    "recentDeviceMac": "11:22:33:44:55:66",
    "firstSeen": "2022-01-01T00:00:00Z",
    "lastSeen": "2024-01-01T12:00:00Z",
    "usage": {"sent": 1024000, "recv": 2048000},
    "networkId": "N_12345",
}

MOCK_WIRED_CLIENT_DATA: dict[str, Any] = {
    **MOCK_CLIENT_DATA,
    "mac": "11:22:33:44:55:66",
    "ssid": None,
    "switchport": "7",
    "description": "Wired Client",
}


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock HomeAssistant instance."""
    hass = MagicMock()
    hass.data = {}
    return hass


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "clients": [MOCK_CLIENT_DATA, MOCK_WIRED_CLIENT_DATA],
        "devices": [],
    }
    coordinator.async_add_listener = MagicMock(return_value=lambda: None)
    return coordinator


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry"
    entry.options = {}
    return entry


class TestMerakiClientVLANSensor:
    """Tests for the VLAN sensor."""

    def test_init(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test sensor initialization."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientVLANSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        assert sensor.unique_id == f"meraki_client_{MOCK_CLIENT_DATA['mac']}_vlan"
        assert sensor.name == "VLAN"
        assert sensor.icon == "mdi:lan"

    def test_native_value(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that native_value returns the VLAN ID."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientVLANSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        assert sensor.native_value == 10

    def test_device_info_new_client(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test device_info when client is new (not linked to existing device)."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientVLANSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        assert sensor.device_info is not None
        assert (DOMAIN, f"client_{MOCK_CLIENT_DATA['mac']}") in sensor.device_info[
            "identifiers"
        ]
        assert sensor.device_info["via_device"] == (DOMAIN, "network_N_12345")


class TestMerakiClientSSIDSensor:
    """Tests for the SSID sensor."""

    def test_native_value_wireless(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that native_value returns the SSID for wireless clients."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientSSIDSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        assert sensor.native_value == "TestNetwork"

    def test_native_value_wired(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that native_value returns None for wired clients."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientSSIDSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_WIRED_CLIENT_DATA,
            )

        assert sensor.native_value is None


class TestMerakiClientConnectedDeviceSensor:
    """Tests for the connected device sensor."""

    def test_native_value(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that native_value returns the connected device name."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientConnectedDeviceSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        assert sensor.native_value == "Office-AP1"

    def test_extra_state_attributes(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test extra state attributes include device serial and MAC."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientConnectedDeviceSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        attrs = sensor.extra_state_attributes
        assert attrs["device_name"] == "Office-AP1"
        assert attrs["device_serial"] == "QXYZ-1234-ABCD"
        assert attrs["device_mac"] == "11:22:33:44:55:66"


class TestMerakiClientConnectionTypeSensor:
    """Tests for the connection type sensor."""

    def test_wireless_connection(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that connection type is 'wireless' for clients with SSID."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientConnectionTypeSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        assert sensor.native_value == "wireless"
        assert sensor.icon == "mdi:wifi"

    def test_wired_connection(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that connection type is 'wired' for clients with switchport."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientConnectionTypeSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_WIRED_CLIENT_DATA,
            )

        assert sensor.native_value == "wired"
        assert sensor.icon == "mdi:ethernet"


class TestMerakiClientDataUsageSensors:
    """Tests for the data usage sensors."""

    def test_sent_bytes(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that sent bytes sensor returns correct value."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientSentBytesSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        assert sensor.native_value == 1024000
        assert sensor.name == "Sent"
        assert sensor.icon == "mdi:upload"

    def test_received_bytes(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that received bytes sensor returns correct value."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientReceivedBytesSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        assert sensor.native_value == 2048000
        assert sensor.name == "Received"
        assert sensor.icon == "mdi:download"


class TestMerakiClientSensorDeviceLinking:
    """Tests for device linking functionality."""

    def test_links_to_existing_device(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that sensor links to existing device when MAC matches."""
        # Create a mock existing device
        mock_device = MagicMock()
        mock_device.identifiers = {("sonos", "RINCON_12345")}
        mock_device.name = "Living Room Speaker"

        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=mock_device,
        ):
            sensor = MerakiClientVLANSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        # Should use the existing device's identifiers
        assert sensor.device_info is not None
        assert sensor.device_info["identifiers"] == mock_device.identifiers

    def test_coordinator_update(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that sensor updates from coordinator data."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientVLANSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        # Update coordinator data with new VLAN
        updated_client_data = {**MOCK_CLIENT_DATA, "vlan": 20}
        mock_coordinator.data = {"clients": [updated_client_data], "devices": []}

        # Mock async_write_ha_state since we're not in a real HA context
        with patch.object(sensor, "async_write_ha_state"):
            # Trigger update
            sensor._handle_coordinator_update()

        # Verify the cached data was updated
        assert sensor._cached_client_data["vlan"] == 20
        assert sensor.native_value == 20

    def test_availability_when_connected(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that sensor is available when client is in coordinator data."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientVLANSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        assert sensor.available is True

    def test_availability_when_disconnected(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that sensor is unavailable when client is not in coordinator data."""
        with patch(
            "custom_components.meraki_ha.sensor.client.base._find_existing_device_by_mac",
            return_value=None,
        ):
            sensor = MerakiClientVLANSensor(
                hass=mock_hass,
                coordinator=mock_coordinator,
                config_entry=mock_config_entry,
                client_data=MOCK_CLIENT_DATA,
            )

        # Remove client from coordinator data
        mock_coordinator.data = {"clients": [], "devices": []}

        assert sensor.available is False
