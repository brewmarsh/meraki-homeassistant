# CI/CD Pipeline Best Practices

This document outlines a set of best practices for creating and maintaining effective CI/CD pipelines, based on the successful refactoring of the Meraki Home Assistant integration. These guidelines are designed to be shared and adapted for other repositories.

## 1. Consolidate and Clarify Workflows

**Principle:** Avoid a proliferation of small, single-purpose workflow files. Instead, create a few, clearly-named workflows that group related tasks.

**Implementation:**

- **Primary CI:** Maintain a primary CI workflow for each main branch (e.g., `main-ci.yaml`, `beta-ci.yaml`). These should run a comprehensive suite of checks, including linting, testing, and security scans.
- **Clear Naming:** Use a consistent and descriptive naming convention for all workflow files (e.g., `[branch]-ci.yaml`, `[purpose].yaml`).

## 2. Modernize and Standardize Tooling

**Principle:** Use modern, fast, and configurable tools to keep the pipeline efficient and easy to maintain.

**Implementation:**

- **All-in-One Linters:** Adopt modern linters like `ruff` to replace multiple older tools (`flake8`, `pydocstyle`, etc.). This simplifies configuration and dramatically speeds up linting steps.
- **Configuration as Code:** Store tool configurations in a central file like `pyproject.toml` to ensure consistency between local development and CI environments.

## 3. Enhance Security with Dependency Scanning

**Principle:** A secure application requires secure dependencies. Don't just scan your own code; scan the third-party libraries you use.

**Implementation:**

- **Automated Scanning:** Add a step to your primary CI workflow to scan for known vulnerabilities in your project's dependencies.
- **Recommended Tool:** For Python projects, `pip-audit` is a lightweight and effective tool that integrates easily into any pipeline.

## 4. Optimize for Speed with Caching

**Principle:** A fast CI/CD pipeline is essential for developer productivity. Don't waste time reinstalling the same dependencies on every run.

**Implementation:**

- **Cache Dependencies:** Use your CI platform's caching mechanism (e.g., `actions/cache` in GitHub Actions) to store and reuse dependencies.
- **Smart Keys:** Use a cache key based on the dependency file (e.g., `requirements.txt`, `package-lock.json`) to ensure the cache is only invalidated when dependencies change.

## 5. Separate and Clarify Release Workflows

**Principle:** Versioning and releasing should be a distinct, automated process, separate from the main CI pipeline.

**Implementation:**

- **Dedicated Release Workflows:** Create separate workflows for version bumping and release creation (e.g., `beta-version-update.yaml`, `production-version-update.yaml`).
- **Trigger on Merge:** Trigger these workflows only on successful merges to release branches (`main`, `beta`, etc.) to ensure that only tested code is released.
- **Semantic Versioning:** Use tools like `bump2version` and follow a clear versioning scheme (e.g., Semantic Versioning) to communicate the impact of changes.

## 6. Document Agent and Developer Workflows

**Principle:** Clear documentation is essential for ensuring that all contributors (human or AI) follow the same best practices.

**Implementation:**

- **`AGENTS.md`:** Maintain a dedicated file with instructions for AI agents, including branching strategies, commit message formats, and architectural patterns.
- **Branching and Commits:** Enforce a consistent branching model (e.g., `feature/<detail>`, `fix/<detail>`) and commit message format (e.g., Conventional Commits) to keep the project history clean and navigable.
