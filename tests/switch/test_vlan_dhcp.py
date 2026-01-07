"""Tests for the VLAN DHCP switch module."""

from typing import cast
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.switch.vlan_dhcp import MerakiVLANDHCPSwitch
from custom_components.meraki_ha.types import MerakiVlan

MOCK_VLAN: MerakiVlan = cast(
    MerakiVlan,
    {
        "id": 100,
        "name": "Test VLAN",
        "dhcpHandling": "Run a DHCP server",
        "subnet": "192.168.100.0/24",
    },
)


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Create a mock coordinator."""
    coordinator = MagicMock()
    coordinator.data = {
        "vlans": {"N_123": [MOCK_VLAN]},
        "networks": [{"id": "N_123", "name": "Test Network"}],
    }
    coordinator.api = MagicMock()
    coordinator.api.appliance = MagicMock()
    coordinator.api.appliance.update_network_vlan = AsyncMock()
    coordinator.is_pending = MagicMock(return_value=False)
    coordinator.register_pending_update = MagicMock()
    coordinator.config_entry = MagicMock()
    coordinator.config_entry.options = {}
    return coordinator


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.options = {}
    return entry


class TestMerakiVLANDHCPSwitch:
    """Tests for MerakiVLANDHCPSwitch class."""

    def test_initialization(
        self, mock_coordinator: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test VLAN DHCP switch initialization."""
        switch = MerakiVLANDHCPSwitch(
            mock_coordinator, mock_config_entry, "N_123", MOCK_VLAN
        )

        assert switch._network_id == "N_123"
        assert switch._vlan == MOCK_VLAN
        assert switch._attr_name == "DHCP"
        assert switch.unique_id is not None and "dhcp_handling" in switch.unique_id

    def test_initialization_missing_network_id(
        self, mock_coordinator: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test initialization raises error when network ID is missing."""
        with pytest.raises(ValueError, match="Network ID cannot be None"):
            MerakiVLANDHCPSwitch(
                mock_coordinator,
                mock_config_entry,
                None,  # type: ignore[arg-type]
                MOCK_VLAN,
            )

    def test_initialization_missing_vlan_id(
        self, mock_coordinator: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test initialization raises error when VLAN ID is missing."""
        vlan_no_id = cast(MerakiVlan, {"name": "No ID VLAN"})

        # The parent class (MerakiVLANEntity) or the switch class should raise
        # an error when VLAN ID is missing
        with pytest.raises((ValueError, KeyError)):
            MerakiVLANDHCPSwitch(
                mock_coordinator, mock_config_entry, "N_123", vlan_no_id
            )

    def test_is_on_when_dhcp_enabled(
        self, mock_coordinator: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test is_on is True when DHCP is enabled."""
        switch = MerakiVLANDHCPSwitch(
            mock_coordinator, mock_config_entry, "N_123", MOCK_VLAN
        )

        assert switch.is_on is True

    def test_is_on_when_dhcp_disabled(
        self, mock_coordinator: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test is_on is False when DHCP is disabled."""
        vlan_dhcp_off: MerakiVlan = cast(
            MerakiVlan,
            {
                "id": 100,
                "name": "Test VLAN",
                "dhcpHandling": "Do not respond to DHCP requests",
            },
        )

        switch = MerakiVLANDHCPSwitch(
            mock_coordinator, mock_config_entry, "N_123", vlan_dhcp_off
        )

        assert switch.is_on is False

    def test_update_internal_state_skips_pending(
        self, mock_coordinator: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test _update_internal_state skips when pending update."""
        mock_coordinator.is_pending.return_value = True

        vlan_dhcp_off: MerakiVlan = cast(
            MerakiVlan,
            {
                "id": 100,
                "name": "Test VLAN",
                "dhcpHandling": "Do not respond to DHCP requests",
            },
        )

        switch = MerakiVLANDHCPSwitch(
            mock_coordinator, mock_config_entry, "N_123", MOCK_VLAN
        )
        switch._attr_is_on = True

        # Change VLAN data and try to update
        switch._vlan = vlan_dhcp_off
        switch._update_internal_state()

        # Should still be True because update was skipped
        assert switch._attr_is_on is True

    def test_handle_coordinator_update(
        self, mock_coordinator: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test _handle_coordinator_update updates VLAN data."""
        switch = MerakiVLANDHCPSwitch(
            mock_coordinator, mock_config_entry, "N_123", MOCK_VLAN
        )
        switch.async_write_ha_state = MagicMock()

        # Update coordinator data with new DHCP setting
        updated_vlan = dict(MOCK_VLAN)
        updated_vlan["dhcpHandling"] = "Do not respond to DHCP requests"
        mock_coordinator.data = {"vlans": {"N_123": [updated_vlan]}}

        switch._handle_coordinator_update()

        assert switch._vlan["dhcpHandling"] == "Do not respond to DHCP requests"  # type: ignore[typeddict-item]
        assert switch.is_on is False
        switch.async_write_ha_state.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_turn_on(
        self, mock_coordinator: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test async_turn_on enables DHCP."""
        vlan_dhcp_off: MerakiVlan = cast(
            MerakiVlan,
            {
                "id": 100,
                "name": "Test VLAN",
                "dhcpHandling": "Do not respond to DHCP requests",
            },
        )

        switch = MerakiVLANDHCPSwitch(
            mock_coordinator, mock_config_entry, "N_123", vlan_dhcp_off
        )
        switch.async_write_ha_state = MagicMock()

        await switch.async_turn_on()

        assert switch._attr_is_on is True
        switch.async_write_ha_state.assert_called_once()
        mock_coordinator.register_pending_update.assert_called_once_with(
            switch.unique_id
        )
        mock_coordinator.api.appliance.update_network_vlan.assert_called_once_with(
            network_id="N_123",
            vlan_id=100,
            dhcpHandling="Run a DHCP server",
        )

    @pytest.mark.asyncio
    async def test_async_turn_off(
        self, mock_coordinator: MagicMock, mock_config_entry: MagicMock
    ) -> None:
        """Test async_turn_off disables DHCP."""
        switch = MerakiVLANDHCPSwitch(
            mock_coordinator, mock_config_entry, "N_123", MOCK_VLAN
        )
        switch.async_write_ha_state = MagicMock()

        await switch.async_turn_off()

        assert switch._attr_is_on is False
        switch.async_write_ha_state.assert_called_once()
        mock_coordinator.register_pending_update.assert_called_once_with(
            switch.unique_id
        )
        mock_coordinator.api.appliance.update_network_vlan.assert_called_once_with(
            network_id="N_123",
            vlan_id=100,
            dhcpHandling="Do not respond to DHCP requests",
        )
