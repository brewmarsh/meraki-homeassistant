"""Tests for the Meraki camera platform."""

from unittest.mock import AsyncMock

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

import pytest

from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_AUTO_ENABLE_RTSP,
    CONF_USE_LAN_IP_FOR_RTSP,
    DATA_CLIENT,
)
from custom_components.meraki_ha.camera import MerakiCamera, async_setup_entry

@pytest.fixture
def mock_device_coordinator():
    """Mock a MerakiDeviceCoordinator."""
    coordinator = AsyncMock()
    coordinator.data = {
        "devices": [
            {
                "serial": "Q234-ABCD-5678",
                "name": "Test Camera",
                "model": "MV12",
                "productType": "camera",
                "video_settings": {
                    "externalRtspEnabled": True,
                    "rtspUrl": "rtsp://test.com:9000/stream",
                },
            },
            {
                "serial": "Q234-EFGH-9012",
                "name": "Another Camera",
                "model": "MV22",
                "productType": "camera",
                "video_settings": {
                    "externalRtspEnabled": False,
                    "rtspUrl": None,
                },
            },
        ]
    }
    return coordinator


@pytest.mark.asyncio
async def test_camera_entity(hass: HomeAssistant, mock_device_coordinator):
    """Test the camera entity."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry_id",
        title="Test Org",
        data={},
        options={CONF_AUTO_ENABLE_RTSP: False},
    )
    config_entry.add_to_hass(hass)
    mock_device_coordinator.config_entry = config_entry

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = {
        "coordinator": mock_device_coordinator,
        DATA_CLIENT: AsyncMock(),
    }

    async_add_entities = AsyncMock()

    await async_setup_entry(hass, config_entry, async_add_entities)
    await hass.async_block_till_done()

    assert async_add_entities.call_count == 1
    entities = async_add_entities.call_args[0][0]
    assert len(entities) == 2

    camera1 = entities[0]
    assert isinstance(camera1, MerakiCamera)
    assert camera1.unique_id == "Q234-ABCD-5678-camera"
    assert camera1.name == "Test Camera"
    assert camera1.is_streaming is True
    assert await camera1.stream_source() == "rtsp://test.com:9000/stream"

    camera2 = entities[1]
    assert isinstance(camera2, MerakiCamera)
    assert camera2.unique_id == "Q234-EFGH-9012-camera"
    assert camera2.name == "Another Camera"
    assert camera2.is_streaming is False
    assert await camera2.stream_source() is None


@pytest.mark.asyncio
async def test_camera_auto_enable_rtsp(hass: HomeAssistant, mock_device_coordinator):
    """Test the camera entity with auto-enable RTSP."""
    mock_api_client = AsyncMock()
    mock_device_coordinator.hass = hass  # Set the hass object on the mock coordinator

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry_id",
        title="Test Org",
        data={},
        options={CONF_AUTO_ENABLE_RTSP: True},
    )
    config_entry.add_to_hass(hass)
    mock_device_coordinator.config_entry = config_entry

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = {
        "coordinator": mock_device_coordinator,
        DATA_CLIENT: mock_api_client,
    }

    async_add_entities = AsyncMock()

    await async_setup_entry(hass, config_entry, async_add_entities)
    await hass.async_block_till_done()

    assert async_add_entities.call_count == 1
    entities = async_add_entities.call_args[0][0]
    camera2 = entities[1]

    # Attach the hass object to the camera instance
    camera2.hass = hass

    # Mock the _enable_rtsp method to verify it's called
    camera2._enable_rtsp = AsyncMock()

    # Simulate a coordinator update to trigger the auto-enable logic
    camera2._handle_coordinator_update()
    await hass.async_block_till_done()

    # Verify that _enable_rtsp was called
    camera2._enable_rtsp.assert_called_once()


@pytest.mark.asyncio
async def test_camera_use_lan_ip_for_rtsp(hass: HomeAssistant, mock_device_coordinator):
    """Test the camera entity with use_lan_ip_for_rtsp."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry_id",
        title="Test Org",
        data={},
        options={CONF_AUTO_ENABLE_RTSP: False, CONF_USE_LAN_IP_FOR_RTSP: True},
    )
    config_entry.add_to_hass(hass)
    mock_device_coordinator.config_entry = config_entry
    mock_device_coordinator.data["devices"][0]["lanIp"] = "192.168.1.100"

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = {
        "coordinator": mock_device_coordinator,
        DATA_CLIENT: AsyncMock(),
    }

    async_add_entities = AsyncMock()

    await async_setup_entry(hass, config_entry, async_add_entities)
    await hass.async_block_till_done()

    assert async_add_entities.call_count == 1
    entities = async_add_entities.call_args[0][0]
    camera1 = entities[0]
    camera1.hass = hass
    camera1.entity_id = "camera.test_camera"

    camera1._handle_coordinator_update()
    await hass.async_block_till_done()

    assert await camera1.stream_source() == "rtsp://192.168.1.100:9000"
