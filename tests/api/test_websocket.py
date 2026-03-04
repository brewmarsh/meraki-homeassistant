"""Tests for the Meraki HA WebSocket API."""

from collections.abc import AsyncGenerator, Callable, Generator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry, mock_component
from pytest_homeassistant_custom_component.typing import WebSocketGenerator

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
def bypass_platform_setup() -> Generator[None, None, None]:
    """Override global fixture to allow component setup."""
    yield


@pytest.fixture(autouse=True)
def verify_cleanup() -> Generator[None, None, None]:
    """Override verify_cleanup to avoid spurious thread errors."""
    yield


@pytest.fixture
async def setup_integration(hass: HomeAssistant) -> AsyncGenerator[MockConfigEntry, None]:
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

        hass.data[DOMAIN]["mocks"] = {
            "get_video_stream_url": mock_get_stream,
            "get_camera_snapshot": mock_get_snapshot,
        }

        yield config_entry


@pytest.fixture
async def ws_client(
    hass: HomeAssistant,
    hass_ws_client: WebSocketGenerator,
) -> Any:
    """Fixture to setup and return a websocket client."""
    async_setup_websocket_api(hass)
    return await hass_ws_client(hass)


@pytest.mark.asyncio
async def test_subscribe_meraki_data(
    hass: HomeAssistant,
    ws_client: Any,
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

    await ws_client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/subscribe_meraki_data",
            "config_entry_id": entry_id,
        }
    )

    response = await ws_client.receive_json()
    assert response["success"]
    assert response["result"]["org_name"] == "Test Org"
    mock_coordinator.async_add_listener.assert_called_once()


@pytest.mark.asyncio
async def test_get_version(
    ws_client: Any,
) -> None:
    """Test getting the version."""
    await ws_client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/get_version",
        }
    )

    response = await ws_client.receive_json()
    assert response["success"]
    assert "version" in response["result"]


@pytest.mark.asyncio
async def test_get_network_events(
    hass: HomeAssistant,
    ws_client: Any,
) -> None:
    """Test fetching network events."""
    entry_id = "test_entry"
    hass.data.setdefault(DOMAIN, {})

    mock_client = MagicMock()
    mock_client.network.get_network_events = AsyncMock(return_value=[{"id": "event1"}])

    hass.data[DOMAIN][entry_id] = {
        DATA_CLIENT: mock_client,
    }

    await ws_client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/get_network_events",
            "config_entry_id": entry_id,
            "network_id": "N_123",
            "per_page": 10,
        }
    )

    response = await ws_client.receive_json()
    assert response["success"]
    assert response["result"] == [{"id": "event1"}]
    mock_client.network.get_network_events.assert_called_once_with("N_123", per_page=10)


@pytest.mark.asyncio
async def test_update_options(
    hass: HomeAssistant,
    ws_client: Any,
) -> None:
    """Test updating options."""
    config_entry = MockConfigEntry(domain=DOMAIN, entry_id="test_entry")
    config_entry.add_to_hass(hass)

    await ws_client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/update_options",
            "config_entry_id": config_entry.entry_id,
            "options": {"enable_device_status": True},
        }
    )

    response = await ws_client.receive_json()
    assert response["success"]
    assert config_entry.options == {"enable_device_status": True}


@pytest.mark.asyncio
async def test_update_enabled_networks(
    hass: HomeAssistant,
    ws_client: Any,
) -> None:
    """Test updating enabled networks."""
    config_entry = MockConfigEntry(domain=DOMAIN, entry_id="test_entry", options={"existing": "option"})
    config_entry.add_to_hass(hass)

    await ws_client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/update_enabled_networks",
            "config_entry_id": config_entry.entry_id,
            "enabled_networks": ["N_123"],
        }
    )

    response = await ws_client.receive_json()
    assert response["success"]
    assert config_entry.options["enabled_networks"] == ["N_123"]
    assert config_entry.options["existing"] == "option"


@pytest.mark.asyncio
async def test_ipsk_get_keys(
    hass: HomeAssistant,
    ws_client: Any,
) -> None:
    """Test getting guest keys."""
    hass.data.setdefault(DOMAIN, {})

    mock_manager = MagicMock()
    mock_manager.get_active_keys.return_value = [{"id": "key1"}]
    hass.data[DOMAIN]["ipsk_manager"] = mock_manager

    await ws_client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/ipsk/get",
            "configEntryId": "test_entry",
        }
    )

    response = await ws_client.receive_json()
    assert response["success"]
    assert response["result"] == [{"id": "key1"}]
    mock_manager.get_active_keys.assert_called_once_with("test_entry", None)


@pytest.mark.asyncio
async def test_timed_access_get_policies(
    hass: HomeAssistant,
    ws_client: Any,
) -> None:
    """Test getting group policies."""
    entry_id = "test_entry"
    hass.data.setdefault(DOMAIN, {})

    mock_client = MagicMock()
    mock_client.network.get_group_policies = AsyncMock(return_value=[{"id": "p1"}])

    hass.data[DOMAIN][entry_id] = {
        DATA_CLIENT: mock_client,
    }

    await ws_client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/timed_access/get_policies",
            "configEntryId": entry_id,
            "networkId": "N_123",
        }
    )

    response = await ws_client.receive_json()
    assert response["success"]
    assert response["result"] == [{"id": "p1"}]
    mock_client.network.get_group_policies.assert_called_once_with("N_123")


@pytest.mark.asyncio
async def test_ipsk_create(
    hass: HomeAssistant,
    ws_client: Any,
) -> None:
    """Test creating a guest key."""
    hass.data.setdefault(DOMAIN, {})

    mock_manager = MagicMock()
    mock_manager.create_guest_key = AsyncMock(return_value={"id": "new_key"})
    hass.data[DOMAIN]["ipsk_manager"] = mock_manager

    await ws_client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/ipsk/create",
            "configEntryId": "test_entry",
            "networkId": "N_123",
            "ssidNumber": "0",
            "durationMinutes": 60,
            "name": "Guest",
        }
    )

    response = await ws_client.receive_json()
    assert response["success"]
    assert response["result"] == {"id": "new_key"}
    mock_manager.create_guest_key.assert_called_once_with(
        config_entry_id="test_entry",
        network_id="N_123",
        ssid_number="0",
        duration_minutes=60,
        name="Guest",
        passphrase=None,
        group_policy_id=None,
    )


@pytest.mark.asyncio
async def test_ipsk_revoke(
    hass: HomeAssistant,
    ws_client: Any,
) -> None:
    """Test revoking a guest key."""
    hass.data.setdefault(DOMAIN, {})

    mock_manager = MagicMock()
    mock_manager.remove_guest_key = AsyncMock(return_value=True)
    hass.data[DOMAIN]["ipsk_manager"] = mock_manager

    await ws_client.send_json(
        {
            "id": 1,
            "type": "meraki_ha/ipsk/revoke",
            "identityPskId": "psk1",
        }
    )

    response = await ws_client.receive_json()
    assert response["success"]
    mock_manager.remove_guest_key.assert_called_once_with("psk1")
