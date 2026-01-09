"""Tests for the camera snapshot button entity."""

from typing import cast
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.button.device.camera_snapshot import (
    MerakiSnapshotButton,
)
from custom_components.meraki_ha.types import MerakiDevice

MOCK_CAMERA_DEVICE: MerakiDevice = cast(
    MerakiDevice,
    {
        "serial": "CAM-123-XYZ",
        "name": "Office Camera",
        "model": "MV12W",
        "networkId": "N_123456",
        "productType": "camera",
    },
)


@pytest.fixture
def mock_coordinator() -> MagicMock:
    """Create a mock coordinator."""
    coord = MagicMock()
    coord.data = {
        "devices": [MOCK_CAMERA_DEVICE],
    }
    coord.last_update_success = True
    return coord


@pytest.fixture
def mock_camera_service() -> MagicMock:
    """Create a mock camera service."""
    service = MagicMock()
    service.generate_snapshot = AsyncMock(
        return_value="https://snapshot.meraki.com/image.jpg"
    )
    return service


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Create a mock config entry."""
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.options = {}
    return entry


class TestMerakiSnapshotButton:
    """Tests for MerakiSnapshotButton."""

    def test_initialization(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test button initialization."""
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        assert button._device == MOCK_CAMERA_DEVICE
        assert button._attr_unique_id == "CAM-123-XYZ-snapshot"
        assert button._attr_name == "Office Camera Snapshot"

    def test_device_info(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test device_info property returns device info."""
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        device_info = button.device_info
        assert device_info is not None

    def test_get_current_device_data_found(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test _get_current_device_data returns device data when found."""
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        device_data = button._get_current_device_data()
        assert device_data is not None
        assert device_data["serial"] == "CAM-123-XYZ"

    def test_get_current_device_data_not_found(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test _get_current_device_data returns None when not found."""
        mock_coordinator.data = {"devices": []}
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        assert button._get_current_device_data() is None

    def test_get_current_device_data_no_data(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test _get_current_device_data returns None when coordinator has no data."""
        mock_coordinator.data = None
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        assert button._get_current_device_data() is None

    def test_available_true(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test available returns True when device is in coordinator data."""
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        assert button.available is True

    def test_available_false_no_device(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test available returns False when device is not in coordinator data."""
        mock_coordinator.data = {"devices": []}
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        assert button.available is False

    def test_available_false_coordinator_failed(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test available returns False when coordinator last update failed."""
        mock_coordinator.last_update_success = False
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        assert button.available is False

    def test_handle_coordinator_update(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test _handle_coordinator_update updates device data."""
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        # Update coordinator data with new device name
        updated_device = dict(MOCK_CAMERA_DEVICE)
        updated_device["name"] = "Updated Camera"
        mock_coordinator.data = {"devices": [updated_device]}

        # Mock async_write_ha_state to avoid HA dependency
        mock_async_write = MagicMock()
        object.__setattr__(button, "async_write_ha_state", mock_async_write)

        button._handle_coordinator_update()

        assert button._device["name"] == "Updated Camera"
        mock_async_write.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_press_success(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test async_press generates snapshot successfully."""
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        await button.async_press()

        mock_camera_service.generate_snapshot.assert_called_once_with("CAM-123-XYZ")

    @pytest.mark.asyncio
    async def test_async_press_no_url(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test async_press handles no URL returned."""
        mock_camera_service.generate_snapshot.return_value = None
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        # Should not raise
        await button.async_press()

        mock_camera_service.generate_snapshot.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_press_error(
        self,
        mock_coordinator: MagicMock,
        mock_camera_service: MagicMock,
        mock_config_entry: MagicMock,
    ) -> None:
        """Test async_press handles exceptions."""
        mock_camera_service.generate_snapshot.side_effect = Exception("API Error")
        button = MerakiSnapshotButton(
            coordinator=mock_coordinator,
            device=MOCK_CAMERA_DEVICE,
            camera_service=mock_camera_service,
            config_entry=mock_config_entry,
        )

        # Should not raise, just log error
        await button.async_press()

        mock_camera_service.generate_snapshot.assert_called_once()
