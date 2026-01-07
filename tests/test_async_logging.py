"""Tests for async_logging.py module."""

import logging
from unittest.mock import MagicMock

import pytest

from custom_components.meraki_ha.async_logging import async_log_time


def test_async_log_time_decorator() -> None:
    """Test async_log_time decorator."""
    mock_logger = MagicMock()

    @async_log_time(mock_logger)
    async def sample_function():
        return "result"

    # The decorator should wrap the function
    assert sample_function is not None


@pytest.mark.asyncio
async def test_async_log_time_execution() -> None:
    """Test async_log_time decorator execution."""
    mock_logger = MagicMock()

    @async_log_time(mock_logger)
    async def sample_function():
        return "result"

    result = await sample_function()

    assert result == "result"


@pytest.mark.asyncio
async def test_async_log_time_logs_execution() -> None:
    """Test async_log_time logs execution time."""
    mock_logger = MagicMock()

    @async_log_time(mock_logger)
    async def slow_function():
        # Simulate some work
        return "done"

    await slow_function()

    # Logger.log should have been called (not logger.debug)
    mock_logger.log.assert_called()


@pytest.mark.asyncio
async def test_async_log_time_with_custom_level() -> None:
    """Test async_log_time with custom log level."""
    mock_logger = MagicMock()

    @async_log_time(mock_logger, level=logging.DEBUG)
    async def custom_level_function():
        return "done"

    await custom_level_function()

    # Should have been called with DEBUG level
    call_args = mock_logger.log.call_args
    assert call_args[0][0] == logging.DEBUG


@pytest.mark.asyncio
async def test_async_log_time_preserves_function_name() -> None:
    """Test async_log_time preserves function name."""
    mock_logger = MagicMock()

    @async_log_time(mock_logger)
    async def named_function():
        return "done"

    assert named_function.__name__ == "named_function"
