"""Global fixtures for meraki_ha integration."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

def pytest_configure(config):
    """A pytest hook that runs at the beginning of a test session."""
    print("sys.path:", sys.path)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations defined in the test dir."""
    yield
