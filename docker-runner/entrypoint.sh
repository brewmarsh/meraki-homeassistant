#!/bin/bash
set -e

# --- Cleaned-Up entrypoint.sh ---

# Check for required environment variables
# Note: We rely on the parent shell/environment to have set GITHUB_PAT.
if [ -z "$RUNNER_TOKEN" ]; then
    echo "FATAL: RUNNER_TOKEN environment variable must be set."
    exit 1
fi
if [ -z "$RUNNER_REPO" ]; then
    echo "FATAL: RUNNER_REPO environment variable must be set (e.g., brewmarsh/meraki-homeassistant)."
    exit 1
fi

# Define the configuration arguments
CONFIG_ARGS=()
CONFIG_ARGS+=(--url "https://github.com/${RUNNER_REPO}")
CONFIG_ARGS+=(--token "$RUNNER_TOKEN")

# Optional arguments
if [ -n "$RUNNER_NAME" ]; then
    CONFIG_ARGS+=(--name "$RUNNER_NAME")
fi
if [ -n "$LABELS" ]; then
    CONFIG_ARGS+=(--labels "$LABELS")
fi
if [ "$EPHEMERAL" = "true" ]; then
    CONFIG_ARGS+=(--ephemeral)
fi

# Standard flags for non-interactive Docker deployment
CONFIG_ARGS+=(--unattended) # Skips confirmation prompts
CONFIG_ARGS+=(--replace)    # Replaces any existing runner with the same name

echo "--- Configuring Runner ---"
# EXECUTION USES THE ABSOLUTE PATH TO THE RUNNER FILES
# The container is running as root (UID 0) to ensure the subsequent workflow copy succeeds.
/home/runner/actions-runner/config.sh "${CONFIG_ARGS[@]}"

echo "--- Starting Runner ---"
# EXECUTION USES THE ABSOLUTE PATH TO THE RUNNER FILES
# 'exec' replaces the current shell process with the run.sh process.
exec /home/runner/actions-runner/run.sh
