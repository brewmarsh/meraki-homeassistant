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
    echo "FATAL: RUNNER_REPO environment variable must be set (e.g., liptonj/meraki-homeassistant)."
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
# FIX: Execute config.sh using sudo to switch to the non-root 'runner' user
sudo -u runner /home/runner/actions-runner/config.sh "${CONFIG_ARGS[@]}"

echo "--- Starting Runner ---"
# FIX: Execute run.sh using sudo to switch to the non-root 'runner' user
exec sudo -u runner /home/runner/actions-runner/run.sh
