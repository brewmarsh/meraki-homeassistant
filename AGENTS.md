# Agent Instructions & Project Standards

## 1. Critical Environment Constraints
* **Target Branch:** ALL development, fixes, and features MUST target the `beta` branch. Never target `main` unless explicitly instructed for a release.
* **Python Version:** The project target is Python 3.13. However, CI runners may use 3.13.0. Do not lock `homeassistant` core in `requirements_dev.txt`; use `pytest-homeassistant-custom-component` instead.
* **Module Shadowing:** Avoid naming directories after Python standard libraries. 
    * *Example:* The `select` platform MUST be named `meraki_select` to avoid crashing system networking tools.

## 2. Coding Standards (Home Assistant)
* **Config Flow:** Always use `homeassistant.helpers.selector` for UI schemas. Raw Python types (e.g., `vol.Required(str)`) are forbidden as they fail serialization.
* **Formatting:** Follow PEP 8. Use `ruff` for linting.
* **Documentation:** All public functions require Google-style docstrings.
* **Commits:** Use Conventional Commits (e.g., `fix:`, `feat:`, `chore:`).

## 3. Conflict Resolution & Robustness
* **Linear History:** Always `git rebase origin/beta`. Never use `git merge`.
* **Atomic Changes:** Only modify files strictly necessary for the task to minimize merge conflicts.
* **Pre-Flight Check:** Before submitting a PR, agents must:
    1. Run `python -m py_compile` on modified files.
    2. Verify `pip-audit -r requirements.txt -l` passes with 0 vulnerabilities.
    3. Ensure version numbers in `manifest.json` align with the `beta` branch.

## 4. Known Issues & Lessons Learned
* **ValueError in UI:** Caused by passing `[str]` instead of a `SelectSelector` or `TextSelector`.
* **Cognitive Loop Error:** Caused by using `base_branch` or `instructions_path` in GitHub Actions. Only use `starting_branch`.
