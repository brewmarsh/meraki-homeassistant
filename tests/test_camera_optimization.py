
import pytest
from unittest.mock import MagicMock, AsyncMock
from custom_components.meraki_ha.core.models.device import MerakiDevice
from custom_components.meraki_ha.core.fetch_strategies.camera import CameraFetchStrategy
from custom_components.meraki_ha.core.coordinator_helpers.data_fetcher import DataFetchManager

@pytest.mark.asyncio
async def test_camera_modulo_fetch():
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
    strategy.build_device_tasks(device, tasks)
    assert f"sense_settings_{device.serial}" in tasks

    # Poll 2
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is False
    tasks = {}
    strategy.build_device_tasks(device, tasks)
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
    strategy.build_device_tasks(device, tasks)
    assert f"sense_settings_{device.serial}" in tasks

@pytest.mark.asyncio
async def test_camera_sense_disabled():
    client = MagicMock()
    # Strategy with sense disabled
    strategy = CameraFetchStrategy(client, set(), enable_camera_sense=False)

    device = MerakiDevice(serial="Q123", product_type="camera")

    # Poll 1
    strategy.increment_poll_count()
    assert strategy.should_fetch_sense is False
    tasks = {}
    strategy.build_device_tasks(device, tasks)
    assert f"sense_settings_{device.serial}" not in tasks

@pytest.mark.asyncio
async def test_dfm_batch_analytics_modulo():
    client = MagicMock()
    client._disabled_features = set()
    dfm = DataFetchManager(client, enable_camera_sense=True)

    devices = [MerakiDevice(serial="Q123", product_type="camera")]

    # Mock the API call
    client.camera.get_device_camera_analytics_recent = MagicMock(return_value=AsyncMock()())
    client.run_with_semaphore.side_effect = lambda x: x

    # Poll 1
    dfm.camera_strategy.increment_poll_count()
    with MagicMock() as mock_gather:
        # We need to mock _async_gather_with_timeout because it tries to await tasks
        dfm._async_gather_with_timeout = AsyncMock(return_value={})
        await dfm._fetch_batch_camera_analytics(devices)
        assert dfm._async_gather_with_timeout.called

    # Poll 2
    dfm.camera_strategy.increment_poll_count()
    dfm._async_gather_with_timeout = AsyncMock(return_value={})
    result = await dfm._fetch_batch_camera_analytics(devices)
    assert result == {}
    # Check that _async_gather_with_timeout was NOT called for analytics
    assert not dfm._async_gather_with_timeout.called
