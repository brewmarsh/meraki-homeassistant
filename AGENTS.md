# `AGENTS.md`: AI Agent Guidelines

**This document is for AI agents working on this codebase.** Human developers should refer to the `DEVELOPMENT.md` file for instructions.

---

## 1. Project Overview

This is a **Cisco Meraki integration for Home Assistant**. It allows users to monitor and manage their Meraki network infrastructure (access points, switches, cameras, security appliances, and environmental sensors) directly from Home Assistant.

### Key Technologies

| Layer       | Technologies                                                      |
| ----------- | ----------------------------------------------------------------- |
| Backend     | Python 3.13, Home Assistant Core, `meraki` SDK, `aiohttp`         |
| Frontend    | React, TypeScript, Vite, Home Assistant custom panel architecture |
| Testing     | pytest, pytest-asyncio, pytest-homeassistant-custom-component     |
| Linting     | Ruff, mypy, bandit, pylint                                        |
| CI/CD       | GitHub Actions, semantic-release, HACS                            |
| **Package** | **`uv` with `pyproject.toml`** (NOT pip/requirements.txt)         |

### Repository Structure

```
meraki-homeassistant/
├── custom_components/meraki_ha/     # Main integration code
│   ├── __init__.py                  # Integration entry point
│   ├── api/                         # API client and WebSocket handlers
│   ├── binary_sensor/               # Binary sensor platform
│   ├── button/                      # Button platform
│   ├── camera.py                    # Camera platform
│   ├── coordinators/                # Data update coordinators
│   ├── core/                        # Core business logic & API client
│   ├── discovery/                   # Device discovery handlers
│   ├── helpers/                     # Utility functions
│   ├── hubs/                        # Hub/bridge implementations
│   ├── number/                      # Number platform
│   ├── select/                      # Select platform
│   ├── sensor/                      # Sensor platform (largest)
│   ├── services/                    # HA service implementations
│   ├── switch/                      # Switch platform
│   ├── text/                        # Text input platform
│   └── www/                         # React frontend (Vite project)
├── tests/                           # Test suite (mirrors src structure)
├── docs/                            # Architecture & design documentation
├── DEVELOPMENT.md                   # Developer setup guide
├── CONTRIBUTING.md                  # Contribution guidelines
├── pyproject.toml                   # Python dependencies & tool config (uv)
├── uv.lock                          # Lock file for reproducible builds
└── run_checks.sh                    # Quality check script
```

### Dependency Management: uv + pyproject.toml

This project uses **`uv`** as the Python package manager. **Never use `requirements.txt` files.**

```bash
# Install all dev dependencies
uv sync

# Add a new dependency
uv add <package-name>

# Or edit pyproject.toml directly, then:
uv sync
```

All dependencies are defined in `pyproject.toml` under `[project.optional-dependencies].dev`. The `uv.lock` file ensures reproducible builds across environments.

---

## 2. Core Mission

Your primary goal is to assist human developers by performing well-defined tasks, such as fixing bugs, adding features, and refactoring code. You must do so in a way that is consistent with the project's standards and conventions.

---

## 3. Onboarding & Project-Specifics

Before starting any task, you **must** familiarize yourself with the project by reviewing the following files:

- **`README.md`**: To understand the project's purpose, features, and user-facing documentation.
- **`DEVELOPMENT.md`**: To understand the development environment, coding standards, and architectural principles.
- **`pyproject.toml`**: To understand Python dependencies and tool configurations (ruff, mypy, pytest).
- **`custom_components/meraki_ha/www/package.json`**: For frontend dependencies and scripts.

---

## 4. Recent Changes (v2.2.1)

The 2.2.1 release introduced significant improvements. Be aware of these when working on related code:

### New Features

- **Camera Snapshot Interval**: Configurable `camera_snapshot_interval` option (0-3600 seconds). Set to 0 for on-demand only (default). Cached snapshots reduce API calls.
- **Cloud Video URL Attribute**: Camera entities expose `cloud_video_url` attribute for browser viewing. Note: Streaming uses RTSP only.
- **API Network Filtering**: Only polls networks enabled in integration settings, reducing unnecessary API calls.
- **Frontend Refactor**:
  - Proper HA custom panel architecture with Web Component wrapper
  - Uses `hass.callWS()` for authenticated API calls (no more token prompts)
  - WebSocket subscription handler registered in `__init__.py`
- **Frontend UI Redesign**:
  - Clean card-based layout with CSS variables for light/dark theme support
  - Device status badges (green=online, red=offline, orange=alerting)
  - Device icons based on model type (MR, MS, MV, MX, MG, MT)
- **Camera Linking**: Link Meraki cameras to external NVR cameras (Blue Iris, Frigate, etc.)
  - Stored as `linked_camera_entity` attribute

### Bug Fixes in 2.2.1

- **API "Invalid device type" error**: Filter networks to only query those with client-capable product types
- **Camera snapshot 400 errors**: Retry mechanism (3 attempts, 2-second delays) with graceful fallback
- **Cloud video URL streaming**: Fixed incorrect stream source handling
- **Traffic analysis errors**: Informational errors no longer logged at ERROR level

---

## 5. Core Architectural Principles

### 5.1. The "Optimistic UI with Cooldown" Pattern

This is the **most critical pattern** for entities that modify configuration (e.g., `switch`, `select`, `text`).

**Problem:** The Meraki Cloud API has a significant provisioning delay (up to 2-3 minutes).

**Solution:** Optimistic state with a timed cooldown:

1. The entity's action method immediately updates its own state and writes it to the UI.
2. It makes a "fire-and-forget" API call to Meraki.
3. After the API call, it registers a "pending update" with the `MerakiDataCoordinator` (default 150 seconds).
4. The entity's state update method ignores coordinator updates while in the cooldown period.

**Example implementation pattern:**

```python
async def async_turn_on(self, **kwargs: Any) -> None:
    """Turn the entity on."""
    # 1. Optimistically update state
    self._attr_is_on = True
    self.async_write_ha_state()

    # 2. Fire-and-forget API call
    await self.coordinator.client.update_ssid(
        network_id=self._network_id,
        number=self._ssid_number,
        enabled=True
    )

    # 3. Register pending update to ignore coordinator data
    self.coordinator.register_pending_update(
        self.entity_id,
        cooldown_seconds=150
    )
```

### 5.2. API Client Conventions

- All calls to the `meraki` library object **must** use `snake_case` methods.
- The project's own client wrapper (`MerakiAPIClient`) also uses `snake_case` for consistency.
- Always use the client from the coordinator: `self.coordinator.client`

### 5.3. Home Assistant Integration Best Practices

- **Device & Entity Helpers:**
  - Use `resolve_device_info()` and `format_device_name()` for `DeviceInfo`.
  - Use `format_entity_name()` for entity names.
- **Handling Disabled Features:**
  - When a feature is disabled in Meraki Dashboard, set the entity to `Disabled`, not `unknown`.
- **Constants:**
  - All constants must be defined in `custom_components/meraki_ha/const.py`.
- **Configuration Validation:**
  - All configuration data must be validated using `voluptuous` schemas in `schemas.py`.

### 5.4. MQTT Real-Time Sensor Updates

The integration supports **real-time MQTT updates** for Meraki MT environmental sensors, bypassing the API polling delay.

**How it works:**

1. Meraki MT sensors publish data to an MQTT broker using the topic pattern: `meraki/v1/mt/{network_id}/ble/{sensor_mac}/{metric}`
2. The `MerakiMqttService` subscribes to HA's MQTT integration and listens for these topics
3. When a message arrives, it maps the sensor MAC to a device serial and updates the coordinator
4. MT sensor entities receive immediate updates instead of waiting for the next poll cycle

**Key Components:**

| Component                | Location                                | Purpose                                                                      |
| ------------------------ | --------------------------------------- | ---------------------------------------------------------------------------- |
| `MerakiMqttService`      | `services/mqtt_service.py`              | Subscribes to Meraki MQTT topics, parses messages, updates coordinator       |
| `MqttRelayManager`       | `services/mqtt_relay.py`                | Forwards messages to external MQTT brokers (multiple destinations supported) |
| `MerakiMqttStatusSensor` | `binary_sensor/mqtt_status.py`          | Binary sensor showing MQTT connection status                                 |
| `MqttStatusCard`         | `www/src/components/MqttStatusCard.tsx` | Frontend component displaying MQTT stats                                     |

**Configuration Options:**

- `enable_mqtt`: Enable/disable MQTT functionality (default: `False`)
- `mqtt_relay_destinations`: List of external MQTT brokers to forward messages to

**Relay Destination Settings:**

Each relay destination can be configured with:

- `name`: Display name for the destination
- `host`: MQTT broker hostname
- `port`: Broker port (default: 1883, TLS: 8883)
- `username`/`password`: Authentication credentials
- `use_tls`: Enable TLS encryption
- `topic_filter`: MQTT topic pattern to match (default: `meraki/v1/mt/#`)
- `device_types`: Filter by device types (e.g., `["MT"]`)

---

## 6. Git Branching Strategy

### Critical Rule: Always Branch from Beta

**Always create new branches FROM the `beta` branch, never from `main`.**

```bash
# Correct workflow
git checkout beta
git pull origin beta
git checkout -b feat/my-new-feature

# Do your work...

# When complete, merge back into beta
git checkout beta
git merge feat/my-new-feature
git push origin beta
```

The `main` branch is for **production releases only** and requires a separate PR process from `beta` to `main`.

### Branch Naming Conventions

- `feat/description` - New features
- `fix/description` or `bugfix/description` - Bug fixes
- `refactor/description` - Code refactoring
- `docs/description` - Documentation updates
- `test/description` - Test additions/fixes

---

## 7. Development Workflow

### 7.1. Running Quality Checks

Before submitting changes, you **must** run all quality checks. Use the helper script or individual commands:

**All tool configurations are centralized in `pyproject.toml`** - never create separate config files (no `.bandit.yaml`, `.ruff.toml`, `mypy.ini`, `pytest.ini`, etc.).

```bash
# All-in-one check script
./run_checks.sh

# Or run individually:

# Linting & Formatting (configured in [tool.ruff])
ruff check --fix .
ruff format .

# Type Checking (configured in [tool.mypy])
mypy custom_components/meraki_ha/ tests/

# Security Analysis (configured in [tool.bandit])
bandit -c pyproject.toml -r .

# Run Tests (configured in [tool.pytest.ini_options])
pytest

# Home Assistant Validation
docker run --rm -v "$(pwd)":/github/workspace ghcr.io/home-assistant/hassfest
```

### 7.2. Frontend Development

The Meraki side panel is a React application in `custom_components/meraki_ha/www/`.

```bash
# Install dependencies
cd custom_components/meraki_ha/www/
npm install

# Build for production (required before committing)
npm run build

# Development server (hot-reload, limited HA integration)
npm run dev
```

**Important:** After any frontend changes, you must run `npm run build` and commit the built assets (`meraki-panel.js`, `style.css`).

### 7.3. Docker Test Environment

For isolated testing with a real Home Assistant instance:

```bash
docker compose up
# Access at http://localhost:8123
```

---

## 8. Tool Usage Guidelines

- **Be precise with your tool calls.** Do not use vague or ambiguous parameters.
- **Use the `read_file` tool** to get the exact content of a file before modifying it.
- **Use the `replace` tool** for making targeted changes to files. Be sure to provide enough context in the `old_string` to avoid ambiguity.
- **Use the `run_shell_command` tool** for running commands. Be mindful of the user's operating system and use the correct syntax.
- **When in doubt, ask.** If you are unsure about how to proceed, or if a user's request is ambiguous, ask for clarification.

---

## 9. Code Contribution Standards

### 9.1. Python Code Style

- Follow **PEP 8** and all rules enforced by Ruff.
- Use **NumPy-style docstrings** (configured in `pyproject.toml`).
- Use **type hints** for all function signatures.
- Prefer **async/await** for I/O-bound operations.
- Use **early returns** for error conditions; place the happy path last.

### 9.2. Entity Naming Conventions

```python
# Device name format
f"{network_name} {device_name}"

# Entity name format
f"{device_name} {sensor_type}"

# Entity ID format (auto-generated)
# sensor.{network}_{device}_{type}
```

### 9.3. Commit Messages

Use **Conventional Commits** format:

```
type(scope): description

feat(camera): add configurable snapshot refresh interval
fix(api): filter networks before making API calls
docs(readme): update installation instructions
refactor(sensor): consolidate MT sensor base class
test(switch): add SSID toggle tests
build(deps): update homeassistant to 2025.11
ci(workflow): add beta branch workflow
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `style`, `perf`, `chore`

### 9.4. Versioning

This project uses an automated versioning and release process based on PR titles:

- `[major]`: Major version update (e.g., `1.2.3` -> `2.0.0`)
- `[minor]`: Minor version update (e.g., `1.2.3` -> `1.3.0`)
- `[patch]` or no prefix: Patch version update (e.g., `1.2.3` -> `1.2.4`)

---

## 10. Home Assistant Integration Quality Scale

This integration follows the [Home Assistant Integration Quality Scale](https://developers.home-assistant.io/docs/core/integration-quality-scale/) and targets **🏆 Platinum tier**.

### Quality Scale Tiers (Detailed)

| Tier        | Requirements                                                                                                                      |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 🥉 Bronze   | UI config flow (not YAML), unique entity IDs, basic tests, documentation                                                          |
| 🥈 Silver   | Error handling, reauthentication when credentials fail, 95%+ test coverage, code owners, auto-recovery from errors                |
| 🥇 Gold     | Discovery, diagnostics, translations, entity categories, comprehensive docs, firmware updates, full test coverage                 |
| 🏆 Platinum | All dependencies are async (`async-dependency`), websession injection (`inject-websession`), strict typing, optimized performance |

**This integration should meet Gold tier standards minimum, targeting Platinum.**

### Key Integration Patterns

Follow these Home Assistant integration patterns:

1. **Use config entries** (not YAML configuration)
2. **Implement proper async code** throughout
3. **Handle device offline states gracefully** - mark entities unavailable, don't throw errors
4. **Use `CoordinatorEntity`** for data updates - centralized polling with automatic refresh
5. **Implement reauthentication** when credentials fail (re-auth flow)
6. **Provide `DeviceInfo`** for device registry integration
7. **Use entity naming conventions** (`_attr_has_entity_name = True`)
8. **Ensure entities recover automatically** from errors without filling logs

### Key Rules to Maintain

When modifying code, ensure these rules remain satisfied:

- **entity-unique-id**: All entities must have unique IDs
- **has-entity-name**: Use `_attr_has_entity_name = True`
- **entity-unavailable**: Mark entities unavailable when device/service is offline
- **entity-device-class**: Use appropriate device classes
- **entity-category**: Assign `EntityCategory.CONFIG` or `EntityCategory.DIAGNOSTIC` where appropriate
- **test-coverage**: Maintain 95%+ test coverage
- **strict-typing**: All code must be fully typed with type annotations
- **async-dependency**: Use async patterns throughout

### Quality Scale File

Track compliance in `quality_scale.yaml`. Reference the [full rules documentation](https://developers.home-assistant.io/docs/core/integration-quality-scale/rules) for details on each rule.

---

## 11. Testing Requirements

### Critical Rule: Never Break Existing Functionality

**Always run the full test suite before completing work.** If any previously passing test fails after your changes, you must fix it before marking the task complete.

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=custom_components/meraki_ha --cov-report=term-missing
```

### Test Requirements

- **Unit tests are mandatory** for new features and bug fixes
- New features need tests proving they work
- Bug fixes need tests proving the bug is fixed
- Tests should be placed in the `tests/` directory, mirroring the source structure
- Use `pytest-asyncio` for async tests (configured with `asyncio_mode = "auto"`)
- Mock external API calls; never make real Meraki API calls in tests

**Test file naming:** `test_{module_name}.py`

**Example test structure:**

```python
"""Tests for the SSID switch platform."""

import pytest
from unittest.mock import AsyncMock, patch

from custom_components.meraki_ha.switch.ssid_switch import MerakiSSIDSwitch


@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator."""
    coordinator = AsyncMock()
    coordinator.client = AsyncMock()
    return coordinator


async def test_ssid_switch_turn_on(mock_coordinator):
    """Test turning on an SSID switch."""
    switch = MerakiSSIDSwitch(coordinator=mock_coordinator, ...)
    await switch.async_turn_on()

    assert switch.is_on is True
    mock_coordinator.client.update_ssid.assert_called_once()
```

---

## 12. Security Guidelines

### 12.1. Credentials

- **NEVER** hardcode API keys, tokens, or credentials in source code.
- Use environment variables or Home Assistant's `config_entry` for secrets.
- The Meraki API key is stored in `entry.data[CONF_API_KEY]`.

### 12.2. Cryptography

- Use only modern, secure algorithms (SHA-256+, AES-GCM, ECDHE).
- Never use MD5, SHA-1, DES, 3DES, or RC4.
- See the workspace rules for the complete banned algorithm list.

---

## 13. Common Tasks

### Adding a New Sensor

1. Create the sensor class in `custom_components/meraki_ha/sensor/` (or appropriate subdirectory).
2. Register it in the sensor platform's `async_setup_entry()`.
3. Add constants to `const.py`.
4. Write unit tests in `tests/sensor/`.
5. Run all quality checks.

### Adding a New Device Type Handler

1. Create a handler in `custom_components/meraki_ha/discovery/handlers/`.
2. Register the handler in the discovery service.
3. Ensure proper `DeviceInfo` is returned.
4. Write unit tests.

### Modifying the Frontend

1. Make changes in `custom_components/meraki_ha/www/src/`.
2. Test with `npm run dev`.
3. Build with `npm run build`.
4. Commit both source and built files.

---

## 14. Troubleshooting

### Common Issues

| Issue                      | Solution                                                       |
| -------------------------- | -------------------------------------------------------------- |
| `ha-blocking-import` error | Defer imports using `async_get_loaded_integrations()`          |
| Circular import            | Use deferred imports or restructure modules                    |
| Entity shows "unavailable" | Check coordinator data population and entity `_attr_available` |
| Frontend not loading       | Rebuild with `npm run build`, clear browser cache              |
| API rate limiting          | Increase scan interval in integration options                  |

### Debug Logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.meraki_ha: debug
```

---

## 15. Self-Correction and Learning

- If you make a mistake, acknowledge it and correct it.
- If you discover a new technique or a better way of doing something, incorporate it into your future work.
- If you encounter a new tool or a new version of a tool, read its documentation to understand how to use it correctly.
- Always verify your changes pass all quality checks before considering a task complete.

---

## 16. Quick Reference

| What                    | Where                                                    |
| ----------------------- | -------------------------------------------------------- |
| Integration entry point | `custom_components/meraki_ha/__init__.py`                |
| API client              | `custom_components/meraki_ha/core/meraki_api_client.py`  |
| Data coordinator        | `custom_components/meraki_ha/meraki_data_coordinator.py` |
| Constants               | `custom_components/meraki_ha/const.py`                   |
| Config flow             | `custom_components/meraki_ha/config_flow.py`             |
| Options flow            | `custom_components/meraki_ha/options_flow.py`            |
| MQTT service            | `custom_components/meraki_ha/services/mqtt_service.py`   |
| MQTT relay manager      | `custom_components/meraki_ha/services/mqtt_relay.py`     |
| Frontend source         | `custom_components/meraki_ha/www/src/`                   |
| Frontend build output   | `custom_components/meraki_ha/www/meraki-panel.js`        |
| Test configuration      | `pyproject.toml` → `[tool.pytest.ini_options]`           |
| Ruff configuration      | `pyproject.toml` → `[tool.ruff]`                         |
| Mypy configuration      | `pyproject.toml` → `[tool.mypy]`                         |
| Bandit configuration    | `pyproject.toml` → `[tool.bandit]`                       |
| CI workflows            | `.github/workflows/`                                     |

---

_This document was last updated for version 2.2.1._
