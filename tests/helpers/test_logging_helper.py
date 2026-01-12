"""Tests for the logging helper module.

These tests ensure:
1. All configurable loggers have corresponding config options
2. All config options map to valid loggers
3. The apply_log_levels function works correctly
4. The get_logger function works correctly

If a test fails, it likely means someone added a logger without a config option
(or vice versa), which would break the integration's logging options flow.
"""

from __future__ import annotations

import logging
from typing import Final

import pytest

from custom_components.meraki_ha.helpers.logging_helper import (
    _CONFIG_TO_LOGGER_MAP,
    FEATURE_NAMES,
    MerakiLoggers,
    apply_log_levels,
    get_logger,
)

# Define which loggers are intentionally NOT configurable via options flow
# MAIN: Controlled via HA's yaml configuration (custom_components.meraki_ha)
# WEBHOOK: Legacy alias, deprecated - users should use ALERTS or SCANNING_API
EXCLUDED_LOGGERS: Final[set[str]] = {"MAIN", "WEBHOOK"}


class TestMerakiLoggersSynchronization:
    """Tests to ensure loggers and config options stay synchronized."""

    def test_all_configurable_loggers_have_config_options(self) -> None:
        """Verify every configurable logger has a corresponding config option.

        This test ensures that when someone adds a new logger to MerakiLoggers,
        they also add a corresponding config option to _CONFIG_TO_LOGGER_MAP.
        """
        # Get all public logger attributes from MerakiLoggers
        all_logger_names = {
            name
            for name in dir(MerakiLoggers)
            if not name.startswith("_")
            and isinstance(getattr(MerakiLoggers, name), logging.Logger)
        }

        # Get all loggers that are in the config map
        configured_loggers = set(_CONFIG_TO_LOGGER_MAP.values())

        # Check each logger (except excluded ones) has a config option
        missing_config = []
        for logger_name in all_logger_names:
            if logger_name in EXCLUDED_LOGGERS:
                continue
            logger = getattr(MerakiLoggers, logger_name)
            if logger not in configured_loggers:
                missing_config.append(logger_name)

        assert not missing_config, (
            f"Loggers missing config options in _CONFIG_TO_LOGGER_MAP: "
            f"{missing_config}. Add 'log_level_xxx' entries to const.py, "
            f"schemas.py, logging_helper.py, and translation files."
        )

    def test_all_config_options_map_to_valid_loggers(self) -> None:
        """Verify every config option maps to a valid MerakiLoggers logger.

        This test ensures that config options don't reference non-existent loggers.
        """
        # Get all loggers from MerakiLoggers class
        all_loggers = {
            getattr(MerakiLoggers, name)
            for name in dir(MerakiLoggers)
            if not name.startswith("_")
            and isinstance(getattr(MerakiLoggers, name), logging.Logger)
        }

        for config_key, logger in _CONFIG_TO_LOGGER_MAP.items():
            assert logger in all_loggers, (
                f"Config option '{config_key}' maps to a logger that is not defined "
                f"in MerakiLoggers class. Ensure the logger exists in MerakiLoggers."
            )

    def test_config_key_naming_convention(self) -> None:
        """Verify config keys follow the 'log_level_xxx' naming convention."""
        for config_key in _CONFIG_TO_LOGGER_MAP:
            assert config_key.startswith("log_level_"), (
                f"Config key '{config_key}' does not follow the 'log_level_xxx' "
                f"naming convention."
            )

    def test_feature_names_cover_important_features(self) -> None:
        """Verify FEATURE_NAMES documents the key configurable features."""
        # These are the minimum features that should be documented
        expected_features = {
            "mqtt",
            "alerts",
            "scanning_api",
            "api",
            "coordinator",
            "device_tracker",
            "discovery",
            "camera",
            "sensor",
            "switch",
            "frontend",
        }

        documented_features = set(FEATURE_NAMES.keys())

        missing_docs = expected_features - documented_features
        assert not missing_docs, (
            f"The following features are missing from FEATURE_NAMES: {missing_docs}. "
            f"Please add descriptions for these features."
        )


class TestGetLogger:
    """Tests for the get_logger function."""

    def test_get_logger_without_feature(self) -> None:
        """Test get_logger returns base logger when no feature specified."""
        logger = get_logger()
        assert logger.name == "custom_components.meraki_ha"

    def test_get_logger_with_feature(self) -> None:
        """Test get_logger returns feature-specific logger."""
        logger = get_logger("mqtt")
        assert logger.name == "custom_components.meraki_ha.mqtt"

    def test_get_logger_returns_logger_instance(self) -> None:
        """Test get_logger returns a logging.Logger instance."""
        logger = get_logger("api")
        assert isinstance(logger, logging.Logger)

    @pytest.mark.parametrize(
        "feature",
        [
            "mqtt",
            "api",
            "coordinator",
            "discovery",
            "camera",
            "sensor",
            "switch",
            "frontend",
        ],
    )
    def test_get_logger_various_features(self, feature: str) -> None:
        """Test get_logger works for various feature names."""
        logger = get_logger(feature)
        assert logger.name == f"custom_components.meraki_ha.{feature}"


class TestApplyLogLevels:
    """Tests for the apply_log_levels function."""

    def test_apply_log_levels_sets_correct_levels(self) -> None:
        """Test apply_log_levels sets the correct log level for each logger."""
        options: dict[str, str] = {
            "log_level_mqtt": "warning",
            "log_level_api": "debug",
            "log_level_coordinator": "error",
        }

        apply_log_levels(options)

        assert MerakiLoggers.MQTT.level == logging.WARNING
        assert MerakiLoggers.API.level == logging.DEBUG
        assert MerakiLoggers.COORDINATOR.level == logging.ERROR

    def test_apply_log_levels_defaults_to_info(self) -> None:
        """Test apply_log_levels defaults to INFO when option not provided."""
        # Reset logger level first
        MerakiLoggers.MQTT.setLevel(logging.NOTSET)

        options: dict[str, str] = {}  # No options provided

        apply_log_levels(options)

        # Should default to INFO
        assert MerakiLoggers.MQTT.level == logging.INFO

    def test_apply_log_levels_handles_invalid_level(self) -> None:
        """Test apply_log_levels handles invalid log level gracefully."""
        options: dict[str, str] = {
            "log_level_mqtt": "invalid_level",
        }

        # Should not raise, should default to INFO
        apply_log_levels(options)
        assert MerakiLoggers.MQTT.level == logging.INFO

    @pytest.mark.parametrize(
        ("level_str", "expected_level"),
        [
            ("debug", logging.DEBUG),
            ("info", logging.INFO),
            ("warning", logging.WARNING),
            ("error", logging.ERROR),
            ("critical", logging.CRITICAL),
        ],
    )
    def test_apply_log_levels_all_levels(
        self, level_str: str, expected_level: int
    ) -> None:
        """Test apply_log_levels handles all valid log levels."""
        options = {"log_level_mqtt": level_str}

        apply_log_levels(options)

        assert MerakiLoggers.MQTT.level == expected_level


class TestMerakiLoggersClass:
    """Tests for the MerakiLoggers class itself."""

    def test_main_logger_is_base_domain(self) -> None:
        """Test MAIN logger uses the base domain."""
        assert MerakiLoggers.MAIN.name == "custom_components.meraki_ha"

    @pytest.mark.parametrize(
        ("logger_attr", "expected_suffix"),
        [
            ("API", "api"),
            ("COORDINATOR", "coordinator"),
            ("MQTT", "mqtt"),
            ("ALERTS", "alerts"),
            ("SCANNING_API", "scanning_api"),
            ("WEBHOOK", "webhook"),
            ("DEVICE_TRACKER", "device_tracker"),
            ("CAMERA", "camera"),
            ("SENSOR", "sensor"),
            ("SWITCH", "switch"),
            ("DISCOVERY", "discovery"),
            ("FRONTEND", "frontend"),
        ],
    )
    def test_logger_names_correct(self, logger_attr: str, expected_suffix: str) -> None:
        """Test each logger has the correct name."""
        logger = getattr(MerakiLoggers, logger_attr)
        expected_name = f"custom_components.meraki_ha.{expected_suffix}"
        assert logger.name == expected_name

    def test_all_loggers_are_logger_instances(self) -> None:
        """Test all public attributes of MerakiLoggers are Logger instances."""
        for name in dir(MerakiLoggers):
            if name.startswith("_"):
                continue
            attr = getattr(MerakiLoggers, name)
            if isinstance(attr, logging.Logger):
                # This is expected
                pass
            else:
                pytest.fail(
                    f"MerakiLoggers.{name} is not a logging.Logger instance. "
                    f"All public attributes should be loggers."
                )


class TestLoggerConfigConsistency:
    """Tests to ensure const.py, schemas.py, and logging_helper.py stay in sync."""

    def test_config_map_uses_const_values(self) -> None:
        """Verify config map keys match the constants defined in const.py."""
        from custom_components.meraki_ha import const

        # Get all CONF_LOG_LEVEL_* constants from const.py
        const_log_levels = {
            getattr(const, name)
            for name in dir(const)
            if name.startswith("CONF_LOG_LEVEL_")
        }

        config_map_keys = set(_CONFIG_TO_LOGGER_MAP.keys())

        # All config map keys should be defined as constants
        for key in config_map_keys:
            const_name = key.upper().replace("LOG_LEVEL_", "")
            assert key in const_log_levels, (
                f"Config key '{key}' not defined in const.py. "
                f"Add CONF_LOG_LEVEL_{const_name}."
            )

    def test_all_const_log_levels_are_in_config_map(self) -> None:
        """Verify all CONF_LOG_LEVEL_* constants are used in the config map."""
        from custom_components.meraki_ha import const

        # Get all CONF_LOG_LEVEL_* constants from const.py
        const_log_levels = {
            getattr(const, name)
            for name in dir(const)
            if name.startswith("CONF_LOG_LEVEL_")
        }

        config_map_keys = set(_CONFIG_TO_LOGGER_MAP.keys())

        unused_constants = const_log_levels - config_map_keys
        assert not unused_constants, (
            f"CONF_LOG_LEVEL_* constants defined but not used in "
            f"_CONFIG_TO_LOGGER_MAP: {unused_constants}."
        )
