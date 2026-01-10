"""Tests to ensure translation files stay in sync with strings.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

# Path to the integration
INTEGRATION_PATH = Path(__file__).parent.parent / "custom_components" / "meraki_ha"
STRINGS_JSON_PATH = INTEGRATION_PATH / "strings.json"
TRANSLATIONS_PATH = INTEGRATION_PATH / "translations"


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON file and return its contents."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_translation_files() -> list[Path]:
    """Get all translation JSON files."""
    return list(TRANSLATIONS_PATH.glob("*.json"))


def get_nested_keys(d: dict[str, Any], prefix: str = "") -> set[str]:
    """Get all nested keys from a dictionary as dot-separated paths."""
    keys = set()
    for key, value in d.items():
        full_key = f"{prefix}.{key}" if prefix else key
        keys.add(full_key)
        if isinstance(value, dict):
            keys.update(get_nested_keys(value, full_key))
    return keys


def get_structure_keys(d: dict[str, Any], prefix: str = "") -> set[str]:
    """Get structural keys (dict keys, not leaf values) from a dictionary."""
    keys = set()
    for key, value in d.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.add(full_key)
            keys.update(get_structure_keys(value, full_key))
    return keys


class TestTranslationFilesExist:
    """Test that required translation files exist."""

    def test_strings_json_exists(self) -> None:
        """Test that strings.json exists."""
        assert STRINGS_JSON_PATH.exists(), "strings.json must exist"

    def test_translations_directory_exists(self) -> None:
        """Test that translations directory exists."""
        assert TRANSLATIONS_PATH.exists(), "translations directory must exist"

    def test_en_json_exists(self) -> None:
        """Test that en.json translation file exists."""
        en_json = TRANSLATIONS_PATH / "en.json"
        assert en_json.exists(), "en.json translation file must exist"

    def test_translation_files_are_valid_json(self) -> None:
        """Test that all translation files are valid JSON."""
        for path in get_translation_files():
            try:
                load_json(path)
            except json.JSONDecodeError as e:
                pytest.fail(f"{path.name} is not valid JSON: {e}")


class TestOptionsMenuSync:
    """Test that options menu is properly defined in all translation files."""

    @pytest.fixture
    def strings_json(self) -> dict[str, Any]:
        """Load strings.json."""
        return load_json(STRINGS_JSON_PATH)

    @pytest.fixture
    def en_json(self) -> dict[str, Any]:
        """Load en.json."""
        return load_json(TRANSLATIONS_PATH / "en.json")

    def test_strings_json_has_options_menu(self, strings_json: dict[str, Any]) -> None:
        """Test that strings.json has options menu_options defined."""
        assert "options" in strings_json, "strings.json must have 'options' section"
        assert "step" in strings_json["options"], "options must have 'step' section"
        options_step = strings_json["options"]["step"]
        assert "init" in options_step, "options.step must have 'init'"
        assert "menu_options" in options_step["init"], (
            "options.step.init must have 'menu_options'"
        )

    def test_en_json_has_options_menu(self, en_json: dict[str, Any]) -> None:
        """Test that en.json has options menu_options defined."""
        assert "options" in en_json, "en.json must have 'options' section"
        assert "step" in en_json["options"], "options must have 'step' section"
        assert "init" in en_json["options"]["step"], "options.step must have 'init'"
        assert "menu_options" in en_json["options"]["step"]["init"], (
            "en.json options.step.init must have 'menu_options'"
        )

    def test_menu_options_match_between_strings_and_en(
        self, strings_json: dict[str, Any], en_json: dict[str, Any]
    ) -> None:
        """Test that menu_options keys match between strings.json and en.json."""
        strings_init = strings_json["options"]["step"]["init"]
        en_init = en_json["options"]["step"]["init"]
        strings_menu = set(strings_init["menu_options"].keys())
        en_menu = set(en_init["menu_options"].keys())

        missing_in_en = strings_menu - en_menu
        extra_in_en = en_menu - strings_menu

        assert not missing_in_en, f"en.json is missing menu_options: {missing_in_en}"
        assert not extra_in_en, (
            f"en.json has extra menu_options not in strings.json: {extra_in_en}"
        )

    @pytest.mark.parametrize("lang", ["es", "fr"])
    def test_translation_files_have_menu_options(self, lang: str) -> None:
        """Test that translation files have menu_options defined."""
        trans_path = TRANSLATIONS_PATH / f"{lang}.json"
        if not trans_path.exists():
            pytest.skip(f"{lang}.json does not exist")

        trans_json = load_json(trans_path)
        assert "options" in trans_json, f"{lang}.json must have 'options' section"
        assert "step" in trans_json["options"], f"{lang}.json options must have 'step'"
        assert "init" in trans_json["options"]["step"], (
            f"{lang}.json options.step must have 'init'"
        )
        assert "menu_options" in trans_json["options"]["step"]["init"], (
            f"{lang}.json options.step.init must have 'menu_options'"
        )


class TestOptionsStepsSync:
    """Test that all options steps are defined in translation files."""

    # These are the menu options defined in options_flow.py async_step_init
    REQUIRED_MENU_OPTIONS = [
        "network_selection",
        "polling",
        "camera",
        "mqtt",
        "display_preferences",
        "notifications",
    ]

    # Additional steps that are part of the options flow
    REQUIRED_OPTIONS_STEPS = [
        "init",
        "network_selection",
        "polling",
        "camera",
        "mqtt",
        "display_preferences",
        "notifications",
        "mqtt_select_destination",
        "mqtt_destination",
    ]

    @pytest.fixture
    def strings_json(self) -> dict[str, Any]:
        """Load strings.json."""
        return load_json(STRINGS_JSON_PATH)

    def test_strings_json_has_all_menu_options(
        self, strings_json: dict[str, Any]
    ) -> None:
        """Test that strings.json has all required menu options."""
        menu_options = strings_json["options"]["step"]["init"].get("menu_options", {})
        for option in self.REQUIRED_MENU_OPTIONS:
            assert option in menu_options, f"strings.json missing menu_option: {option}"

    def test_strings_json_has_all_options_steps(
        self, strings_json: dict[str, Any]
    ) -> None:
        """Test that strings.json has all required options steps."""
        steps = strings_json["options"]["step"]
        for step in self.REQUIRED_OPTIONS_STEPS:
            assert step in steps, f"strings.json missing options.step.{step}"

    @pytest.mark.parametrize("lang", ["en", "es", "fr"])
    def test_translation_has_all_menu_options(self, lang: str) -> None:
        """Test that translation files have all required menu options."""
        trans_path = TRANSLATIONS_PATH / f"{lang}.json"
        if not trans_path.exists():
            pytest.skip(f"{lang}.json does not exist")

        trans_json = load_json(trans_path)
        init_step = trans_json.get("options", {}).get("step", {}).get("init", {})
        menu_options = init_step.get("menu_options", {})

        for option in self.REQUIRED_MENU_OPTIONS:
            assert option in menu_options, f"{lang}.json missing menu_option: {option}"

    @pytest.mark.parametrize("lang", ["en", "es", "fr"])
    def test_translation_has_all_options_steps(self, lang: str) -> None:
        """Test that translation files have all required options steps."""
        trans_path = TRANSLATIONS_PATH / f"{lang}.json"
        if not trans_path.exists():
            pytest.skip(f"{lang}.json does not exist")

        trans_json = load_json(trans_path)
        steps = trans_json.get("options", {}).get("step", {})

        for step in self.REQUIRED_OPTIONS_STEPS:
            assert step in steps, f"{lang}.json missing options.step.{step}"


class TestStructuralSync:
    """Test that translation files have matching structure to strings.json."""

    # Required config steps (used by the actual config flow)
    REQUIRED_CONFIG_STEPS = ["user", "init", "reauth", "reconfigure"]

    @pytest.fixture
    def strings_json(self) -> dict[str, Any]:
        """Load strings.json."""
        return load_json(STRINGS_JSON_PATH)

    def test_en_json_has_config_section(self) -> None:
        """Test that en.json has config section."""
        en_json = load_json(TRANSLATIONS_PATH / "en.json")
        assert "config" in en_json, "en.json must have 'config' section"

    def test_en_json_has_options_section(self) -> None:
        """Test that en.json has options section."""
        en_json = load_json(TRANSLATIONS_PATH / "en.json")
        assert "options" in en_json, "en.json must have 'options' section"

    def test_en_json_has_entity_section(self) -> None:
        """Test that en.json has entity section."""
        en_json = load_json(TRANSLATIONS_PATH / "en.json")
        assert "entity" in en_json, "en.json must have 'entity' section"

    def test_en_json_has_required_config_steps(self) -> None:
        """Test that en.json has all required config steps."""
        en_json = load_json(TRANSLATIONS_PATH / "en.json")
        config_steps = en_json.get("config", {}).get("step", {})

        for step in self.REQUIRED_CONFIG_STEPS:
            assert step in config_steps, f"en.json missing config.step.{step}"

    def test_en_json_config_steps_have_required_keys(self) -> None:
        """Test that en.json config steps have required keys (title, description)."""
        en_json = load_json(TRANSLATIONS_PATH / "en.json")
        config_steps = en_json.get("config", {}).get("step", {})

        for step_name, step_data in config_steps.items():
            assert "title" in step_data, f"config.step.{step_name} missing 'title'"
            assert "description" in step_data, (
                f"config.step.{step_name} missing 'description'"
            )


class TestOptionsErrorsSync:
    """Test that options error messages are synced."""

    REQUIRED_OPTIONS_ERRORS = [
        "host_required",
        "name_required",
        "invalid_port",
    ]

    @pytest.mark.parametrize("lang", ["en", "es", "fr"])
    def test_translation_has_options_errors(self, lang: str) -> None:
        """Test that translation files have options error messages."""
        trans_path = TRANSLATIONS_PATH / f"{lang}.json"
        if not trans_path.exists():
            pytest.skip(f"{lang}.json does not exist")

        trans_json = load_json(trans_path)
        errors = trans_json.get("options", {}).get("error", {})

        for error_key in self.REQUIRED_OPTIONS_ERRORS:
            assert error_key in errors, f"{lang}.json missing options.error.{error_key}"


class TestConfigErrorsSync:
    """Test that config error messages are synced."""

    REQUIRED_CONFIG_ERRORS = [
        "invalid_auth",
        "invalid_org_id",
        "cannot_connect",
        "unknown",
    ]

    @pytest.mark.parametrize("lang", ["en", "es", "fr"])
    def test_translation_has_config_errors(self, lang: str) -> None:
        """Test that translation files have config error messages."""
        trans_path = TRANSLATIONS_PATH / f"{lang}.json"
        if not trans_path.exists():
            pytest.skip(f"{lang}.json does not exist")

        trans_json = load_json(trans_path)
        errors = trans_json.get("config", {}).get("error", {})

        for error_key in self.REQUIRED_CONFIG_ERRORS:
            assert error_key in errors, f"{lang}.json missing config.error.{error_key}"


class TestConfigAbortSync:
    """Test that config abort reasons are synced."""

    REQUIRED_CONFIG_ABORTS = [
        "reauth_successful",
        "reconfigure_successful",
        "already_configured",
        "unknown_entry",
    ]

    @pytest.mark.parametrize("lang", ["en", "es", "fr"])
    def test_translation_has_config_aborts(self, lang: str) -> None:
        """Test that translation files have config abort reasons."""
        trans_path = TRANSLATIONS_PATH / f"{lang}.json"
        if not trans_path.exists():
            pytest.skip(f"{lang}.json does not exist")

        trans_json = load_json(trans_path)
        aborts = trans_json.get("config", {}).get("abort", {})

        for abort_key in self.REQUIRED_CONFIG_ABORTS:
            assert abort_key in aborts, f"{lang}.json missing config.abort.{abort_key}"


class TestReconfigureReauthSync:
    """Test that reconfigure and reauth steps are properly defined."""

    REQUIRED_REAUTH_FIELDS = ["meraki_api_key", "meraki_org_id"]
    REQUIRED_RECONFIGURE_FIELDS = [
        "enabled_networks",
        "enable_device_tracker",
        "enable_vlan_management",
    ]

    @pytest.mark.parametrize("lang", ["en", "es", "fr"])
    def test_translation_has_reauth_step(self, lang: str) -> None:
        """Test that translation files have reauth step."""
        trans_path = TRANSLATIONS_PATH / f"{lang}.json"
        if not trans_path.exists():
            pytest.skip(f"{lang}.json does not exist")

        trans_json = load_json(trans_path)
        config_steps = trans_json.get("config", {}).get("step", {})

        assert "reauth" in config_steps, f"{lang}.json missing config.step.reauth"
        reauth = config_steps["reauth"]
        assert "title" in reauth, f"{lang}.json reauth missing title"
        assert "description" in reauth, f"{lang}.json reauth missing description"
        assert "data" in reauth, f"{lang}.json reauth missing data"

        for field in self.REQUIRED_REAUTH_FIELDS:
            assert field in reauth["data"], f"{lang}.json reauth.data missing {field}"

    @pytest.mark.parametrize("lang", ["en", "es", "fr"])
    def test_translation_has_reconfigure_step(self, lang: str) -> None:
        """Test that translation files have reconfigure step."""
        trans_path = TRANSLATIONS_PATH / f"{lang}.json"
        if not trans_path.exists():
            pytest.skip(f"{lang}.json does not exist")

        trans_json = load_json(trans_path)
        config_steps = trans_json.get("config", {}).get("step", {})

        assert "reconfigure" in config_steps, (
            f"{lang}.json missing config.step.reconfigure"
        )
        reconfigure = config_steps["reconfigure"]
        assert "title" in reconfigure, f"{lang}.json reconfigure missing title"
        assert "description" in reconfigure, (
            f"{lang}.json reconfigure missing description"
        )
        assert "data" in reconfigure, f"{lang}.json reconfigure missing data"

        for field in self.REQUIRED_RECONFIGURE_FIELDS:
            assert field in reconfigure["data"], (
                f"{lang}.json reconfigure.data missing {field}"
            )


class TestEntityTranslationsSync:
    """Test that entity translations are present."""

    @pytest.fixture
    def strings_json(self) -> dict[str, Any]:
        """Load strings.json."""
        return load_json(STRINGS_JSON_PATH)

    def test_en_json_has_sensor_entity_translations(self) -> None:
        """Test that en.json has sensor entity translations."""
        en_json = load_json(TRANSLATIONS_PATH / "en.json")
        assert "entity" in en_json, "en.json must have 'entity' section"
        assert "sensor" in en_json["entity"], "en.json entity must have 'sensor'"

    def test_en_json_has_switch_entity_translations(self) -> None:
        """Test that en.json has switch entity translations."""
        en_json = load_json(TRANSLATIONS_PATH / "en.json")
        assert "entity" in en_json, "en.json must have 'entity' section"
        assert "switch" in en_json["entity"], "en.json entity must have 'switch'"

    def test_entity_sensor_keys_match(self, strings_json: dict[str, Any]) -> None:
        """Test that entity sensor keys match between strings.json and en.json."""
        en_json = load_json(TRANSLATIONS_PATH / "en.json")

        strings_sensors = set(strings_json.get("entity", {}).get("sensor", {}).keys())
        en_sensors = set(en_json.get("entity", {}).get("sensor", {}).keys())

        missing = strings_sensors - en_sensors
        assert not missing, f"en.json entity.sensor is missing: {missing}"

    def test_entity_switch_keys_match(self, strings_json: dict[str, Any]) -> None:
        """Test that entity switch keys match between strings.json and en.json."""
        en_json = load_json(TRANSLATIONS_PATH / "en.json")

        strings_switches = set(strings_json.get("entity", {}).get("switch", {}).keys())
        en_switches = set(en_json.get("entity", {}).get("switch", {}).keys())

        missing = strings_switches - en_switches
        assert not missing, f"en.json entity.switch is missing: {missing}"
