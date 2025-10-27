"""Global fixtures for meraki_ha integration."""

from collections.abc import Generator

import pytest


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations: None,
) -> Generator[None, None, None]:
    """
    Enable custom integrations defined in the test dir.

    Args:
    ----
        enable_custom_integrations: The fixture to enable custom integrations.

    """
    yield
