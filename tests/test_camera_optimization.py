import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)
from custom_components.meraki_ha.core.fetch_strategies.camera import CameraFetchStrategy
from custom_components.meraki_ha.core.models.device import MerakiDevice


@pytest.mark.asyncio
async def test_camera_modulo_fetch():
    """Test that camera sense data is fetched only on every 5th poll."""
    client = MagicMock()
    # Mock run_with_semaphore to just return the coro
    client.run_with_semaphore.side_effect = lambda x: x

    # Strategy with sense enabled
    strategy = CameraFetchStrategy(client, set(), enable_camera_sense=True)

    device = MerakiDevice(serial="Q123", product_type="camera")

    # Poll 1
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is True
    tasks = {}
    strategy.build_device_tasks(
        device, tasks, capabilities=["camera_stream", "camera_analytics"]
    )
    assert f"sense_settings_{device.serial}" in tasks

    # Cleanup Poll 1 tasks
    for task in tasks.values():
        if asyncio.iscoroutine(task):
            task.close()

    # Poll 2
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is False
    tasks = {}
    strategy.build_device_tasks(
        device, tasks, capabilities=["camera_stream", "camera_analytics"]
    )
    assert f"sense_settings_{device.serial}" not in tasks

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
        device, tasks, capabilities=["camera_stream", "camera_analytics"]
    )
    assert f"sense_settings_{device.serial}" in tasks

    # Cleanup Poll 6 tasks
    for task in tasks.values():
        if asyncio.iscoroutine(task):
            task.close()


@pytest.mark.asyncio
async def test_camera_sense_disabled():
    """Test that camera sense data is never fetched when disabled."""
    client = MagicMock()
    # Strategy with sense disabled
    strategy = CameraFetchStrategy(client, set(), enable_camera_sense=False)

    device = MerakiDevice(serial="Q123", product_type="camera")

    # Poll 1
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is False
    tasks = {}
    strategy.build_device_tasks(
        device, tasks, capabilities=["camera_stream", "camera_analytics"]
    )
    assert f"sense_settings_{device.serial}" not in tasks


@pytest.mark.asyncio
async def test_dfm_batch_analytics_modulo():
    """Test that batch analytics fetching respects the modulo logic."""
    client = MagicMock()
    client._disabled_features = set()
    dfm = DataFetchManager(client, enable_camera_sense=True)

    # Use MV12 model to ensure capabilities include analytics
    devices = [MerakiDevice(serial="Q123", product_type="camera", model="MV12")]

    # Mock the API call
    client.camera.get_device_camera_analytics_recent = AsyncMock(return_value={})
    client.run_with_semaphore.side_effect = lambda x: x

    # Poll 1
    dfm.camera_strategy.increment_poll_count()

    # We test via _collect_device_tasks
    tasks = {}
    dfm._collect_device_tasks({"devices": devices}, tasks)

    # Analytics should be present in poll 1 (1 % 5 == 1? No (1-1)%5 == 0)
    assert f"camera_analytics_{devices[0].serial}" in tasks

    # Cleanup Poll 1 tasks
    for task in tasks.values():
        if asyncio.iscoroutine(task):
            await task

    # Poll 2
    dfm.camera_strategy.increment_poll_count()
    tasks = {}
    dfm._collect_device_tasks({"devices": devices}, tasks)

    # Analytics should NOT be present in poll 2
    assert f"camera_analytics_{devices[0].serial}" not in tasks
