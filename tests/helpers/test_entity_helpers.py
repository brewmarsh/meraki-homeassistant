"""Tests for the Meraki entity helpers."""

<<<<<<< HEAD
from custom_components.meraki_ha.core.utils.naming_utils import format_entity_name
=======
from custom_components.meraki_ha.helpers.entity_helpers import format_entity_name
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)


def test_format_entity_name():
    """Test the format_entity_name function."""
    assert format_entity_name("Device Name", "Sensor") == "Device Name Sensor"
    assert format_entity_name("Device Name", "") == "Device Name"
    assert format_entity_name("Device Name", " ") == "Device Name"
    assert format_entity_name("[Wireless] AP", "Status") == "[Wireless] AP Status"
