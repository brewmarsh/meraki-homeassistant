# Agent artifact pre-commit suggestion

## Purpose

Provide a short example and guidance for a pre-commit hook that prevents accidental commits of agent/debugging artifacts (e.g., `git-error-*`, `message_to_user.txt`).

## Suggested `.pre-commit-config.yaml` additions

This example uses the `local` hook type to run a simple shell check that rejects commits containing forbidden filenames.

Example snippet (add to your existing `.pre-commit-config.yaml`):

repos:

- repo: local
  hooks:
  - id: forbid-agent-artifacts
    name: Forbid agent artifacts
    entry: bash -c 'git diff --cached --name-only | grep -E "(^|/)\b(git-error-|git-output-|message_to_user\.txt|\*~|\.tmp$)\b" && echo "Forbidden artifact files staged for commit" && exit 1 || exit 0'
    language: system
    files: ''

## Notes

- The snippet above runs a shell command to look at staged files and fails the commit if a match is found.
- On Windows/Powershell-only environments, replace the `entry` with an equivalent PowerShell one-liner or use a small Python script.
- You can harden this by writing a small script `tools/check_artifacts.py` and referencing it from this local hook instead of an inline command.

## Why we sometimes skip frontend bundles

- Frontend bundle files (for example `custom_components/meraki_ha/www/meraki-panel.js`) are generated artifacts produced by the build toolchain. - Use the pre-commit framework to automatically format code and check for common errors. This helps maintain code quality and consistency across the project.

- **Pre-commit hooks:**

  - **`ruff`**: For linting and formatting Python code.
  - **`black`**: For Python code formatting. (Note: This is commented out, relying on ruff)
  - **`codespell`**: For checking spelling in text files.
  - **`markdownlint-cli2`**: For enforcing markdown style.
  - **`prettier`**: For formatting code like JS, TS, CSS, HTML.
  - **`python-typing-update`**: For updating Python type hints.
  - **`trailing-whitespace`**: Removes trailing whitespace.
  - **`mixed-line-ending`**: Ensures consistent line endings (LF).
  - **`check-merge-conflict`**: Detects merge conflict markers.
  - **`check-toml`**: Checks TOML file syntax.
  - **`check-json`**: Checks JSON file syntax.
  - **`check-executables-have-shebangs`**: Ensures executable files have shebangs.
  - **`end-of-file-fixer`**: Ensures files end with a newline.

- **Local hook:**
  - **`forbid-agent-artifacts`**: Prevents committing agent-generated artifacts.

**Running Pre-commit Hooks:**
To ensure code quality and adherence to project conventions, run the following command before committing:

```bash
pre-commit run --all-files
```

This command will execute all configured hooks on the entire project. If any hook fails, it will indicate the issues and attempt to fix them. Resolve any reported issues before proceeding.

**Troubleshooting:**
If you encounter issues with specific hooks, consult the hook's documentation or the pre-commit framework. For example, if `ruff` or `black` fail, ensure you have the necessary Python environment set up. If `markdownlint-cli2` fails, check your Markdown files for compliance with the configured rules.

- Modifying generated bundles directly is unsafe — it will be overwritten by the build process and can break the frontend. For that reason, we recommend excluding such generated files from textual linters and instead run linters against source files (React/JSX/TSX) before bundling.
- If you need to allow a particular generated file through a linter for a one-off reason, prefer whitelisting the exact filename in the hook config or creating a small `--skip` list for that hook rather than editing the generated file itself.

## Recommendation

- Add the `forbid-agent-artifacts` hook to the repo and ensure maintainers install pre-commit locally.
- Keep the list of forbidden patterns in `docs/AGENT_FILE_CLEANUP.md` in sync with this hook.
