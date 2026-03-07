# Meraki Home Assistant Development Guide

This document provides a comprehensive guide for developers who want to contribute to the Meraki Home Assistant integration.

## 1. Getting Started

### 1.1. Local Development Environment

This project uses standard `pip` for dependency management.

1.  **Install dependencies:**
    ```bash
    pip install -r requirements_dev.txt
    ```

### 1.2. Docker Test Environment

For a more isolated and consistent testing environment, you can use the provided Docker setup.

1.  **Ensure Docker is Running:** Make sure you have Docker Desktop (or the Docker daemon) running on your system.
2.  **Start Home Assistant:**
    ```bash
    docker compose up
    ```
    This will start a local Home Assistant instance with your local version of the Meraki integration mounted.
3.  **Build Frontend (Lovelace Cards):**
    The project uses TypeScript for custom Lovelace cards. Build artifacts are *not* tracked in Git.
    ```bash
    cd frontend
    npm install
    npm run build
    ```
    This will generate `meraki-card.js` in `custom_components/meraki_ha/www/`.
4.  **Access Home Assistant:**
    - URL: `http://localhost:8123`
    - Follow the on-screen prompts to create a user and configure the Meraki integration.

## 2. Running Quality Checks

Before submitting, you **must** run all quality checks. These are also enforced by pre-commit hooks.

1.  **Linting & Formatting (Ruff):**

    ```bash
    ruff check --fix .
    ruff format .
    ```

2.  **Type Checking (mypy):**

    ```bash
    mypy custom_components/meraki_ha/ tests/
    ```

3.  **Security Analysis (bandit):**

    ```bash
    bandit -c .bandit.yaml -r .
    ```

4.  **Run Tests (pytest):**

    ```bash
    pytest
    ```

5.  **Home Assistant Validation (hassfest):**
    ```bash
    docker run --rm -v "$(pwd)":/github/workspace ghcr.io/home-assistant/hassfest
    ```

## 3. CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment.

### 3.1. Staging Smoke Tests

The staging deployment workflow (`deploy-staging.yaml`) runs automated smoke tests on the `beta` branch. These tests include:
- Auditing Home Assistant logs for Meraki-related Python errors or tracebacks.
- Verifying that all Meraki entities are available and not in an `unknown` or `unavailable` state.

If any of these checks fail, the workflow will automatically create a GitHub Issue titled `🚨 Staging Smoke Test Failed` (if one doesn't already exist) to track the regression.

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

### 4.3. Frontend Development

- Source code resides in the `frontend/` directory.
- Build artifacts (`.js` files) in `custom_components/meraki_ha/www/` are excluded from version control.
- CI/CD pipelines are responsible for building the frontend before deployment.

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

## 6. Versioning and Releases

This project uses an automated versioning and release process based on PR titles:

- `[major]`: Major version update (e.g., `1.2.3` -> `2.0.0`).
- `[minor]`: Minor version update (e.g., `1.2.3` -> `1.3.0`).
- `[patch]` or no prefix: Patch version update (e.g., `1.2.3` -> `1.2.4`).

A `CHANGELOG.md` is automatically updated, and a new GitHub Release is created.
