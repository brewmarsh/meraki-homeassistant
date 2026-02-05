from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import (
    DataFetchManager,
)
from custom_components.meraki_ha.core.fetch_strategies.camera import CameraFetchStrategy
from custom_components.meraki_ha.core.models.device import MerakiDevice


@pytest.mark.asyncio
async def test_camera_modulo_fetch():
    """Test camera modulo fetch logic."""
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
        device, tasks, capabilities=["camera_stream", "analytics"]
    )
    assert f"sense_settings_{device.serial}" in tasks

    # Poll 2
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is False
    tasks = {}
    strategy.build_device_tasks(
        device, tasks, capabilities=["camera_stream", "analytics"]
    )
    assert f"sense_settings_{device.serial}" not in tasks

    # Poll 3, 4, 5
    strategy.increment_poll_count() # 3
    strategy.increment_poll_count() # 4
    strategy.increment_poll_count() # 5
    assert strategy.should_fetch_sense is False

    # Poll 6
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is True
    tasks = {}
    strategy.build_device_tasks(
        device, tasks, capabilities=["camera_stream", "analytics"]
    )
    assert f"sense_settings_{device.serial}" in tasks

@pytest.mark.asyncio
async def test_camera_sense_disabled():
    """Test camera sense disabled logic."""
    client = MagicMock()
    # Strategy with sense disabled
    strategy = CameraFetchStrategy(client, set(), enable_camera_sense=False)

    device = MerakiDevice(serial="Q123", product_type="camera")

    # Poll 1
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is False
    tasks = {}
    strategy.build_device_tasks(
        device, tasks, capabilities=["camera_stream", "analytics"]
    )
    assert f"sense_settings_{device.serial}" not in tasks

@pytest.mark.asyncio
async def test_dfm_batch_analytics_modulo():
    """Test DataFetchManager batch analytics modulo logic."""
    client = MagicMock()
    client._disabled_features = set()
    dfm = DataFetchManager(client, enable_camera_sense=True)

    devices = [MerakiDevice(serial="Q123", product_type="camera")]

    # Mock the API call - returns a coroutine
    client.camera.get_device_camera_analytics_recent = AsyncMock()
    client.run_with_semaphore.side_effect = lambda x: x

    async def mock_gather_timeout(tasks, **kwargs):
        """Mock gather to close tasks."""
        for task in tasks.values():
            task.close()
        return {}

    # Poll 1
    dfm.camera_strategy.increment_poll_count()
    # We need to mock _async_gather_with_timeout because it tries to await tasks
    # Using the 'chore' branch approach here as it correctly closes coroutines
    dfm._async_gather_with_timeout = AsyncMock(side_effect=mock_gather_timeout)
    await dfm._fetch_batch_camera_analytics(devices)
    assert dfm._async_gather_with_timeout.called

    # Poll 2
    dfm.camera_strategy.increment_poll_count()
    dfm._async_gather_with_timeout = AsyncMock(side_effect=mock_gather_timeout)
    result = await dfm._fetch_batch_camera_analytics(devices)
    assert result == {}
    # Check that _async_gather_with_timeout was NOT called for analytics
    assert not dfm._async_gather_with_timeout.called