# Technology Stack

**Analysis Date:** 2024-05-23

## Languages

**Primary:**

- Python 3.12 - Used for backend integration logic, API client, and Home Assistant component structure.

**Secondary:**

- TypeScript 5.0 - Used for frontend components and custom Home Assistant cards.
- JavaScript - Used for build scripts and legacy frontend code.

## Runtime

**Environment:**

- Home Assistant Core - The primary integration environment.

**Package Manager:**

- uv - Primary fast Python package manager and resolver.
- pip - Used for legacy dependency installation and Home Assistant compatibility.
- npm - Used for frontend dependency management in the `frontend/` directory.
- Lockfile: `uv.lock` and `package-lock.json` are present.

## Frameworks

**Core:**

- Home Assistant Integration Framework - Core framework for the integration.
- Lit 3.0 - Used for building lightweight frontend web components.
- Vite 5.0 - Frontend build tool and development server.

**Testing:**

- Pytest 8.3 - Primary backend testing framework.
- Playwright 1.48 - Used for end-to-end and UI testing.
- Braintrust - Used for AI-assisted observability and trace analysis.

**Build/Dev:**

- Ruff - Fast Python linter and formatter.
- Mypy - Static type checker for Python.
- Pre-commit - Framework for managing git hooks.

## Key Dependencies

**Critical:**

- `meraki` 1.54.0 - Official Cisco Meraki Dashboard API Python SDK.
- `aiohttp` - Used for asynchronous HTTP requests.
- `baml-py` - AI-assisted extraction and intent routing.

**Infrastructure:**

- `diskcache` 5.6.3 - Persistent disk cache for improving startup times.
- `cryptography` - Used for secure handling of credentials and webhooks.
- `webrtc-models` - Support for Meraki camera WebRTC streaming.

## Configuration

**Environment:**

- `.python-version` - Specifies the target Python version (3.12).
- `pyproject.toml` - Main configuration for Python tools (ruff, pytest, mypy).
- `tsconfig.json` - TypeScript configuration for the frontend.

**Build:**

- `vite.config.ts` - Vite configuration for frontend bundling.
- `Makefile` - Orchestrates common development tasks.

## Platform Requirements

**Development:**

- Python 3.12+
- Node.js & npm (for frontend)
- Home Assistant core development environment.

**Production:**

- Home Assistant (latest stable version recommended).
- Network access to Cisco Meraki Dashboard API (`api.meraki.com`).

---

_Stack analysis: 2024-05-23_
