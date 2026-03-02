"""Tests for camera data fetching optimization and sense logic."""

import asyncio
from collections.abc import Coroutine
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)
from custom_components.meraki_ha.core.fetch_strategies.camera import CameraFetchStrategy
from custom_components.meraki_ha.core.models.device import MerakiDevice


@pytest.fixture(name="mock_client")  # type: ignore[untyped-decorator]
def fixture_mock_client() -> MagicMock:
    """Provide a basic mock client."""
    client = MagicMock()
    # Mock run_with_semaphore to just return the coro
    client.run_with_semaphore.side_effect = lambda x: x
    # pylint: disable=protected-access
    client._disabled_features = set()
    return client


@pytest.fixture(name="mock_camera_device")  # type: ignore[untyped-decorator]
def fixture_mock_camera_device() -> MerakiDevice:
    """Provide a basic camera device."""
    return MerakiDevice(serial="Q123", product_type="camera", model="MV12")


def _cleanup_tasks(tasks: dict[str, Coroutine[Any, Any, Any] | Any]) -> None:
    """Close unawaited coroutine tasks in tests."""
    for task in tasks.values():
        if asyncio.iscoroutine(task):
            task.close()


@pytest.mark.asyncio  # type: ignore[untyped-decorator]
async def test_camera_modulo_fetch(
    mock_client: MagicMock, mock_camera_device: MerakiDevice
) -> None:
    """Test that camera sense data is fetched only on every 5th poll."""
    # Strategy with sense enabled
    strategy = CameraFetchStrategy(mock_client, set(), enable_camera_sense=True)

    # Poll 1
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is True
    tasks: dict[str, Coroutine[Any, Any, Any]] = {}
    strategy.build_device_tasks(
        mock_camera_device, tasks, capabilities=["camera_stream", "camera_analytics"]
    )
    assert f"sense_settings_{mock_camera_device.serial}" in tasks
    _cleanup_tasks(tasks)

    # Poll 2
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is False
    tasks = {}
    strategy.build_device_tasks(
        mock_camera_device, tasks, capabilities=["camera_stream", "camera_analytics"]
    )
    assert f"sense_settings_{mock_camera_device.serial}" not in tasks
    _cleanup_tasks(tasks)

    # Poll 3, 4, 5
    strategy.increment_poll_count()  # 3
    strategy.increment_poll_count()  # 4
    strategy.increment_poll_count()  # 5
    assert strategy.should_fetch_sense is False

    # Poll 6
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is True
    tasks = {}
    strategy.build_device_tasks(
        mock_camera_device, tasks, capabilities=["camera_stream", "camera_analytics"]
    )
    assert f"sense_settings_{mock_camera_device.serial}" in tasks
    _cleanup_tasks(tasks)


@pytest.mark.asyncio  # type: ignore[untyped-decorator]
async def test_camera_sense_disabled(
    mock_client: MagicMock, mock_camera_device: MerakiDevice
) -> None:
    """Test that camera sense data is never fetched when disabled."""
    # Strategy with sense disabled
    strategy = CameraFetchStrategy(mock_client, set(), enable_camera_sense=False)

    # Poll 1
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is False
    tasks: dict[str, Coroutine[Any, Any, Any]] = {}
    strategy.build_device_tasks(
        mock_camera_device, tasks, capabilities=["camera_stream", "camera_analytics"]
    )
    assert f"sense_settings_{mock_camera_device.serial}" not in tasks
    _cleanup_tasks(tasks)


@pytest.mark.asyncio  # type: ignore[untyped-decorator]
async def test_dfm_batch_analytics_modulo(
    mock_client: MagicMock, mock_camera_device: MerakiDevice
) -> None:
    """Test that batch analytics fetching respects the modulo logic."""
    dfm = DataFetchManager(mock_client, enable_camera_sense=True)

    devices = [mock_camera_device]

    # Mock the API call
    mock_client.camera.get_device_camera_analytics_recent = AsyncMock(return_value={})

    # Poll 1
    dfm.camera_strategy.increment_poll_count()

    # We test via _collect_device_tasks
    tasks: dict[str, Coroutine[Any, Any, Any]] = {}
    # pylint: disable=protected-access
    dfm._collect_device_tasks({"devices": devices}, tasks)

    # Analytics should be present in poll 1 (1 % 5 == 1? No (1-1)%5 == 0)
    assert f"camera_analytics_{devices[0].serial}" in tasks
    _cleanup_tasks(tasks)

    # Poll 2
    dfm.camera_strategy.increment_poll_count()
    tasks = {}
    # pylint: disable=protected-access
    dfm._collect_device_tasks({"devices": devices}, tasks)

    # Analytics should NOT be present in poll 2
    assert f"camera_analytics_{devices[0].serial}" not in tasks
    _cleanup_tasks(tasks)
