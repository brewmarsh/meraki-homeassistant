"""Tests for the device association feature.

This module tests the manual device association functionality that allows
users to link Meraki network clients to existing Home Assistant devices.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from custom_components.meraki_ha.const import (
    CONF_MANUAL_CLIENT_ASSOCIATIONS,
    DOMAIN,
)
from custom_components.meraki_ha.device_tracker import (
    _find_existing_device,
    _find_existing_device_by_manual_association,
)
from custom_components.meraki_ha.options_flow import MerakiOptionsFlowHandler

# Sample client data for testing
MOCK_CLIENT_DATA = {
    "id": "client123",
    "mac": "00:11:22:33:44:55",
    "ip": "192.168.1.100",
    "description": "Ring Doorbell",
    "dhcpHostname": "ring-doorbell-1234",
    "manufacturer": "Ring",
    "networkId": "N_12345",
}


@pytest.fixture
def mock_hass() -> MagicMock:
    """Fixture for a mocked HomeAssistant instance."""
    hass = MagicMock(spec=HomeAssistant)
    return hass


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Fixture for a mocked ConfigEntry with no manual associations."""
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = "test_entry_id"
    entry.options = {}
    return entry


@pytest.fixture
def mock_config_entry_with_associations() -> MagicMock:
    """Fixture for a mocked ConfigEntry with manual associations."""
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = "test_entry_id"
    entry.options = {
        CONF_MANUAL_CLIENT_ASSOCIATIONS: {
            "00:11:22:33:44:55": "device_id_123",
            "aa:bb:cc:dd:ee:ff": "device_id_456",
        }
    }
    return entry


@pytest.fixture
def mock_device_registry() -> MagicMock:
    """Fixture for a mocked device registry."""
    registry = MagicMock(spec=dr.DeviceRegistry)

    # Create a mock device
    mock_device = MagicMock()
    mock_device.id = "device_id_123"
    mock_device.name = "Ring Integration Device"
    mock_device.manufacturer = "Ring"
    mock_device.identifiers = {("ring", "123456")}
    mock_device.connections = set()

    registry.async_get.return_value = mock_device
    registry.devices = {
        "device_id_123": mock_device,
    }

    return registry


class TestFindExistingDeviceByManualAssociation:
    """Tests for _find_existing_device_by_manual_association function."""

    def test_returns_none_when_no_config_entry(self, mock_hass: MagicMock) -> None:
        """Test that None is returned when config_entry is None."""
        result = _find_existing_device_by_manual_association(
            mock_hass, "00:11:22:33:44:55", None
        )
        assert result is None

    def test_returns_none_when_no_associations(
        self, mock_hass: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test that None is returned when no associations are configured."""
        result = _find_existing_device_by_manual_association(
            mock_hass, "00:11:22:33:44:55", mock_config_entry
        )
        assert result is None

    def test_returns_none_when_mac_not_in_associations(
        self, mock_hass: MagicMock, mock_config_entry_with_associations: MagicMock
    ) -> None:
        """Test that None is returned when MAC is not in associations."""
        result = _find_existing_device_by_manual_association(
            mock_hass, "ff:ff:ff:ff:ff:ff", mock_config_entry_with_associations
        )
        assert result is None

    @patch("custom_components.meraki_ha.device_tracker.dr.async_get")
    def test_returns_device_when_association_exists(
        self,
        mock_dr_async_get: MagicMock,
        mock_hass: MagicMock,
        mock_config_entry_with_associations: MagicMock,
        mock_device_registry: MagicMock,
    ) -> None:
        """Test that device is returned when association exists."""
        mock_dr_async_get.return_value = mock_device_registry

        result = _find_existing_device_by_manual_association(
            mock_hass, "00:11:22:33:44:55", mock_config_entry_with_associations
        )

        assert result is not None
        assert result.name == "Ring Integration Device"

    @patch("custom_components.meraki_ha.device_tracker.dr.async_get")
    def test_normalizes_mac_address(
        self,
        mock_dr_async_get: MagicMock,
        mock_hass: MagicMock,
        mock_config_entry_with_associations: MagicMock,
        mock_device_registry: MagicMock,
    ) -> None:
        """Test that MAC address is normalized for comparison."""
        mock_dr_async_get.return_value = mock_device_registry

        # Test with uppercase MAC
        result = _find_existing_device_by_manual_association(
            mock_hass, "00:11:22:33:44:55", mock_config_entry_with_associations
        )
        assert result is not None

        # Test with dash-separated MAC
        result = _find_existing_device_by_manual_association(
            mock_hass, "00-11-22-33-44-55", mock_config_entry_with_associations
        )
        assert result is not None


class TestFindExistingDevice:
    """Tests for _find_existing_device function with manual associations."""

    @patch(
        "custom_components.meraki_ha.device_tracker._find_existing_device_by_manual_association"
    )
    @patch("custom_components.meraki_ha.device_tracker._find_existing_device_by_mac")
    @patch("custom_components.meraki_ha.device_tracker._find_existing_device_by_ip")
    def test_manual_association_has_priority(
        self,
        mock_find_by_ip: MagicMock,
        mock_find_by_mac: MagicMock,
        mock_find_by_manual: MagicMock,
        mock_hass: MagicMock,
        mock_config_entry_with_associations: MagicMock,
    ) -> None:
        """Test that manual association takes priority over MAC/IP matching."""
        # Set up mock to return a device for manual association
        mock_manual_device = MagicMock()
        mock_manual_device.name = "Manual Association Device"
        mock_find_by_manual.return_value = mock_manual_device

        # Set up mocks for MAC and IP to return different devices
        mock_mac_device = MagicMock()
        mock_mac_device.name = "MAC Match Device"
        mock_find_by_mac.return_value = mock_mac_device

        mock_ip_device = MagicMock()
        mock_ip_device.name = "IP Match Device"
        mock_find_by_ip.return_value = mock_ip_device

        result = _find_existing_device(
            mock_hass,
            "00:11:22:33:44:55",
            "192.168.1.100",
            mock_config_entry_with_associations,
        )

        assert result == mock_manual_device
        mock_find_by_manual.assert_called_once()
        # MAC and IP should not be called when manual association is found
        mock_find_by_mac.assert_not_called()
        mock_find_by_ip.assert_not_called()

    @patch(
        "custom_components.meraki_ha.device_tracker._find_existing_device_by_manual_association"
    )
    @patch("custom_components.meraki_ha.device_tracker._find_existing_device_by_mac")
    @patch("custom_components.meraki_ha.device_tracker._find_existing_device_by_ip")
    def test_falls_back_to_mac_when_no_manual_association(
        self,
        mock_find_by_ip: MagicMock,
        mock_find_by_mac: MagicMock,
        mock_find_by_manual: MagicMock,
        mock_hass: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test that MAC matching is used when no manual association exists."""
        mock_find_by_manual.return_value = None

        mock_mac_device = MagicMock()
        mock_mac_device.name = "MAC Match Device"
        mock_find_by_mac.return_value = mock_mac_device

        result = _find_existing_device(
            mock_hass, "00:11:22:33:44:55", "192.168.1.100", mock_config_entry
        )

        assert result == mock_mac_device
        mock_find_by_manual.assert_called_once()
        mock_find_by_mac.assert_called_once()
        mock_find_by_ip.assert_not_called()


class TestDeviceAssociationOptionsFlow:
    """Tests for the device association options flow step."""

    def _create_options_flow_handler(
        self,
        options: dict[str, Any] | None = None,
        clients: list[dict[str, Any]] | None = None,
    ) -> MerakiOptionsFlowHandler:
        """Create an options flow handler with mocked dependencies."""
        if options is None:
            options = {}
        if clients is None:
            clients = [MOCK_CLIENT_DATA]

        handler = MerakiOptionsFlowHandler()

        # Create mock config entry
        mock_entry = MagicMock()
        mock_entry.entry_id = "test_entry_id"
        mock_entry.options = options

        # Set up hass mock
        hass = MagicMock()
        mock_coordinator = MagicMock()
        mock_coordinator.data = {
            "clients": clients,
            "networks": [],
        }
        hass.data = {
            DOMAIN: {
                "test_entry_id": {
                    "coordinator": mock_coordinator,
                }
            }
        }
        hass.config_entries.async_get_known_entry.return_value = mock_entry

        # Mock device registry
        mock_device = MagicMock()
        mock_device.id = "device_id_123"
        mock_device.name = "Ring Doorbell"
        mock_device.manufacturer = "Ring"
        mock_device.identifiers = {("ring", "123456")}

        mock_device_registry = MagicMock()
        mock_device_registry.devices = MagicMock()
        mock_device_registry.devices.values.return_value = [mock_device]
        mock_device_registry.async_get.return_value = mock_device

        handler.hass = hass
        handler._options = options
        handler._options_initialized = True

        # Set the handler property (this is what the framework sets - it's the entry ID)
        handler.handler = "test_entry_id"

        # Mock the config_entry property to return our mock
        handler._config_entry = mock_entry  # type: ignore[attr-defined]

        return handler

    @pytest.mark.asyncio
    async def test_device_association_menu_shows_add_option(self) -> None:
        """Test that device association menu shows add option."""
        handler = self._create_options_flow_handler()

        with patch("homeassistant.helpers.device_registry.async_get") as mock_dr:
            mock_device_registry = MagicMock()
            mock_device_registry.devices = MagicMock()
            mock_device_registry.devices.values.return_value = []
            mock_device_registry.async_get.return_value = None
            mock_dr.return_value = mock_device_registry

            result = await handler.async_step_device_association()

            assert result["type"] == "form"
            assert result["step_id"] == "device_association"
            assert result["data_schema"] is not None
            assert "action" in result["data_schema"].schema

    @pytest.mark.asyncio
    async def test_device_association_shows_remove_when_associations_exist(
        self,
    ) -> None:
        """Test that remove option appears when associations exist."""
        options = {
            CONF_MANUAL_CLIENT_ASSOCIATIONS: {
                "00:11:22:33:44:55": "device_id_123",
            }
        }
        handler = self._create_options_flow_handler(options=options)

        with patch("homeassistant.helpers.device_registry.async_get") as mock_dr:
            mock_device = MagicMock()
            mock_device.id = "device_id_123"
            mock_device.name = "Ring Doorbell"

            mock_device_registry = MagicMock()
            mock_device_registry.async_get.return_value = mock_device
            mock_dr.return_value = mock_device_registry

            result = await handler.async_step_device_association()

            assert result["type"] == "form"
            placeholders = result.get("description_placeholders", {})
            assert placeholders is not None
            assert "1" in str(placeholders.get("association_count", ""))

    @pytest.mark.asyncio
    async def test_select_client_shows_available_clients(self) -> None:
        """Test that select_client step shows available clients."""
        handler = self._create_options_flow_handler()

        result = await handler.async_step_select_client()

        assert result["type"] == "form"
        assert result["step_id"] == "select_client"
        assert result["data_schema"] is not None
        assert "client" in result["data_schema"].schema

    @pytest.mark.asyncio
    async def test_select_client_stores_selection_and_proceeds(self) -> None:
        """Test that selecting a client proceeds to device selection."""
        handler = self._create_options_flow_handler()

        with patch.object(handler, "async_step_select_device") as mock_select_device:
            mock_select_device.return_value = {"type": "form"}

            await handler.async_step_select_client(
                user_input={"client": "00:11:22:33:44:55"}
            )

            assert handler._selected_client_mac == "00:11:22:33:44:55"
            mock_select_device.assert_called_once()

    @pytest.mark.asyncio
    async def test_select_device_saves_association(self) -> None:
        """Test that selecting a device saves the association."""
        handler = self._create_options_flow_handler()
        handler._selected_client_mac = "00:11:22:33:44:55"

        with patch("homeassistant.helpers.device_registry.async_get") as mock_dr:
            mock_device = MagicMock()
            mock_device.id = "device_id_123"
            mock_device.name = "Ring Doorbell"
            mock_device.manufacturer = "Ring"
            mock_device.identifiers = {("ring", "123456")}

            mock_device_registry = MagicMock()
            mock_device_registry.devices = MagicMock()
            mock_device_registry.devices.values.return_value = [mock_device]
            mock_device_registry.async_get.return_value = mock_device
            mock_dr.return_value = mock_device_registry

            await handler.async_step_select_device(
                user_input={"device": "device_id_123"}
            )

            # Verify the association was saved
            associations = handler.options.get(CONF_MANUAL_CLIENT_ASSOCIATIONS, {})
            assert "00:11:22:33:44:55" in associations
            assert associations["00:11:22:33:44:55"] == "device_id_123"

    @pytest.mark.asyncio
    async def test_remove_association_deletes_association(self) -> None:
        """Test that remove_association step deletes selected associations."""
        options = {
            CONF_MANUAL_CLIENT_ASSOCIATIONS: {
                "00:11:22:33:44:55": "device_id_123",
                "aa:bb:cc:dd:ee:ff": "device_id_456",
            }
        }
        handler = self._create_options_flow_handler(options=options)

        with patch("homeassistant.helpers.device_registry.async_get") as mock_dr:
            mock_device = MagicMock()
            mock_device.name = "Test Device"
            mock_device_registry = MagicMock()
            mock_device_registry.async_get.return_value = mock_device
            mock_dr.return_value = mock_device_registry

            await handler.async_step_remove_association(
                user_input={"associations": ["00:11:22:33:44:55"]}
            )

            # Verify the association was removed
            associations = handler.options.get(CONF_MANUAL_CLIENT_ASSOCIATIONS, {})
            assert "00:11:22:33:44:55" not in associations
            assert "aa:bb:cc:dd:ee:ff" in associations
