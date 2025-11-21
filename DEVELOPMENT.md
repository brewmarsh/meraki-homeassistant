# Meraki Home Assistant Development Guide

This document provides a comprehensive guide for developers who want to contribute to the Meraki Home Assistant integration.

## 1. Getting Started

### 1.1. Local Development Environment

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1.  **Install dependencies:**
    ```bash
    poetry install
    ```
2.  **Activate the virtual environment:**
    ```bash
    poetry shell
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
    *   URL: `http://localhost:8123`
    *   Follow the on-screen prompts to create a user and configure the Meraki integration.

## 2. Running Quality Checks

Before submitting, you **must** run all quality checks. These are also enforced by pre-commit hooks.

1.  **Linting & Formatting (Ruff):**
    ```bash
    poetry run ruff check --fix .
    poetry run ruff format .
    ```

2.  **Type Checking (mypy):**
    ```bash
    poetry run mypy .
    ```

3.  **Security Analysis (bandit):**
    ```bash
    poetry run bandit -r custom_components/meraki_ha/
    ```

4.  **Run Tests (pytest):**
    ```bash
    poetry run pytest
    ```

5.  **Home Assistant Validation (hassfest):**
    ```bash
    poetry run python -m script.hassfest
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

*   **Problem:** The Meraki Cloud API has a significant provisioning delay.
*   **Solution:** We use an optimistic state with a timed cooldown.
    1.  The entity's action method immediately updates its own state and writes it to the UI.
    2.  It then makes a "fire-and-forget" API call to Meraki.
    3.  After the API call, it registers a "pending update" with the `MerakiDataCoordinator` (default 150 seconds).
    4.  The entity's state update method ignores coordinator updates while it is in the cooldown period.

### 4.2. API Client Conventions

*   All calls to the `meraki` library object **must** use `snake_case` methods.
*   This project's own client wrapper methods also use `snake_case` for consistency.

## 5. Home Assistant Integration Best Practices

*   **Device & Entity Helpers:**
    *   Use the `resolve_device_info` and `format_device_name` helpers for `DeviceInfo`.
    *   Use the `format_entity_name` helper for entity names.
*   **Handling Disabled Features:**
    *   When a feature is disabled in the Meraki Dashboard, the corresponding entity should be set to `Disabled`, not `unknown`.
*   **Constants:**
    *   All constants must be defined in `custom_components/meraki_ha/const.py`.
*   **Configuration Validation:**
    *   All configuration data must be validated using `voluptuous` schemas.

## 6. Versioning and Releases

This project uses an automated versioning and release process based on PR titles:
-   `[major]`: Major version update (e.g., `1.2.3` -> `2.0.0`).
-   `[minor]`: Minor version update (e.g., `1.2.3` -> `1.3.0`).
-   `[patch]` or no prefix: Patch version update (e.g., `1.2.3` -> `1.2.4`).

A `CHANGELOG.md` is automatically updated, and a new GitHub Release is created.
