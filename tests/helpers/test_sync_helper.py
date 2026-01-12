"""Tests for the sync_helper."""

from unittest.mock import MagicMock

from custom_components.meraki_ha.helpers.sync_helper import find_root_device


def test_find_root_device():
    """Test the find_root_device function."""
    device_registry = MagicMock()

    # Create a mock device hierarchy
    # root -> child -> grandchild
    root = MagicMock()
    root.id = "root"
    root.via_device_id = None

    child = MagicMock()
    child.id = "child"
    child.via_device_id = "root"

    grandchild = MagicMock()
    grandchild.id = "grandchild"
    grandchild.via_device_id = "child"

    def get_device(device_id):
        if device_id == "root":
            return root
        if device_id == "child":
            return child
        if device_id == "grandchild":
            return grandchild
        return None

    device_registry.async_get = get_device

    # Test starting from the grandchild
    assert find_root_device(device_registry, grandchild) == root

    # Test starting from the child
    assert find_root_device(device_registry, child) == root

    # Test starting from the root
    assert find_root_device(device_registry, root) == root
