"""Tests for Meraki blueprints."""

import os

import pytest
import yaml

BLUEPRINT_PATH = "custom_components/meraki_ha/blueprints/automation/meraki/"


# Register custom yaml constructor for '!input' tag commonly used in Home Assistant blueprints
def input_constructor(loader, node):
    return loader.construct_scalar(node)


yaml.SafeLoader.add_constructor("!input", input_constructor)


def get_blueprints():
    """Get all Meraki blueprints."""
    blueprints = []
    for file in os.listdir(BLUEPRINT_PATH):
        if file.endswith(".yaml"):
            blueprints.append(os.path.join(BLUEPRINT_PATH, file))
    return blueprints


@pytest.mark.parametrize("blueprint_file", get_blueprints())
def test_blueprint_yaml_loading(blueprint_file):
    """Test that blueprints are valid YAML and contain required keys."""
    with open(blueprint_file, encoding="utf-8") as f:
        try:
            content = yaml.safe_load(f)
            assert content is not None
            assert "blueprint" in content
            assert "name" in content["blueprint"]
            assert "description" in content["blueprint"]
            assert "domain" in content["blueprint"]
            assert content["blueprint"]["domain"] == "automation"
        except yaml.YAMLError as e:
            pytest.fail(f"Blueprint {blueprint_file} is not valid YAML: {e}")


def test_mt_leak_blueprint():
    """Test MT leak alert blueprint specifically."""
    path = os.path.join(BLUEPRINT_PATH, "meraki_mt_leak_alert.yaml")
    with open(path, encoding="utf-8") as f:
        content = yaml.safe_load(f)
        assert "Water Leak" in content["blueprint"]["name"]
        assert "input" in content["blueprint"]
        assert "leak_sensor" in content["blueprint"]["input"]


def test_mt_temp_blueprint():
    """Test MT temperature alert blueprint specifically."""
    path = os.path.join(BLUEPRINT_PATH, "meraki_mt_temp_alert.yaml")
    with open(path, encoding="utf-8") as f:
        content = yaml.safe_load(f)
        assert "Temperature Alert" in content["blueprint"]["name"]
        assert "input" in content["blueprint"]
        assert "temp_sensor" in content["blueprint"]["input"]
        assert "threshold" in content["blueprint"]["input"]
