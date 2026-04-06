"""Tests for Meraki async logging utilities."""

import pytest
from unittest.mock import MagicMock
import asyncio

from custom_components.meraki_ha.async_logging import async_log_time

@pytest.mark.asyncio
async def test_async_log_time():
    """Test the async_log_time decorator."""
    logger = MagicMock()

    @async_log_time(logger)
    async def slow_func(x):
        await asyncio.sleep(0.1)
        return x * 2

    result = await slow_func(5)
    assert result == 10

    logger.log.assert_called_once()
    call_args = logger.log.call_args
    assert call_args[0][0] == 20  # logging.INFO
    assert "Execution of %s took %.4f seconds" == call_args[0][1]
    assert call_args[0][2] == "slow_func"
    assert call_args[0][3] >= 0.1
