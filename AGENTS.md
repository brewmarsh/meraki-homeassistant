# `AGENTS.md`: Agent & Developer Guidelines

<<<<<<< HEAD
This document provides essential instructions for AI agents and human developers. Adhering to these guidelines is critical for maintaining the stability of the **Meraki Home Assistant** integration, especially regarding Python 3.13 and Home Assistant Core 2026.1 compatibility.
=======
<<<<<<< HEAD
This document provides essential instructions for AI agents and human developers. Adhering to these guidelines is critical for maintaining the stability of the **Meraki Home Assistant** integration, especially regarding Python 3.13 and Home Assistant Core 2026.1 compatibility.

---

## 1. Onboarding & Version Control

### Branch & Commit Naming

- **Branching:** Use category prefixes: `feature/`, `fix/`, `chore/`, or `docs/`.
- **Commits:** Use [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat(camera): add webrtc support`). This is **mandatory** for automated changelog generation.

---

## 2. Dependency Management & Version Locks

The environment (Python 3.13 / HA Core 2026.1) is highly sensitive. **Do not attempt to upgrade or downgrade the following pins** without manual verification.

### The "Golden Pins"

| Library         | Version    | Rationale                                               |
| --------------- | ---------- | ------------------------------------------------------- |
| `aiodns`        | `==3.6.1`  | Matches HA Core internal lock; prevents backtracking.   |
| `pycares`       | `==4.11.0` | **Critical:** Resolves `AttributeError` on Python 3.13. |
| `webrtc-models` | `==0.3.0`  | Required for modern camera streaming logic.             |
| `diskcache`     | `==5.6.3`  | Specific version tested for coordinator caching.        |

### Manifest Consistency

- **Synchronization:** Version pins **must** be identical across `manifest.json`, `requirements.txt`, and `requirements_dev.txt`.
- **Loader Safety:** Do not list `webrtc` in the `dependencies` array. Use `after_dependencies: ["stream", "camera"]` to prevent "Integration not found" errors.

---

## 3. Architectural Patterns

### 3.1. Meraki API Usage

- **Naming:** All calls to the `meraki` library **must** use `snake_case` (e.g., `dashboard.organizations.get_organizations`).
- **Centralization:** All API-specific logic must reside in the `meraki_api/` directory, separate from Home Assistant entity logic.

### 3.2. Optimistic UI with Cooldown

Meraki Dashboard has a provisioning delay. To prevent UI flickering (the "Toggle Bounce"):

- Implement an **Optimistic UI** pattern for switches and configuration entities.
- Use a **Cooldown** period after a service call before accepting a new state update from the cloud coordinator.

---

## 4. Coding Standards & Tooling

### 4.1. Python Standards

- **Formatting:** Use **Ruff** for both linting and formatting. Run `ruff format .` before any commit.
- **Type Hinting:** All new functions **must** include PEP 484 type hints.
- **Docstrings:** Follow the **Google Python Style Guide**.

### 4.2. Testing

- **Requirement:** All new features must include `pytest` coverage.
- **Mocks:** Ensure DNS resolution is mocked in tests to avoid `pycares` initialization errors in CI environments.

---

## 5. CI/CD & Automation

### Bot Triggers (Jules & Healer)

- **PAT Requirement:** GitHub suppresses events triggered by the default `GITHUB_TOKEN`. Jules **must** be configured with a Personal Access Token (PAT) named `JULES_GITHUB_PAT` to allow the **Agent Healer** to trigger on CI failures.
- **Health Audit:** After deployment, wait 90 seconds for the Meraki coordinator to stabilize before running the `tools/auditor/audit.py` script to check for `unavailable` entities.
=======
This document provides essential instructions for AI agents and human developers working across this organization's codebases. Adhering to these guidelines is critical for maintaining code quality, consistency, and stability.

This file contains **common rules** that apply to *all* projects. For project-specific details (like technology stack, file paths, and build commands), please refer to the `README.md` or `CONTRIBUTING.md` file in the specific repository.
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)

---

## 1. Onboarding & Version Control

### Branch & Commit Naming

- **Branching:** Use category prefixes: `feature/`, `fix/`, `chore/`, or `docs/`.
- **Commits:** Use [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat(camera): add webrtc support`). This is **mandatory** for automated changelog generation.

---

## 2. Dependency Management & Version Locks

The environment (Python 3.13 / HA Core 2026.1) is highly sensitive. **Do not attempt to upgrade or downgrade the following pins** without manual verification.

### The "Golden Pins"

| Library         | Version    | Rationale                                               |
| --------------- | ---------- | ------------------------------------------------------- |
| `aiodns`        | `==3.6.1`  | Matches HA Core internal lock; prevents backtracking.   |
| `pycares`       | `==4.11.0` | **Critical:** Resolves `AttributeError` on Python 3.13. |
| `webrtc-models` | `==0.3.0`  | Required for modern camera streaming logic.             |
| `diskcache`     | `==5.6.3`  | Specific version tested for coordinator caching.        |

### Manifest Consistency

- **Synchronization:** Version pins **must** be identical across `manifest.json`, `requirements.txt`, and `requirements_dev.txt`.
- **Loader Safety:** Do not list `webrtc` in the `dependencies` array. Use `after_dependencies: ["stream", "camera"]` to prevent "Integration not found" errors.

---

## 3. Architectural Patterns

### 3.1. Meraki API Usage

- **Naming:** All calls to the `meraki` library **must** use `snake_case` (e.g., `dashboard.organizations.get_organizations`).
- **Centralization:** All API-specific logic must reside in the `meraki_api/` directory, separate from Home Assistant entity logic.

### 3.2. Optimistic UI with Cooldown

Meraki Dashboard has a provisioning delay. To prevent UI flickering (the "Toggle Bounce"):

- Implement an **Optimistic UI** pattern for switches and configuration entities.
- Use a **Cooldown** period after a service call before accepting a new state update from the cloud coordinator.

---

## 4. Coding Standards & Tooling

### 4.1. Python Standards

- **Formatting:** Use **Ruff** for both linting and formatting. Run `ruff format .` before any commit.
- **Type Hinting:** All new functions **must** include PEP 484 type hints.
- **Docstrings:** Follow the **Google Python Style Guide**.

### 4.2. Testing

- **Requirement:** All new features must include `pytest` coverage.
- **Mocks:** Ensure DNS resolution is mocked in tests to avoid `pycares` initialization errors in CI environments.

---

## 5. CI/CD & Automation

### Bot Triggers (Jules & Healer)

<<<<<<< HEAD
- **PAT Requirement:** GitHub suppresses events triggered by the default `GITHUB_TOKEN`. Jules **must** be configured with a Personal Access Token (PAT) named `JULES_GITHUB_PAT` to allow the **Agent Healer** to trigger on CI failures.
- **Health Audit:** After deployment, wait 90 seconds for the Meraki coordinator to stabilize before running the `tools/auditor/audit.py` script to check for `unavailable` entities.
=======
* **Pre-commit Hooks:** This repository should use `pre-commit` to automatically run linters and formatters before each commit. You can install it with `pre-commit install`.
* **Static Analysis:** This project may use `mypy` (Python type checking) or `bandit` (Python security analysis). These checks must pass in the CI pipeline.

### 5.2. Testing

* **Coverage:** All new features or business logic **must** be accompanied by unit tests.
* **Run Tests:** Always run the full test suite (e.g., `pytest`, `npm test`) *before* submitting your code.
* **Mocks:** When writing tests, ensure all mocks are as accurate as possible to the real APIs or functions they are replacing.

---

## 6. Documentation & Iteration

* **Iterative Improvement:** If you encounter an issue (e.g., a security vulnerability, a bug, a confusing pattern), look for other instances of the same problem in the codebase and fix them all.
* **Update Documentation:** As you make changes, ensure that `README.md` and `CONTRIBUTING.md` are updated to reflect the new state of the application.
* **Update This File:** If you discover a new development technique, a useful debugging procedure, or a common pitfall, please update *this* `AGENTS.md` file to help future agents.
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
>>>>>>> c0de2c1e (fix(config_flow): Resolve CI failures and rebase on beta)
