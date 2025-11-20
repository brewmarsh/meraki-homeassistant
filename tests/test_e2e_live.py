"""Live end-to-end tests for the Meraki Web UI, running against a live HA instance."""

import os

import pytest
from playwright.async_api import async_playwright, expect

# The base URL of the Home Assistant instance
HA_BASE_URL = "http://localhost:8123"


@pytest.mark.asyncio
async def test_live_dashboard_loads():
    """
    Test that the live dashboard loads after logging in.

    This test assumes that the Home Assistant instance is already set up with a user.
    """
    username = os.environ.get("HA_USERNAME")
    password = os.environ.get("HA_PASSWORD")

    if not username or not password:
        pytest.skip(
            "HA_USERNAME and HA_PASSWORD environment variables must be set to run "
            "this test."
        )
