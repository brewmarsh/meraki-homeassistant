# System Requirements for CI/CD, Build, and Versioning

This document outlines the requirements for setting up a CI/CD, build, and versioning system based on the practices of the `meraki-homeassistant` project.

## 1. Development Environment

The project requires both Python and Node.js for development and automation.

- **Python:**
  - Version: 3.9 or higher.
  - Dependencies are managed with `pip`.
  - Application dependencies are listed in `requirements.txt`.
  - Development dependencies are listed in `requirements_dev.txt`.
- **Node.js:**
  - Version: 18 or higher.
  - Dependencies are managed with `npm`.
  - Development dependencies are listed in `package.json`.

## 2. Git Hooks

The project uses the `pre-commit` framework to enforce code quality and consistency before code is committed.

- **Setup:** Developers must install `pre-commit` and run `pre-commit install` to set up the Git hooks locally.
- **Configuration:** The hooks are defined in the `.pre-commit-config.yaml` file.
- **Required Hooks:**
  - `pre-commit-hooks`: For basic checks like merge conflicts, JSON/TOML syntax, and end-of-file fixing.
  - `black`: For automated Python code formatting.
  - `ruff`: For Python linting and style checking.
  - `codespell`: For checking spelling errors.
  - `prettier`: For formatting non-Python files (e.g., Markdown, YAML).
  - `markdownlint-cli2`: For linting Markdown files.

## 3. Versioning Strategy

The project uses an automated versioning system based on `bump2version` and conventional commits.

- **Source of Truth:** The version number is stored in a `manifest.json` file (e.g., `custom_components/my_integration/manifest.json`). The versioning scheme should follow semantic versioning (e.g., `1.2.3`).
- **Automation Tool:** `bump2version` is used to increment the version number. A `.bumpversion.cfg` file must be created to configure it:
  - It should be configured to update the version in the `manifest.json` file.
  - It should have `commit = False` and `tag = False` set, as the CI/CD pipeline will handle this.
- **Pull Request Titles:** The version increment type is determined by the pull request title:
  - `[major]`: For a major version increment (e.g., `1.x.x` -> `2.0.0`).
  - `[minor]`: For a minor version increment (e.g., `1.2.x` -> `1.3.0`).
  - If neither is present, a `patch` increment is performed by default (e.g., `1.2.3` -> `1.2.4`).
- **Version Synchronization:** A `package.json` file should be used for Node.js dependencies. The version in this file must be kept in sync with the version in `manifest.json`. A script (e.g., `get-version.js`) should be created to read the version from `manifest.json`.

## 4. CI/CD Pipeline (GitHub Actions)

The CI/CD pipeline is implemented using GitHub Actions. The following workflows are required:

<<<<<<< HEAD
\*\*4.1. Code Quality and Testing (`python-lint.yaml`)
=======
### 4.1. Code Quality and Testing (`python-lint.yaml`)
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)

- **Trigger:** On pushes and pull requests to the `main` branch.
- **Steps:**

1. Set up Python 3.9.
2. Install Python dependencies from `requirements_dev.txt`.
3. Run `black --check` to verify code formatting.
4. Run `flake8` for linting.
5. Run `mypy` for static type checking.
6. Run `pydocstyle` for docstring style checking.
7. Run `bandit` for security scanning.
8. Run `pytest` to execute the test suite and generate a coverage report.
9. (Optional) Upload the coverage report to a service like Codecov.

<<<<<<< HEAD
\*\*4.2. Home Assistant Validation (Optional, for HA projects)
=======
### 4.2. Home Assistant Validation (Optional, for HA projects)
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)

- If the project is a Home Assistant custom component, two validation workflows should be included:
  - **`validate.yaml`**: Uses the `hacs/action` to validate the project for the Home Assistant Community Store.
  - **`hassfest.yaml`**: Uses the `home-assistant/actions/hassfest` action to perform Home Assistant specific validation.

<<<<<<< HEAD
\*\*4.3. Documentation Deployment (`mkdocs-deploy.yaml`)
=======
### 4.3. Documentation Deployment (`mkdocs-deploy.yaml`)
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)

- **Trigger:** On the creation of a new release.
- **Steps:**
  1. Set up Python.
  2. Install development dependencies.
  3. Build the documentation using `mkdocs build`.
  4. Deploy the generated `site` directory to the `gh-pages` branch using the `peaceiris/actions-gh-pages` action.

<<<<<<< HEAD
\*\*4.4. Versioning and Release (`version_and_release.yaml`)
=======
### 4.4. Versioning and Release (`version_and_release.yaml`)
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)

- **Trigger:** When a pull request is closed and merged into the `main` branch.
- **Job 1: `version`**
  1. Check out the `main` branch.
  2. Set up Python and Node.js.
  3. Install `bump2version` and `npm` dependencies.
  4. Determine the version increment type from the PR title.
  5. Run `bumpversion` to update the version in `manifest.json`.
  6. Update the version in `package.json`.
  7. Generate a `CHANGELOG.md` file using `conventional-changelog-cli`.
  8. Commit the updated files (`manifest.json`, `package.json`, `.bumpversion.cfg`, `CHANGELOG.md`) back to the `main` branch.
  9. Upload the release notes as an artifact.
- **Job 2: `release`**
  1. Depends on the successful completion of the `version` job.
  2. Download the release notes artifact.
  3. Create a new GitHub release with a tag in the format `vX.Y.Z` and the release notes as the body.
