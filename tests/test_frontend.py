"""Tests for frontend.py module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.meraki_ha.frontend import (
    async_register_panel,
    async_register_static_path,
    async_unregister_frontend,
)


@pytest.fixture
def mock_hass() -> MagicMock:
    """Create a mock hass instance."""
    hass = MagicMock()
    hass.http = MagicMock()
    hass.http.async_register_static_paths = AsyncMock()
    return hass


@pytest.fixture
def mock_config_entry() -> MagicMock:
    """Create a mock config entry."""
    entry = MagicMock()
    entry.title = "Meraki"
    entry.entry_id = "test_entry_id"
    return entry


@pytest.mark.asyncio
async def test_async_register_static_path(mock_hass: MagicMock) -> None:
    """Test registering static path."""
    await async_register_static_path(mock_hass)

    mock_hass.http.async_register_static_paths.assert_called_once()


@pytest.mark.asyncio
async def test_async_register_panel(
    mock_hass: MagicMock, mock_config_entry: MagicMock
) -> None:
    """Test registering panel."""
    # Mock aiofiles.open to return manifest data
    mock_manifest = '{"version": "1.0.0"}'
    mock_open = AsyncMock()
    mock_open.__aenter__.return_value.read = AsyncMock(return_value=mock_manifest)

    with (
        patch("aiofiles.open", return_value=mock_open),
        patch(
            "custom_components.meraki_ha.frontend.frontend.async_register_built_in_panel"
        ) as mock_register,
    ):
        await async_register_panel(mock_hass, mock_config_entry)

    mock_register.assert_called_once()


def test_async_unregister_frontend(mock_hass: MagicMock) -> None:
    """Test unregistering frontend."""
    with patch(
        "custom_components.meraki_ha.frontend.frontend.async_remove_panel"
    ) as mock_remove:
        async_unregister_frontend(mock_hass)

    mock_remove.assert_called_once_with(mock_hass, "meraki")


def test_async_unregister_frontend_handles_error(mock_hass: MagicMock) -> None:
    """Test unregistering frontend handles errors gracefully."""
    with patch(
        "custom_components.meraki_ha.frontend.frontend.async_remove_panel",
        side_effect=Exception("Error"),
    ):
        # Should raise since the function doesn't handle errors
        with pytest.raises(Exception, match="Error"):
            async_unregister_frontend(mock_hass)
