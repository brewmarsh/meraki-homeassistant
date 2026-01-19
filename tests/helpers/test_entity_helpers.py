"""Tests for the Meraki entity helpers."""

<<<<<<< HEAD
from custom_components.meraki_ha.core.utils.naming_utils import format_entity_name
=======
from custom_components.meraki_ha.helpers.entity_helpers import format_entity_name
>>>>>>> 9bc35b7 (Merge pull request #845 from brewmarsh/fix/frontend-build-2299669574949783162)


def test_format_entity_name():
    """Test the format_entity_name function."""
    assert format_entity_name("Device Name", "Sensor") == "Device Name Sensor"
    assert format_entity_name("Device Name", "") == "Device Name"
    assert format_entity_name("Device Name", " ") == "Device Name"
    assert format_entity_name("[Wireless] AP", "Status") == "[Wireless] AP Status"
