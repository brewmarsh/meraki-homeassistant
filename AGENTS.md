# `AGENTS.md`: Agent & Developer Guidelines

<<<<<<< HEAD
**Mandatory: All Pull Requests must target the `beta` branch. Never target `main` for feature work.**

=======
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
This document provides essential instructions for AI agents and human developers working across this organization's codebases. Adhering to these guidelines is critical for maintaining code quality, consistency, and stability.

This file contains **common rules** that apply to _all_ projects. For project-specific details (like technology stack, file paths, and build commands), please refer to the `README.md` or `CONTRIBUTING.md` file in the specific repository.

---

## 1. Onboarding & Project-Specifics

Before starting work, review the following files in the **root of the specific repository**:

- **`README.md`**: Contains the project's objective, technology stack, and definitive guide for setup, installation, and deployment.
- **`CONTRIBUTING.md` (if present)**: Contains detailed, project-specific rules, key file paths, and architectural patterns you must follow.
- **`[e.g., pyproject.toml, package.json]`**: Review the project's dependencies and available scripts.

---

## 2. Version Control & Naming

A clean Git history is essential for collaboration. All branches and commits **must** follow these naming conventions.

### Branch Naming

Use a prefix separated by a slash (`/`) to categorize your work.

- **`feature/<short-description>`**: For adding new features (e.g., `feature/add-user-profile`).
- **`fix/<short-description>`**: For fixing bugs (e.g., `fix/login-csrf-bug`).
- **`chore/<short-description>`**: For maintenance, refactoring, or CI/CD tasks (e.g., `chore/update-docker-base-image`).
- **`docs/<short-description>`**: For documentation-only changes (e.g., `docs/update-api-examples`).

### Commit (Check-in) Naming

All commit messages **must** follow the [**Conventional Commits**](https://www.conventionalcommits.org/en/v1.0.0/) format. This is not optional.

The format is: `type(scope): subject`

- **`feat:`**: A new feature (e.g., `feat: allow users to reset their password`).
- **`fix:`**: A bug fix (e.g., `fix: correct password hash iterations during login`).
- **`docs:`**: Documentation-only changes (e.g., `docs: update AGENTS.md with commit standards`).
- **`style:`**: Code style changes (e.g., `style: run ruff formatter on all python files`).
- **`refactor:`**: A code change that neither fixes a bug nor adds a feature (e.g., `refactor: extract api client into separate service`).
- **`test:`**: Adding missing tests or correcting existing tests (e.g., `test: add unit test for new validation logic`).
- **`chore:`**: Changes to the build process or auxiliary tools (e.g., `chore: add new linter to pre-commit hook`).

<<<<<<< HEAD
## Pull Request Standards

- **Issue Linking:** Every PR must link to its source issue.
- **Format:** Always include "Fixes #<number>" in the PR title or the first line of the description.
- **Base Branch:** All PRs should target the `beta` branch unless explicitly told otherwise.

=======
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
---

## 3. Code Organization & Naming

### General Naming Conventions

- **Python:**
  - Files: `snake_case.py`
  - Classes: `PascalCase`
  - Functions & Variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
- **JavaScript/React:**
  - Files & Components: `PascalCase.jsx` (for components), `camelCase.js` (for utilities).
  - Functions & Variables: `camelCase`
  - Constants: `UPPER_SNAKE_CASE`

### General Structure

- **Keep Logic Separate:** Route handlers (`routes.py`, `views.py`) should only parse requests and return responses. All business logic **must** be in separate service functions/classes (e.g., in a `services/` or `utils/` directory).
- **Keep Clients Separate:** All third-party API client logic (e.g., Meraki API, Google API) **must** be in its own module (e.g., `clients/meraki_client.py`).
- **Constants:** Do not use "magic strings" or numbers in code. Define them as constants in a central `const.py` file or at the top of the module.

---

## 4. Coding Standards & Best Practices

### 4.1. General Principles

- **Use the ORM:** When a project uses an ORM (like SQLAlchemy or Django ORM), **all** database interactions must use it. Do not write raw SQL queries unless absolutely necessary.
- **Beware N+1 Queries:** When fetching lists of items that have related data, use the ORM's built-in methods (e.g., `joinedload`, `subqueryload`, `select_related`, `prefetch_related`) to prevent N+1 query bugs.
- **Security:**
  - **Validate Input:** All user-provided input **must** be validated on the server side.
  - **CSRF Protection:** All state-changing requests (POST, PUT, DELETE) **must** be protected against Cross-Site Request Forgery (CSRF).
  - **Passwords:** Never handle or store passwords in plaintext. Use `werkzeug.security` or `django.contrib.auth` for hashing.

### 4.2. Language-Specific Rules (Python)

- **Linting & Formatting:** This project uses [**Ruff**](https://docs.astral.sh/ruff/) for linting _and_ formatting (replacing Black, Flake8, and isort).
  - All code **must** be formatted with `ruff format .` before committing.
  - All code **must** be free of linter errors from `ruff check .`.
- **Type Hinting:** All new functions **must** include [PEP 484](https://peps.python.org/pep-0484/) type hints for all arguments and return values.
- **Docstrings:** All public modules, classes, and functions **must** have docstrings following the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#3.8-comments-and-docstrings).
- **Dependencies:** Use `pyproject.toml` with a tool like [Poetry](https://python-poetry.org/) or [PDM](https://pdm.fming.dev/) for dependency management. `requirements.txt` should only be used if the project is already using it.
- **Error Handling:** Use specific exceptions. Do not use broad `except Exception:` blocks.

### 4.3. Language-Specific Rules (JavaScript/React)

- **Linting & Formatting:** This project uses [**Prettier**](https://prettier.io/) for formatting and [**ESLint**](https://eslint.org/) for linting.
- **Modern JS:** Use modern ECMAScript features (e.g., `const`/`let` over `var`, arrow functions, spread syntax).
- **React:**
  - Use **Functional Components** and **Hooks** (e.g., `useState`, `useEffect`) for all new code.
  - Do not write class-based components.

---

## 5. Quality & Testing

### 5.1. Code Quality Tools

- **Pre-commit Hooks:** This repository should use `pre-commit` to automatically run linters and formatters before each commit. You can install it with `pre-commit install`.
- **Static Analysis:** This project may use `mypy` (Python type checking) or `bandit` (Python security analysis). These checks must pass in the CI pipeline.

### 5.2. Testing

- **Coverage:** All new features or business logic **must** be accompanied by unit tests.
- **Run Tests:** Always run the full test suite (e.g., `pytest`, `npm test`) _before_ submitting your code.
- **Mocks:** When writing tests, ensure all mocks are as accurate as possible to the real APIs or functions they are replacing.

---

## 6. Documentation & Iteration

- **Iterative Improvement:** If you encounter an issue (e.g., a security vulnerability, a bug, a confusing pattern), look for other instances of the same problem in the codebase and fix them all.
- **Update Documentation:** As you make changes, ensure that `README.md` and `CONTRIBUTING.md` are updated to reflect the new state of the application.
- **Update This File:** If you discover a new development technique, a useful debugging procedure, or a common pitfall, please update _this_ `AGENTS.md` file to help future agents.
<<<<<<< HEAD

---

## 7. Knowledge Base

This section serves as a repository for institutional knowledge and recurring fixes. Before tackling an issue, review this section to see if a similar problem has been solved before.

- **[Symptom/Problem]:** [Brief description of the issue]
  - **Fix:** [Explanation of the solution]
  - **Reasoning:** [Why this fix works and what the root cause was]

## 8. Conflict Avoidance Strategy
Atomic Commits: Only modify the files absolutely necessary for the task.

Manifest Locking: If a task requires a version bump in manifest.json, check if a pending PR already has a higher version. Use the highest version available.

Rebase First: Before starting any new task, always git checkout beta followed by git pull to ensure the starting point is current.

## 9. Automated Conflict Resolution Protocol
When summoned to resolve conflicts:

Always Rebase: Never use git merge. Always use git rebase origin/beta.

Infrastructure Priority: If manifest.json or requirements.txt have conflicts, accept the version number from beta unless the current task specifically requires a bump.

Naming Continuity: Ensure the meraki_select renaming is preserved. Do not let a rebase revert folders back to the standard library select name.
=======
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
