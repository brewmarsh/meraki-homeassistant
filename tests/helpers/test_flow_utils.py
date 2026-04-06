"""Tests for Meraki flow utilities."""

import pytest
from unittest.mock import MagicMock

from custom_components.meraki_ha.helpers.flow_utils import (
    get_network_options,
    has_cameras,
    validate_credentials,
)
from custom_components.meraki_ha.core.errors import MerakiAuthenticationError, MerakiConnectionError

def test_get_network_options():
    """Test get_network_options."""
    # Test with list of dicts
    data = {
        "networks": [
            {"name": "Network 1", "id": "N1"},
            {"name": "Network 2", "id": "N2"},
            {"id": "N3"}, # Missing name
            {"name": "Network 4"} # Missing id
        ]
    }
    options = get_network_options(data)
    assert options == [
        {"label": "Network 1", "value": "N1"},
        {"label": "Network 2", "value": "N2"}
    ]

    # Test with objects
    mock_net = MagicMock()
    mock_net.name = "Network Obj"
    mock_net.id = "N_OBJ"
    data = {"networks": [mock_net]}
    options = get_network_options(data)
    assert options == [{"label": "Network Obj", "value": "N_OBJ"}]

def test_has_cameras():
    """Test has_cameras."""
    # Test with dicts
    data = {"devices": [{"productType": "camera"}]}
    assert has_cameras(data) is True

    data = {"devices": [{"model": "MV12"}]}
    assert has_cameras(data) is True

    data = {"devices": [{"product_type": "switch"}]}
    assert has_cameras(data) is False

    # Test with objects
    mock_cam = MagicMock()
    mock_cam.product_type = "camera"
    data = {"devices": [mock_cam]}
    assert has_cameras(data) is True

    mock_mv = MagicMock()
    mock_mv.product_type = "something"
    mock_mv.model = "MV72"
    data = {"devices": [mock_mv]}
    assert has_cameras(data) is True

@pytest.mark.asyncio
async def test_validate_credentials(hass):
    """Test validate_credentials."""
    from unittest.mock import patch

    user_input = {"api_key": "test_key", "org_id": "test_org"}

    with patch("custom_components.meraki_ha.authentication.validate_meraki_credentials") as mock_val:
        mock_val.return_value = {"success": True}
        errors, result = await validate_credentials(hass, user_input)
        assert errors == {}
        assert result == {"success": True}

        # Test Auth Error
        mock_val.side_effect = MerakiAuthenticationError("Invalid API Key")
        errors, result = await validate_credentials(hass, user_input)
        assert errors == {"base": "invalid_auth"}

        # Test Connection Error
        mock_val.side_effect = MerakiConnectionError("Connection Failed")
        errors, result = await validate_credentials(hass, user_input)
        assert errors == {"base": "cannot_connect"}

        # Test Unknown Error
        mock_val.side_effect = Exception("Boom")
        errors, result = await validate_credentials(hass, user_input)
        assert errors == {"base": "unknown"}
