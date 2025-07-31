"""Global fixtures for meraki_ha integration."""

import sys
from pathlib import Path

import pytest

# Add the custom_components directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations defined in the test dir."""
    yield
