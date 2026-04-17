# Meraki Home Assistant Development Guide

This document provides a comprehensive guide for developers who want to contribute to the Meraki Home Assistant integration.

## 1. Getting Started

### 1.1. Local Development Environment

This project uses **[uv](https://github.com/astral-sh/uv)** for high-performance dependency management and virtual environments.

1.  **Install uv:**

    ```bash
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex" # Windows
    # OR
    curl -LsSf https://astral.sh/uv/install.sh | sh # macOS/Linux
    ```

2.  **Setup Environment:**
    ```bash
    uv sync
    ```
    This will create a `.venv` and install all production and development dependencies.

### 1.2. Docker Test Environment

For a consistent testing environment, use the provided Docker setup.

1.  **Start Home Assistant:**

    ```bash
    docker compose up
    ```

    This starts a local Home Assistant instance with the Meraki integration mounted.

2.  **Build Frontend (Lovelace Cards):**
    The project uses TypeScript for custom Lovelace cards.
    ```bash
    cd frontend
    npm install
    npm run build
    ```
    Build artifacts are generated in `custom_components/meraki_ha/www/`.

## 2. Running Quality Checks

All code must pass the following checks before submission.

1.  **Linting & Formatting (Ruff):**

    ```bash
    uv run ruff check --fix .
    uv run ruff format .
    ```

2.  **Type Checking (mypy):**

    ```bash
    uv run mypy custom_components/meraki_ha/ tests/
    ```

3.  **Security Analysis (bandit):**

    ```bash
    uv run bandit -c .bandit.yaml -r .
    ```

4.  **Run Tests (pytest):**

    ```bash
    uv run pytest
    ```

5.  **Home Assistant Validation (hassfest):**
    ```bash
    uv run python3 -m script.hassfest # Logic handled by internal script
    ```

## 3. Core Architectural Principles

### 3.1. Optimistic UI with Cooldown

Critical for all entities modifying configuration to avoid "toggle flicker" due to Meraki cloud provisioning delays.

- **Step 1:** Update local state immediately.
- **Step 2:** Trigger API call.
- **Step 3:** Register a "pending update" in the coordinator.
- **Step 4:** Ignore poller updates for the duration of the cooldown (default 150s).

### 3.2. Coordinator-Fetch Model

We use a centralized `MerakiMainCoordinator` and specialized `FetchStrategies` (e.g., `ApplianceUplinkHelper`) to ensure efficient, concurrent, and rate-limited API usage.

## 4. Versioning and Releases

We use **GitHub Flow** with automatic versioning via PR titles:

- `[major]`: 2.6.0 -> 3.0.0
- `[minor]`: 2.6.0 -> 2.7.0
- `[patch]`: 2.6.0 -> 2.6.1 (default)

Merging to `main` triggers a production release; `beta` is used for integration testing.
