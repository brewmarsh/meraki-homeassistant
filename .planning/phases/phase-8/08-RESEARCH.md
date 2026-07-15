# Phase 8: Refactor Staging Test Deployment - Research

**Researched:** 2026-04-27
**Domain:** Staging Test Infrastructure & Automated Quality Assurance
**Confidence:** HIGH

## Summary

The current staging test infrastructure is fragmented, with critical health check logic split between `scripts/staging_test_entities.py` (REST API-based) and `scripts/staging_test_probe.py` (WebSocket-based). This redundancy leads to maintenance overhead and inconsistent error reporting. Additionally, the existing failure reporting mechanism lacks deduplication, resulting in excessive noisy GitHub issues.

This phase aims to consolidate all staging health checks into a unified package (`src/staging_test/`), implement robust failure fingerprinting to deduplicate GitHub issue reporting, and standardize health checks by transitioning fully to the Home Assistant WebSocket API to ensure high-fidelity, real-time status auditing.

**Primary recommendation:** Consolidate all staging health logic into the `src/staging_test/` package, leveraging the existing `src/staging_test/ha_client.py` for all interactions, and implement a hashing mechanism for failure grouping before interacting with the GitHub API.

## User Constraints

_(None in CONTEXT.md)_

## Standard Stack

| Library                 | Purpose              | Why Standard                            |
| ----------------------- | -------------------- | --------------------------------------- |
| `aiohttp`               | Async WebSocket/HTTP | Native HA interaction, high-concurrency |
| `github-api` (via REST) | Issue Management     | Standard for GH Actions automation      |
| `hashlib`               | Fingerprinting       | Essential for stable deduplication      |

## Architecture Patterns

### Recommended Project Structure

```
src/staging_test/
├── __init__.py        # Exposes unified runner
├── cli.py             # CLI entry point
├── ha_client.py       # Standardized WS client
├── auditor.py         # Consolidates health check logic
└── reporter.py        # Fingerprinting & GitHub issue logic
```

### Pattern: Fingerprinting for Deduplication

**What:** Generate a unique hash for each failure event based on `(error_type, entity_id, context_fingerprint)`.
**When to use:** Before creating any GitHub issue, compare the hash against existing open issues with specific labels (e.g., `staging-failure`).
**Example:**

```python
import hashlib
def generate_fingerprint(failure):
    content = f"{failure['type']}:{failure['entity_id']}"
    return hashlib.sha256(content.encode()).hexdigest()
```

### Anti-Patterns to Avoid

- **Hardcoding HA API endpoints:** Use the HA library/WS client to discover state.
- **Reporting raw failures:** Always group by fingerprint to avoid spamming the maintainers.

## Don't Hand-Roll

| Problem        | Don't Build       | Use Instead                                      | Why                                                      |
| -------------- | ----------------- | ------------------------------------------------ | -------------------------------------------------------- |
| Issue Tracking | Manual REST calls | Existing GH Issue API                            | Standardized metadata, labels, and assignment.           |
| WS Connections | Raw TCP/Async     | `homeassistant_ws` (or robust `aiohttp` wrapper) | Avoid protocol complexity and authentication edge cases. |

## Runtime State Inventory

| Category            | Items Found                                   | Action Required                       |
| ------------------- | --------------------------------------------- | ------------------------------------- |
| Stored data         | None — verified by codebase grep              | None                                  |
| Live service config | GitHub Issue labels (e.g., `release-blocker`) | Standardize across CI workflows       |
| OS-registered state | None                                          | None                                  |
| Secrets/env vars    | `HA_TOKEN`, `GITHUB_TOKEN`                    | Ensure consistency in CI environments |
| Build artifacts     | `scripts/` vs `src/staging_test/`             | Migration of scripts to `src/`        |

## Common Pitfalls

### Pitfall 1: WebSocket Timeout/Drop

**What goes wrong:** Staging audits fail due to network instability.
**How to avoid:** Implement robust retries and a connection "wait" period (90 seconds, per requirement) after integration load before starting audit.

### Pitfall 2: Flaky Staging States

**What goes wrong:** "Expected" unknown/unavailable states failing the build.
**How to avoid:** Use a configurable `ALLOWED_STAGING_STATES` environment variable that is strictly managed in `deploy-staging.yaml`.

## Environment Availability

| Dependency     | Required By | Available | Version | Fallback |
| -------------- | ----------- | --------- | ------- | -------- |
| Python 3.12    | All scripts | ✓         | 3.12.x  | —        |
| GitHub Actions | CI Pipeline | ✓         | —       | —        |

## Security Domain

| ASVS Category       | Applies | Standard Control                                  |
| ------------------- | ------- | ------------------------------------------------- |
| V5 Input Validation | Yes     | Validate all environment variables (URL/Token)    |
| V6 Cryptography     | Yes     | Use HTTPS for all API calls (enforced by default) |

### Known Threat Patterns

- **Token Exposure:** Ensure `GITHUB_TOKEN` and `HA_TOKEN` are masked in logs (CI handles this, ensure `print` doesn't leak them).

## Sources

### Primary (HIGH confidence)

- `src/staging_test/` (Existing skeleton)
- `scripts/staging_test_entities.py` / `staging_test_probe.py` (Existing logic)
- `docs/REQUIREMENTS.md` (Functional requirements)

### Secondary (MEDIUM confidence)

- GitHub REST API v3 Documentation

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - Built on established patterns
- Architecture: HIGH - Logical consolidation
- Pitfalls: MEDIUM - Dependent on environment stability

**Research date:** 2026-04-27
**Valid until:** 2026-05-27
