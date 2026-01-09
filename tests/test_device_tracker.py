"""Test the Meraki client tracker."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.const import DOMAIN
from custom_components.meraki_ha.device_tracker import (
    MerakiClientTracker,
    async_setup_entry,
)
from tests.const import MOCK_CONFIG_ENTRY, MOCK_MERAKI_CLIENT, MOCK_NETWORK


async def test_async_setup_entry(hass: HomeAssistant) -> None:
    """Test setup entry."""
    with patch(
        "custom_components.meraki_ha.device_tracker.MerakiClientTracker"
    ) as mock_tracker:
        mock_coordinator = MagicMock()
        mock_coordinator.data = {
            "networks": {MOCK_NETWORK["id"]: MOCK_NETWORK},
            "clients": {MOCK_MERAKI_CLIENT["id"]: MOCK_MERAKI_CLIENT},
            "clients_by_id": {MOCK_MERAKI_CLIENT["id"]: MOCK_MERAKI_CLIENT},
        }

        hass.data = {
            DOMAIN: {
                MOCK_CONFIG_ENTRY.entry_id: {
                    "coordinator": mock_coordinator,
                }
            }
        }
        mock_async_add_entities = AsyncMock()
        await async_setup_entry(
            hass, MOCK_CONFIG_ENTRY, mock_async_add_entities
        )
        mock_async_add_entities.assert_called_once()


async def test_meraki_client_tracker(hass: HomeAssistant) -> None:
    """Test the Meraki client tracker entity."""
    mock_coordinator = MagicMock()
    mock_coordinator.data = {
        "networks": {MOCK_NETWORK["id"]: MOCK_NETWORK},
        "clients": {MOCK_MERAKI_CLIENT["id"]: MOCK_MERAKI_CLIENT},
        "clients_by_id": {MOCK_MERAKI_CLIENT["id"]: MOCK_MERAKI_CLIENT},
    }

    client = MerakiClientTracker(
        hass, mock_coordinator, MOCK_CONFIG_ENTRY, MOCK_MERAKI_CLIENT
    )

    assert client.unique_id == f"meraki-client-{MOCK_MERAKI_CLIENT['id']}"
    assert client.name == MOCK_MERAKI_CLIENT["description"]
    assert client.is_connected is True
    assert client.source_type == "router"
    assert client.ip_address == MOCK_MERAKI_CLIENT["ip"]
    assert client.mac_address == MOCK_MERAKI_CLIENT["mac"]
    assert client.extra_state_attributes["vlan"] == MOCK_MERAKI_CLIENT["vlan"]
    assert client.extra_state_attributes["ssid"] == MOCK_MERAKI_CLIENT["ssid"]
    assert client.extra_state_attributes["status"] == MOCK_MERAKI_CLIENT["status"]
    assert (
        client.device_info["identifiers"]
        == {(DOMAIN, f"meraki-client-{MOCK_MERAKI_CLIENT['id']}")}
    )
