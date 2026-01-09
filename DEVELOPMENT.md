# Meraki Home Assistant Development Guide

This document provides a comprehensive guide for developers who want to contribute to the Meraki Home Assistant integration.

## 1. Getting Started

### 1.1. Package Manager: uv

This project uses **`uv`** as the Python package manager and **`pyproject.toml`** for all dependency management. Never use `requirements.txt` files.

1.  **Install uv** (if not already installed):

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Install dependencies:**

    ```bash
    uv sync --all-extras
    ```

    This reads `pyproject.toml` and installs all dev dependencies from `[project.optional-dependencies].dev`. The `uv.lock` file ensures reproducible builds.

3.  **Adding new dependencies:**
    ```bash
    uv add <package-name>
    # Or edit pyproject.toml directly under [project.optional-dependencies].dev
    uv sync --all-extras
    ```

### 1.2. Docker Test Environment

For a more isolated and consistent testing environment, you can use the provided Docker setup.

1.  **Ensure Docker is Running:** Make sure you have Docker Desktop (or the Docker daemon) running on your system.
2.  **Start Home Assistant:**
    ```bash
    docker compose up
    ```
    This will start a local Home Assistant instance with your local version of the Meraki integration mounted.
3.  **Access Home Assistant:**
    - URL: `http://localhost:8123`
    - Follow the on-screen prompts to create a user and configure the Meraki integration.

## 2. Running Quality Checks

Before submitting, you **must** run all quality checks.

**All tool configurations are centralized in `pyproject.toml`** - never create separate config files.

### 2.1. Recommended: Use the Helper Script

The easiest way to run all checks is with the helper script:

```bash
./run_checks.sh
```

This script will:

- Auto-install `uv` if not present
- Sync all dependencies
- Run ruff, bandit, mypy, and pytest

### 2.2. Running Checks Individually

If you need to run checks individually, use `uv run` to ensure tools run in the virtual environment:

1.  **Linting & Formatting (Ruff):** - configured in `[tool.ruff]`

    ```bash
    uv run ruff check --fix .
    uv run ruff format .
    ```

2.  **Type Checking (mypy):** - configured in `[tool.mypy]`

    ```bash
    uv run mypy custom_components/meraki_ha/ tests/
    ```

3.  **Security Analysis (bandit):** - configured in `[tool.bandit]`

    ```bash
    uv run bandit -c pyproject.toml -r custom_components/meraki_ha/
    ```

4.  **Run Tests (pytest):** - configured in `[tool.pytest.ini_options]`

    ```bash
    uv run pytest
    ```

5.  **Home Assistant Validation (hassfest):**
    ```bash
    docker run --rm -v "$(pwd)":/github/workspace ghcr.io/home-assistant/hassfest
    ```

## 3. Frontend Development

The Meraki side panel is a modern web application built with React, Vite, and TypeScript.

### 3.1. Frontend Code Location

The source code for the frontend panel is located in the `custom_components/meraki_ha/www/` directory.

### 3.2. Installing Dependencies

To work with the frontend code, you must first install the necessary Node.js dependencies.

```bash
cd custom_components/meraki_ha/www/
npm install
```

### 3.3. Building the Frontend

After making changes to the frontend code, you must rebuild the panel to generate the final JavaScript and CSS files.

```bash
npm run build
```

This will compile the frontend application and place the necessary `meraki-panel.js` and `style.css` files in the `custom_components/meraki_ha/www/` directory.

### 3.4. Development Server

For a more interactive development experience, you can run the Vite development server:

```bash
npm run dev
```

This will start a local server, typically on port 5173, that provides hot-reloading. Note that in this mode, the panel will not have access to the Home Assistant `hass` object and may not function completely.

## 4. Core Architectural Principles

### 4.1. The "Optimistic UI with Cooldown" Pattern

This is the **most critical pattern** in this codebase for all entities that modify configuration (e.g., `switch`, `select`, `text`).

- **Problem:** The Meraki Cloud API has a significant provisioning delay.
- **Solution:** We use an optimistic state with a timed cooldown.
  1.  The entity's action method immediately updates its own state and writes it to the UI.
  2.  It then makes a "fire-and-forget" API call to Meraki.
  3.  After the API call, it registers a "pending update" with the `MerakiDataCoordinator` (default 150 seconds).
  4.  The entity's state update method ignores coordinator updates while it is in the cooldown period.

### 4.2. API Client Conventions

- All calls to the `meraki` library object **must** use `snake_case` methods.
- This project's own client wrapper methods also use `snake_case` for consistency.

## 5. Home Assistant Integration Best Practices

- **Device & Entity Helpers:**
  - Use the `resolve_device_info` and `format_device_name` helpers for `DeviceInfo`.
  - Use the `format_entity_name` helper for entity names.
- **Handling Disabled Features:**
  - When a feature is disabled in the Meraki Dashboard, the corresponding entity should be set to `Disabled`, not `unknown`.
- **Constants:**
  - All constants must be defined in `custom_components/meraki_ha/const.py`.
- **Configuration Validation:**
  - All configuration data must be validated using `voluptuous` schemas.

## 6. Git Branching Strategy

**Always create new branches FROM the `beta` branch, never from `main`.**

```bash
# Create a new feature branch from beta
git checkout beta
git pull origin beta
git checkout -b feat/my-new-feature

# When work is complete and all checks pass, merge back into beta
git checkout beta
git merge feat/my-new-feature
git push origin beta
```

The `main` branch is for **production releases only** and requires a separate PR process from `beta` to `main`.

## 7. Testing Requirements

**Never break existing functionality.** Always run the full test suite before completing work.

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=custom_components/meraki_ha --cov-report=term-missing
```

- All code changes **require corresponding unit tests**
- New features need tests proving they work
- Bug fixes need tests proving the bug is fixed
- Place tests in `tests/` mirroring the source structure
- If any previously passing test fails after your changes, **fix it before marking the task complete**

## 8. Versioning and Releases

This project uses an automated versioning and release process based on PR titles:

- `[major]`: Major version update (e.g., `1.2.3` -> `2.0.0`).
- `[minor]`: Minor version update (e.g., `1.2.3` -> `1.3.0`).
- `[patch]` or no prefix: Patch version update (e.g., `1.2.3` -> `1.2.4`).

A `CHANGELOG.md` is automatically updated, and a new GitHub Release is created.

## 9. Commit Message Format

Use **Conventional Commits** format:

```
type(scope): description

feat(sensor): add humidity threshold alert
fix(api): handle rate limiting gracefully
docs(readme): update installation instructions
refactor(sensor): consolidate MT sensor base class
test(switch): add SSID toggle tests
build(deps): update homeassistant to 2025.11
ci(workflow): add beta branch workflow
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `style`, `perf`, `chore`
