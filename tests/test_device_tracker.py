"""Tests for the Meraki device_tracker platform."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from homeassistant.components.device_tracker import SourceType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.meraki_ha.const import CONF_ENABLE_DEVICE_TRACKER, DOMAIN
from custom_components.meraki_ha.device_tracker import (
    MerakiClientDeviceTracker,
    async_setup_entry,
)

# Sample client data for testing
MOCK_CLIENT_DATA = {
    "id": "client123",
    "mac": "00:11:22:33:44:55",
    "ip": "192.168.1.100",
    "ip6": "fe80::1",
    "description": "Test Laptop",
    "dhcpHostname": "test-laptop",
    "manufacturer": "Apple Inc.",
    "os": "macOS",
    "user": "testuser",
    "firstSeen": "2024-01-01T00:00:00Z",
    "lastSeen": "2024-01-15T12:00:00Z",
    "recentDeviceSerial": "Q234-ABCD-5678",
    "recentDeviceName": "Main Access Point",
    "recentDeviceMac": "AA:BB:CC:DD:EE:00",
    "ssid": "Office WiFi",
    "vlan": 100,
    "switchport": None,
    "status": "Online",
    "usage": {"sent": 1000000, "recv": 5000000},
    "networkId": "N_12345",
    "groupPolicy8021x": "Employee",
    "policyId": "101",
}

MOCK_CLIENT_DATA_OFFLINE = {
    "id": "client456",
    "mac": "AA:BB:CC:DD:EE:FF",
    "ip": "192.168.1.101",
    "description": "Guest Phone",
    "manufacturer": "Samsung",
    "status": "Offline",
    "recentDeviceSerial": "Q234-ABCD-5678",
}

MOCK_CLIENT_DATA_NO_PARENT = {
    "id": "client999",
    "mac": "FF:EE:DD:CC:BB:AA",
    "ip": "192.168.1.200",
    "description": "Unknown Device",
    "status": "Online",
    # No recentDeviceSerial - should be skipped
}

MOCK_CLIENT_DATA_WIRED = {
    "id": "client789",
    "mac": "11:22:33:44:55:66",
    "ip": "192.168.1.102",
    "description": "Desktop PC",
    "manufacturer": "Dell",
    "recentDeviceSerial": "Q234-ABCD-SW01",
    "recentDeviceName": "Main Switch",
    "recentDeviceMac": "BB:CC:DD:EE:FF:00",
    "switchport": "3",
    "vlan": 200,
    "status": "Online",
    "networkId": "N_12345",
}


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Fixture for a mocked MerakiDataCoordinator."""
    coordinator = MagicMock(spec=DataUpdateCoordinator)
    coordinator.data = {
        "clients": [MOCK_CLIENT_DATA],
        "devices": [],
        "networks": [],
    }
    coordinator.async_add_listener = MagicMock(return_value=lambda: None)
    return coordinator


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Fixture for a mocked ConfigEntry."""
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = "test_entry_id"
    entry.options = {CONF_ENABLE_DEVICE_TRACKER: True}
    entry.async_on_unload = MagicMock()
    return entry


@pytest.fixture
def mock_hass(mock_coordinator: MagicMock, mock_config_entry: MagicMock) -> MagicMock:
    """Fixture for a mocked HomeAssistant instance."""
    hass = MagicMock(spec=HomeAssistant)
    hass.data = {
        DOMAIN: {
            mock_config_entry.entry_id: {
                "coordinator": mock_coordinator,
            }
        }
    }
    return hass


class TestMerakiClientDeviceTracker:
    """Tests for the MerakiClientDeviceTracker entity."""

    def test_init_basic(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test basic initialization of the device tracker."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        assert tracker._client_mac == "00:11:22:33:44:55"
        assert tracker._attr_unique_id == "meraki_client_00:11:22:33:44:55"
        assert tracker._attr_name == "Test Laptop"
        assert tracker._attr_has_entity_name is True

    def test_init_uses_dhcp_hostname_fallback(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that dhcpHostname is used when description is missing."""
        client_data = {
            "mac": "11:22:33:44:55:66",
            "dhcpHostname": "my-device",
            "ip": "192.168.1.50",
        }
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=client_data,
        )

        assert tracker._attr_name == "my-device"

    def test_init_uses_ip_fallback(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that IP is used when description and hostname are missing."""
        client_data = {
            "mac": "11:22:33:44:55:66",
            "ip": "192.168.1.50",
        }
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=client_data,
        )

        assert tracker._attr_name == "192.168.1.50"

    def test_init_uses_mac_fallback(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that MAC is used when all other identifiers are missing."""
        client_data = {
            "mac": "11:22:33:44:55:66",
        }
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=client_data,
        )

        assert tracker._attr_name == "11:22:33:44:55:66"

    def test_source_type(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that source type is ROUTER."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        assert tracker.source_type == SourceType.ROUTER

    def test_is_connected_when_online(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test is_connected returns True when client is in clients list."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        # Client is in the clients list
        mock_coordinator.data = {"clients": [MOCK_CLIENT_DATA]}

        assert tracker.is_connected is True

    def test_is_connected_when_present_no_status(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test is_connected returns True when client is present without status."""
        client_no_status = {
            "mac": "00:11:22:33:44:55",
            "ip": "192.168.1.100",
        }
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=client_no_status,
        )

        mock_coordinator.data = {"clients": [client_no_status]}

        assert tracker.is_connected is True

    def test_is_connected_when_not_in_clients(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test is_connected returns False when client is not in clients list."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA_OFFLINE,
        )

        # Client not in the clients list (empty list)
        mock_coordinator.data = {"clients": []}

        assert tracker.is_connected is False

    def test_is_connected_when_different_client(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test is_connected returns False when client MAC not in list."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        # Different client in the list
        mock_coordinator.data = {"clients": [MOCK_CLIENT_DATA_OFFLINE]}

        assert tracker.is_connected is False

    def test_is_connected_when_no_data(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test is_connected returns False when no coordinator data."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        mock_coordinator.data = None

        assert tracker.is_connected is False

    def test_mac_address(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test mac_address property."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        assert tracker.mac_address == "00:11:22:33:44:55"

    def test_ip_address(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test ip_address property."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        assert tracker.ip_address == "192.168.1.100"

    def test_hostname(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test hostname property uses dhcpHostname first."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        assert tracker.hostname == "test-laptop"

    def test_hostname_fallback_to_description(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test hostname falls back to description."""
        client_data = {
            "mac": "00:11:22:33:44:55",
            "description": "My Device",
        }
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=client_data,
        )

        assert tracker.hostname == "My Device"

    def test_extra_state_attributes(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test extra_state_attributes property."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        attrs = tracker.extra_state_attributes

        # Network connectivity info
        assert attrs["ip6_address"] == "fe80::1"
        assert attrs["vlan"] == 100
        assert attrs["ssid"] == "Office WiFi"
        assert attrs["connection_type"] == "wireless"

        # Client identification
        assert attrs["manufacturer"] == "Apple Inc."
        assert attrs["os"] == "macOS"
        assert attrs["user"] == "testuser"

        # Connection info - device the client is connected to
        assert attrs["connected_to_device"] == "Main Access Point"
        assert attrs["connected_to_serial"] == "Q234-ABCD-5678"
        assert attrs["connected_to_mac"] == "AA:BB:CC:DD:EE:00"

        # Group policy
        assert attrs["group_policy"] == "Employee"
        assert attrs["policy_id"] == "101"

        # Timestamps
        assert attrs["first_seen"] == "2024-01-01T00:00:00Z"
        assert attrs["last_seen"] == "2024-01-15T12:00:00Z"

        # Usage stats
        assert attrs["sent_bytes"] == 1000000
        assert attrs["received_bytes"] == 5000000

        # Network ID
        assert attrs["network_id"] == "N_12345"

    def test_extra_state_attributes_wired_client(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test extra_state_attributes for a wired client."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA_WIRED,
        )

        attrs = tracker.extra_state_attributes

        # Wired connection info
        assert attrs["switchport"] == "3"
        assert attrs["connection_type"] == "wired"
        assert attrs["vlan"] == 200
        assert "ssid" not in attrs  # No SSID for wired clients

        # Connection info
        assert attrs["connected_to_device"] == "Main Switch"
        assert attrs["connected_to_serial"] == "Q234-ABCD-SW01"
        assert attrs["connected_to_mac"] == "BB:CC:DD:EE:FF:00"

    def test_extra_state_attributes_minimal(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test extra_state_attributes with minimal client data."""
        client_data = {
            "mac": "00:11:22:33:44:55",
        }
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=client_data,
        )

        attrs = tracker.extra_state_attributes
        # Minimal client data has empty attributes
        assert attrs == {}

    def test_device_info_with_network(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test device_info links to Clients group under network.

        Device Hierarchy: Organization → Network → Clients Group → Client
        """
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        device_info = tracker._attr_device_info
        assert device_info is not None
        assert (DOMAIN, "client_00:11:22:33:44:55") in device_info["identifiers"]
        assert device_info["name"] == "Test Laptop"
        assert device_info["manufacturer"] == "Apple Inc."
        # Clients are linked to their Clients group (under network)
        assert device_info["via_device"] == (DOMAIN, "devicetype_N_12345_clients")

    def test_device_info_without_parent(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test device_info has no via_device when networkId missing."""
        client_data = {
            "mac": "00:11:22:33:44:55",
            "description": "Test Device",
            "manufacturer": "Test Manufacturer",
        }
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=client_data,
        )

        device_info = tracker._attr_device_info
        assert device_info is not None
        # via_device is not present when recentDeviceSerial is missing
        assert "via_device" not in device_info

    def test_handle_coordinator_update(
        self,
        mock_hass: MagicMock,
        mock_coordinator: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test _handle_coordinator_update updates cached data."""
        tracker = MerakiClientDeviceTracker(
            hass=mock_hass,
            coordinator=mock_coordinator,
            config_entry=mock_config_entry,
            client_data=MOCK_CLIENT_DATA,
        )

        # Update with new data via clients list
        updated_client = {**MOCK_CLIENT_DATA, "ip": "192.168.1.200"}
        mock_coordinator.data = {"clients": [updated_client]}

        # Mock async_write_ha_state
        tracker.async_write_ha_state = MagicMock()

        tracker._handle_coordinator_update()

        # Check cached data was updated
        assert tracker._cached_client_data["ip"] == "192.168.1.200"
        tracker.async_write_ha_state.assert_called_once()


class TestAsyncSetupEntry:
    """Tests for the async_setup_entry function."""

    async def test_setup_disabled(
        self,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test setup is skipped when device tracker is disabled."""
        mock_config_entry.options = {CONF_ENABLE_DEVICE_TRACKER: False}
        async_add_entities = MagicMock()

        await async_setup_entry(mock_hass, mock_config_entry, async_add_entities)

        async_add_entities.assert_not_called()

    async def test_setup_adds_clients(
        self,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test setup adds device trackers for clients."""
        mock_coordinator.data = {
            "clients": [MOCK_CLIENT_DATA, MOCK_CLIENT_DATA_OFFLINE]
        }
        async_add_entities = MagicMock()

        await async_setup_entry(mock_hass, mock_config_entry, async_add_entities)

        # Should add 2 entities
        async_add_entities.assert_called_once()
        entities = async_add_entities.call_args[0][0]
        assert len(entities) == 2
        assert all(isinstance(e, MerakiClientDeviceTracker) for e in entities)

    async def test_setup_skips_clients_without_mac(
        self,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test setup skips clients without MAC address."""
        mock_coordinator.data = {
            "clients": [
                MOCK_CLIENT_DATA,
                {"id": "no_mac", "ip": "192.168.1.200"},  # No MAC
            ]
        }
        async_add_entities = MagicMock()

        await async_setup_entry(mock_hass, mock_config_entry, async_add_entities)

        # Should only add 1 entity (the one with MAC)
        async_add_entities.assert_called_once()
        entities = async_add_entities.call_args[0][0]
        assert len(entities) == 1

    async def test_setup_with_parent_device(
        self,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test setup includes via_device when client has networkId."""
        mock_coordinator.data = {"clients": [MOCK_CLIENT_DATA]}
        async_add_entities = MagicMock()

        await async_setup_entry(mock_hass, mock_config_entry, async_add_entities)

        # Should add entity with via_device linking to Clients group
        async_add_entities.assert_called_once()
        entities = async_add_entities.call_args[0][0]
        assert len(entities) == 1
        device_info = entities[0]._attr_device_info
        # Clients are linked to their Clients group (under network)
        assert device_info["via_device"] == (DOMAIN, "devicetype_N_12345_clients")

    async def test_setup_no_clients(
        self,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test setup with no clients does nothing."""
        mock_coordinator.data = {"clients": []}
        async_add_entities = MagicMock()

        await async_setup_entry(mock_hass, mock_config_entry, async_add_entities)

        # Should not call async_add_entities with entities
        # (the listener is registered but no initial entities added)
        async_add_entities.assert_not_called()

    async def test_setup_registers_listener(
        self,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
        mock_coordinator: MagicMock,
    ) -> None:
        """Test setup registers a coordinator listener for new clients."""
        mock_coordinator.data = {"clients": []}
        async_add_entities = MagicMock()

        await async_setup_entry(mock_hass, mock_config_entry, async_add_entities)

        # Should register listener
        mock_coordinator.async_add_listener.assert_called_once()
        # Should register unload handler
        mock_config_entry.async_on_unload.assert_called_once()
