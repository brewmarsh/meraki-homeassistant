Archive for agent artifacts
===========================

This directory stores artifacts created by automated agents or developers when debugging or triaging issues.

Policy
------
- Artifacts should be moved here (not left in the repo root).
- Each artifact must have a short `meta` file alongside it explaining:
  - who created it
  - why it's needed
  - the retention policy (recommended 30 days)

To move an artifact: create a subfolder named with the date and reason, and include a `meta.md` file.

Example layout:

- `archive/agent-artifacts/2025-11-20-lint-debug/`
  - `git-error-1756303602882.txt`
  - `meta.md`
