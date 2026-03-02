"""Tests for the Meraki HA WebSocket API."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME
from pytest_homeassistant_custom_component.common import MockConfigEntry, mock_component

from custom_components.meraki_ha.api.websocket import async_setup_websocket_api
from custom_components.meraki_ha.const import DOMAIN, DATA_CLIENT
from custom_components.meraki_ha.const_conf import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
)

MOCK_DATA = {
    "org_name": "Test Org",
    "networks": [{"id": "N_123", "name": "Test Network"}],
    "devices": [],
}


@pytest.fixture(autouse=True)
def bypass_platform_setup():
    """Override global fixture to allow component setup."""
    yield


@pytest.fixture(autouse=True)
def verify_cleanup():
    """Override verify_cleanup to avoid spurious thread errors."""
    yield


@pytest.fixture
async def setup_integration(hass: HomeAssistant) -> MockConfigEntry:
    """Set up the Meraki integration."""
    mock_component(hass, "frontend")
    mock_component(hass, "panel_custom")

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry",
        data={CONF_MERAKI_API_KEY: "test-key", CONF_MERAKI_ORG_ID: "test-org"},
        options={},
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "custom_components.meraki_ha.coordinators.main.MerakiMainCoordinator._async_update_data",
            return_value=MOCK_DATA,
        ),
        patch(
            "custom_components.meraki_ha.async_register_webhook",
            return_value=None,
        ),
        patch(
            "custom_components.meraki_ha.services.camera_service.CameraService.get_video_stream_url",
            new_callable=AsyncMock,
        ) as mock_get_stream,
        patch(
            "custom_components.meraki_ha.services.camera_service.CameraService.get_camera_snapshot",
            new_callable=AsyncMock,
        ) as mock_get_snapshot,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        # Store mocks in hass data for retrieval in tests if needed
        hass.data[DOMAIN]["mocks"] = {
            "get_video_stream_url": mock_get_stream,
            "get_camera_snapshot": mock_get_snapshot,
        }

        return config_entry


@pytest.mark.asyncio
async def test_subscribe_meraki_data(
    hass: HomeAssistant,
    hass_ws_client,
) -> None:
    """Test subscribing to Meraki data."""
    entry_id = "test_entry"
    hass.data.setdefault(DOMAIN, {})

    mock_coordinator = MagicMock()
    mock_coordinator.data = MOCK_DATA
    mock_coordinator.async_add_listener = MagicMock(return_value=lambda: None)

    hass.data[DOMAIN][entry_id] = {
        "main_coordinator": mock_coordinator,
    }

    async_setup_websocket_api(hass)
    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": entry_id,
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert response["result"]["org_name"] == "Test Org"
    mock_coordinator.async_add_listener.assert_called_once()


@pytest.mark.asyncio
async def test_get_version(
    hass: HomeAssistant,
    hass_ws_client,
) -> None:
    """Test getting the version."""
    async_setup_websocket_api(hass)
    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/get_version",
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert "version" in response["result"]


@pytest.mark.asyncio
async def test_get_network_events(
    hass: HomeAssistant,
    hass_ws_client,
) -> None:
    """Test fetching network events."""
    entry_id = "test_entry"
    hass.data.setdefault(DOMAIN, {})

    mock_client = MagicMock()
    mock_client.network.get_network_events = AsyncMock(return_value=[{"id": "event1"}])

    hass.data[DOMAIN][entry_id] = {
        DATA_CLIENT: mock_client,
    }

    async_setup_websocket_api(hass)
    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/get_network_events",
            "config_entry_id": entry_id,
            "network_id": "N_123",
            "per_page": 10,
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert response["result"] == [{"id": "event1"}]
    mock_client.network.get_network_events.assert_called_once_with("N_123", per_page=10)


@pytest.mark.asyncio
async def test_update_options(
    hass: HomeAssistant,
    hass_ws_client,
) -> None:
    """Test updating options."""
    config_entry = MockConfigEntry(domain=DOMAIN, entry_id="test_entry")
    config_entry.add_to_hass(hass)

    async_setup_websocket_api(hass)
    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/update_options",
            "config_entry_id": config_entry.entry_id,
            "options": {"enable_device_status": True},
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert config_entry.options == {"enable_device_status": True}


@pytest.mark.asyncio
async def test_update_enabled_networks(
    hass: HomeAssistant,
    hass_ws_client,
) -> None:
    """Test updating enabled networks."""
    config_entry = MockConfigEntry(domain=DOMAIN, entry_id="test_entry", options={"existing": "option"})
    config_entry.add_to_hass(hass)

    async_setup_websocket_api(hass)
    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/update_enabled_networks",
            "config_entry_id": config_entry.entry_id,
            "enabled_networks": ["N_123"],
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert config_entry.options["enabled_networks"] == ["N_123"]
    assert config_entry.options["existing"] == "option"


@pytest.mark.asyncio
async def test_timed_access_get_keys(
    hass: HomeAssistant,
    hass_ws_client,
) -> None:
    """Test getting timed access keys."""
    entry_id = "test_entry"
    hass.data.setdefault(DOMAIN, {})

    mock_manager = MagicMock()
    mock_manager.get_keys.return_value = [{"id": "key1"}]

    hass.data[DOMAIN][entry_id] = {
        "timed_access_manager": mock_manager,
    }

    async_setup_websocket_api(hass)
    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/timed_access/get_keys",
            "config_entry_id": entry_id,
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert response["result"] == [{"id": "key1"}]


@pytest.mark.asyncio
async def test_timed_access_get_policies(
    hass: HomeAssistant,
    hass_ws_client,
) -> None:
    """Test getting group policies."""
    entry_id = "test_entry"
    hass.data.setdefault(DOMAIN, {})

    mock_client = MagicMock()
    mock_client.network.get_group_policies = AsyncMock(return_value=[{"id": "p1"}])

    hass.data[DOMAIN][entry_id] = {
        DATA_CLIENT: mock_client,
    }

    async_setup_websocket_api(hass)
    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/timed_access/get_policies",
            "config_entry_id": entry_id,
            "network_id": "N_123",
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert response["result"] == [{"id": "p1"}]
    mock_client.network.get_group_policies.assert_called_once_with("N_123")


@pytest.mark.asyncio
async def test_timed_access_create(
    hass: HomeAssistant,
    hass_ws_client,
) -> None:
    """Test creating a timed access key."""
    entry_id = "test_entry"
    hass.data.setdefault(DOMAIN, {})

    mock_manager = MagicMock()
    mock_manager.create_key = AsyncMock(return_value={"id": "new_key"})

    hass.data[DOMAIN][entry_id] = {
        "timed_access_manager": mock_manager,
    }

    async_setup_websocket_api(hass)
    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/timed_access/create",
            "config_entry_id": entry_id,
            "network_id": "N_123",
            "ssid_number": "0",
            "duration": 60,
            "name": "Guest",
        }
    )

    response = await client.receive_json()
    assert response["success"]
    assert response["result"] == {"id": "new_key"}
    mock_manager.create_key.assert_called_once_with(
        config_entry_id=entry_id,
        network_id="N_123",
        ssid_number="0",
        duration_minutes=60,
        name="Guest",
        passphrase=None,
        group_policy_id=None,
    )


@pytest.mark.asyncio
async def test_timed_access_delete(
    hass: HomeAssistant,
    hass_ws_client,
) -> None:
    """Test deleting a timed access key."""
    entry_id = "test_entry"
    hass.data.setdefault(DOMAIN, {})

    mock_manager = MagicMock()
    mock_manager.delete_key = AsyncMock()

    hass.data[DOMAIN][entry_id] = {
        "timed_access_manager": mock_manager,
    }

    async_setup_websocket_api(hass)
    client = await hass_ws_client(hass)

    await client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/timed_access/delete",
            "config_entry_id": entry_id,
            "identity_psk_id": "psk1",
            "network_id": "N_123",
            "ssid_number": "0",
        }
    )

    response = await client.receive_json()
    assert response["success"]
    mock_manager.delete_key.assert_called_once_with(
        identity_psk_id="psk1",
        network_id="N_123",
        ssid_number="0",
        config_entry_id=entry_id,
    )
