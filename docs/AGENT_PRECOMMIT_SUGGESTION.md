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

- Frontend bundle files (for example `custom_components/meraki_ha/www/meraki-panel.js`) are generated artifacts produced by the build toolchain. They often contain minified or compiled identifiers (short tokens such as `Ot`, `Te`, `ue`) that look like misspellings to `codespell` or similar textual linters.
- Modifying generated bundles directly is unsafe — it will be overwritten by the build process and can break the frontend. For that reason, we recommend excluding such generated files from textual linters and instead run linters against source files (React/JSX/TSX) before bundling.
- If you need to allow a particular generated file through a linter for a one-off reason, prefer whitelisting the exact filename in the hook config or creating a small `--skip` list for that hook rather than editing the generated file itself.

## Recommendation

- Add the `forbid-agent-artifacts` hook to the repo and ensure maintainers install pre-commit locally.
- Keep the list of forbidden patterns in `docs/AGENT_FILE_CLEANUP.md` in sync with this hook.
