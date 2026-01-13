# `AGENTS.md`: Agent & Developer Guidelines

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
