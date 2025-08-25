"""Tests for the Meraki camera platform."""

from unittest.mock import AsyncMock, MagicMock

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

import pytest

from custom_components.meraki_ha.const import (
    DOMAIN,
    CONF_AUTO_ENABLE_RTSP,
    CONF_USE_LAN_IP_FOR_RTSP,
    DATA_CLIENT,
    CONF_DEVICE_NAME_FORMAT,
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
        options={},
    )
    config_entry.add_to_hass(hass)
    mock_device_coordinator.config_entry = config_entry

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = {
        "coordinator": mock_device_coordinator,
        DATA_CLIENT: AsyncMock(),
    }

    async_add_entities = MagicMock()

    await async_setup_entry(hass, config_entry, async_add_entities)
    await hass.async_block_till_done()

    assert async_add_entities.call_count == 1
    entities = async_add_entities.call_args[0][0]
    assert len(entities) == 2

    camera1 = entities[0]
    assert isinstance(camera1, MerakiCamera)
    assert camera1.unique_id == "Q234-ABCD-5678-camera"
    assert camera1.name == "[Camera] Test Camera"
    camera1.hass = hass
    camera1.entity_id = "camera.test_camera"
    camera1._handle_coordinator_update()
    await hass.async_block_till_done()
    assert camera1.is_streaming is True
    assert await camera1.stream_source() == "rtsp://test.com:9000/stream/live"

    camera2 = entities[1]
    assert isinstance(camera2, MerakiCamera)
    assert camera2.unique_id == "Q234-EFGH-9012-camera"
    assert camera2.name == "[Camera] Another Camera"

    # Test with omit format
    hass.config_entries.async_update_entry(
        config_entry, options={CONF_DEVICE_NAME_FORMAT: "omit"}
    )
    await hass.async_block_till_done()
    await async_setup_entry(hass, config_entry, async_add_entities)
    await hass.async_block_till_done()
    entities = async_add_entities.call_args[0][0]
    camera1 = entities[0]
    assert camera1.name == "Test Camera"
    assert camera2.is_streaming is False
    assert await camera2.stream_source() is None


@pytest.mark.asyncio
async def test_camera_rtsp_enabled_but_no_url(hass: HomeAssistant, mock_device_coordinator):
    """Test camera when RTSP is enabled but no URL is provided."""
    # Modify the mock data for the first camera
    mock_device_coordinator.data["devices"][0]["video_settings"]["rtspUrl"] = None

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry_id",
        title="Test Org",
        data={},
        options={},
    )
    config_entry.add_to_hass(hass)
    mock_device_coordinator.config_entry = config_entry

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = {
        "coordinator": mock_device_coordinator,
        DATA_CLIENT: AsyncMock(),
    }

    async_add_entities = MagicMock()

    await async_setup_entry(hass, config_entry, async_add_entities)
    await hass.async_block_till_done()

    assert async_add_entities.call_count == 1
    entities = async_add_entities.call_args[0][0]
    camera1 = entities[0]
    camera1.hass = hass
    camera1.entity_id = "camera.test_camera"
    camera1._handle_coordinator_update()
    await hass.async_block_till_done()
    assert camera1.is_streaming is False
    assert await camera1.stream_source() is None


@pytest.mark.asyncio
async def test_camera_auto_enable_rtsp(hass: HomeAssistant, mock_device_coordinator):
    """Test the camera entity with proactive auto-enable RTSP."""
    mock_api_client = AsyncMock()
    mock_api_client.camera.update_camera_video_settings = AsyncMock()
    mock_device_coordinator.hass = hass

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

    async_add_entities = MagicMock()

    await async_setup_entry(hass, config_entry, async_add_entities)
    await hass.async_block_till_done()

    # Verify that the API was NOT called to enable RTSP for the second camera,
    # which is an MV2 model and should be ignored.
    mock_api_client.camera.update_camera_video_settings.assert_not_called()

    # Verify that a refresh was not requested on the coordinator because no changes were made
    mock_device_coordinator.async_request_refresh.assert_not_called()


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

    async_add_entities = MagicMock()

    await async_setup_entry(hass, config_entry, async_add_entities)
    await hass.async_block_till_done()

    assert async_add_entities.call_count == 1
    entities = async_add_entities.call_args[0][0]
    camera1 = entities[0]
    camera1.hass = hass
    camera1.entity_id = "camera.test_camera"

    camera1._handle_coordinator_update()
    await hass.async_block_till_done()

    camera1._handle_coordinator_update()
    await hass.async_block_till_done()
    assert await camera1.stream_source() == "rtsp://192.168.1.100:9000/live"
    mock_device_coordinator.data["devices"][0]["video_settings"][
        "externalRtspEnabled"
    ] = False
    camera1._handle_coordinator_update()
    await hass.async_block_till_done()
    assert await camera1.stream_source() is None


@pytest.mark.asyncio
async def test_camera_mv2_no_rtsp_stream(hass: HomeAssistant, mock_device_coordinator):
    """Test that an MV2 camera does not get an RTSP stream even if enabled."""
    # Set externalRtspEnabled to True for the MV22 camera
    mock_device_coordinator.data["devices"][1]["video_settings"][
        "externalRtspEnabled"
    ] = True
    mock_device_coordinator.data["devices"][1]["video_settings"][
        "rtspUrl"
    ] = "rtsp://test.com:9000/stream"

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry_id",
        title="Test Org",
        data={},
        options={},
    )
    config_entry.add_to_hass(hass)
    mock_device_coordinator.config_entry = config_entry

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = {
        "coordinator": mock_device_coordinator,
        DATA_CLIENT: AsyncMock(),
    }

    async_add_entities = MagicMock()

    await async_setup_entry(hass, config_entry, async_add_entities)
    await hass.async_block_till_done()

    entities = async_add_entities.call_args[0][0]
    camera2 = entities[1]  # The MV22 camera
    camera2.hass = hass
    camera2.entity_id = "camera.another_camera"
    camera2._handle_coordinator_update()
    await hass.async_block_till_done()

    assert camera2.is_streaming is False
    assert await camera2.stream_source() is None
