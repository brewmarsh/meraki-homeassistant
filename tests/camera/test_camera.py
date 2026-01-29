import dataclasses
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant

from custom_components.meraki_ha.camera import MerakiCamera
from tests.const import MOCK_CAMERA_DEVICE


@pytest.fixture
def mock_camera(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> MerakiCamera:
    """Create a mock MerakiCamera entity."""
    mock_coordinator.get_device.return_value = MOCK_CAMERA_DEVICE
    return MerakiCamera(
        coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        device=MOCK_CAMERA_DEVICE,
        camera_service=mock_camera_service,
    )


async def test_camera_rtsp_enabled_via_fallback(mock_coordinator, mock_config_entry):
    """Test RTSP enabled via fallback when flag is False but LAN IP is present."""
    device_data_dict = {
        "serial": "Q234-ABCD-CAM1",
        "name": "Test Camera",
        "model": "MV33",
        "networkId": "N_12345",
        "productType": "camera",
        "lanIp": "192.168.1.100",
        "status": "online",
        "videoSettings": {
            "rtspServerEnabled": False,
        },
        "rtspUrl": None,
    }
    from custom_components.meraki_ha.types import MerakiDevice

    device_data = MerakiDevice.from_dict(device_data_dict)

    # Setup coordinator to return this device
    mock_coordinator.get_device.return_value = device_data
    mock_coordinator.config_entry = mock_config_entry

    camera_service = MagicMock()

    camera = MerakiCamera(
        coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        device=device_data,
        camera_service=camera_service,
    )

    # Check extra_state_attributes
    attrs = camera.extra_state_attributes

    # Should be enabled now because of LAN IP fallback
    assert attrs["stream_status"] == "Enabled"
    assert attrs["rtsp_url"] == "rtsp://192.168.1.100:9000/live"
    assert camera.is_streaming is True

    # Verify no status message added
    mock_coordinator.add_status_message.assert_not_called()


async def test_camera_rtsp_disabled_when_no_ip(mock_coordinator, mock_config_entry):
    """Test RTSP disabled message shown when flag is False and no IP available."""
    device_data_dict = {
        "serial": "Q234-ABCD-CAM2",
        "name": "Test Camera 2",
        "model": "MV33",
        "networkId": "N_12345",
        "productType": "camera",
        "lanIp": None,  # No IP
        "status": "online",
        "videoSettings": {
            "rtspServerEnabled": False,
        },
        "rtspUrl": None,
    }
    from custom_components.meraki_ha.types import MerakiDevice

    device_data = MerakiDevice.from_dict(device_data_dict)

    mock_coordinator.get_device.return_value = device_data
    mock_coordinator.config_entry = mock_config_entry

    camera_service = MagicMock()

    camera = MerakiCamera(
        coordinator=mock_coordinator,
        config_entry=mock_config_entry,
        device=device_data,
        camera_service=camera_service,
    )

    # Check extra_state_attributes
    attrs = camera.extra_state_attributes

    assert attrs["stream_status"] == "Disabled in Meraki Dashboard"
    mock_coordinator.add_status_message.assert_called_with(
        "Q234-ABCD-CAM2", "RTSP stream is disabled in the Meraki dashboard."
    )
    # end test


@pytest.mark.asyncio
async def test_camera_turn_on(
    hass: HomeAssistant,
    mock_camera: MerakiCamera,
    mock_coordinator: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test turning the camera stream on.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_camera: The mocked camera.
        mock_coordinator: The mocked coordinator.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    mock_camera.hass = hass
    mock_camera.entity_id = "camera.test_camera"

    # Act
    await mock_camera.async_turn_on()

    # Assert
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
        MOCK_CAMERA_DEVICE.serial,
        True,
    )
    mock_coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_camera_turn_off(
    hass: HomeAssistant,
    mock_camera: MerakiCamera,
    mock_coordinator: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test turning the camera stream off.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_camera: The mocked camera.
        mock_coordinator: The mocked coordinator.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    mock_camera.hass = hass
    mock_camera.entity_id = "camera.test_camera"

    # Act
    await mock_camera.async_turn_off()

    # Assert
    mock_camera_service.async_set_rtsp_stream_enabled.assert_called_once_with(
        MOCK_CAMERA_DEVICE.serial,
        False,
    )
    mock_coordinator.async_request_refresh.assert_called_once()


@pytest.mark.parametrize(
    ("video_settings", "expected_is_streaming"),
    [
        ({"rtspServerEnabled": True, "rtspUrl": "rtsp://test.com/stream"}, True),
        # If URL is present in device object (which is updated by video_settings), is_streaming should be True
        # even if rtspServerEnabled is False in settings (fallback/override behavior)
        ({"rtspServerEnabled": False, "rtspUrl": "rtsp://test.com/stream"}, True),
        ({"rtspServerEnabled": True, "rtspUrl": None}, False),
        # HTTP is not RTSP but is_streaming uses _rtsp_url which returns it if present.
        # Wait, Meraki API sometimes returns HTTP URLs for RTSP streams?
        # If it's a valid URL, is_streaming is True.
        ({"rtspServerEnabled": True, "rtspUrl": "http://test.com/stream"}, True),
        # If only URL is present (no enabled flag), it is streaming.
        ({"rtspUrl": "rtsp://test.com/stream"}, True),
    ],
)
def test_is_streaming_logic(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
    video_settings: dict,
    expected_is_streaming: bool,
) -> None:
    """
    Test the logic of the is_streaming property.

    Args:
    ----
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.
        video_settings: The video settings to test.
        expected_is_streaming: The expected result.

    """
    # Arrange
    mock_device_data = dataclasses.replace(
        MOCK_CAMERA_DEVICE,
        video_settings=video_settings,
        # Ensure lanIp is None for this test to isolate rtspUrl logic
        lan_ip=None,
        rtsp_url=video_settings.get("rtspUrl"),
    )

    mock_coordinator.get_device.return_value = mock_device_data

    # The entity is initialized with this data, so we pass it directly
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        mock_device_data,
        mock_camera_service,
    )

    # Act & Assert
    assert camera.is_streaming == expected_is_streaming


@pytest.mark.asyncio
async def test_camera_image(
    hass: HomeAssistant,
    mock_camera: MerakiCamera,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test the camera image fetching.

    Args:
    ----
        hass: The Home Assistant instance.
        mock_camera: The mocked camera.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    mock_camera.hass = hass

    with patch(
        "custom_components.meraki_ha.camera.async_get_clientsession",
    ) as mock_session:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read.return_value = b"image_bytes"
        # mock raise_for_status to not raise
        mock_response.raise_for_status = MagicMock()
        mock_session.return_value.get.return_value.__aenter__.return_value = (
            mock_response
        )

        # Act
        image = await mock_camera.async_camera_image()

        # Assert
        assert image == b"image_bytes"
        mock_camera_service.generate_snapshot.assert_called_once_with(
            MOCK_CAMERA_DEVICE.serial,
        )


def test_entity_enabled_if_rtsp_enabled_but_no_url(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test that the camera entity is enabled if RTSP is enabled, even if no stream URL.

    Args:
    ----
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    # Create a mock device with no way to determine a stream URL
    mock_device_no_url = dataclasses.replace(
        MOCK_CAMERA_DEVICE,
        video_settings={
            "rtspServerEnabled": True,
            "rtspUrl": None,
        },
        lan_ip=None,
        rtsp_url=None,
    )

    mock_coordinator.get_device.return_value = mock_device_no_url

    # Act
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        mock_device_no_url,
        mock_camera_service,
    )

    # Assert
    assert camera.entity_registry_enabled_default
    assert camera.extra_state_attributes["stream_status"] is not None


def test_entity_disabled_if_no_url_and_rtsp_disabled(
    mock_coordinator: MagicMock,
    mock_config_entry: MagicMock,
    mock_camera_service: AsyncMock,
) -> None:
    """
    Test that the camera entity is disabled if no stream URL and RTSP is disabled.

    Args:
    ----
        mock_coordinator: The mocked coordinator.
        mock_config_entry: The mocked config entry.
        mock_camera_service: The mocked camera service.

    """
    # Arrange
    # Create a mock device with no way to determine a stream URL
    mock_device_no_url = dataclasses.replace(
        MOCK_CAMERA_DEVICE,
        video_settings={
            "rtspServerEnabled": False,
            "rtspUrl": None,
        },
        lan_ip=None,
        rtsp_url=None,
    )

    mock_coordinator.get_device.return_value = mock_device_no_url

    # Act
    camera = MerakiCamera(
        mock_coordinator,
        mock_config_entry,
        mock_device_no_url,
        mock_camera_service,
    )

    # Assert
    assert not camera.entity_registry_enabled_default
