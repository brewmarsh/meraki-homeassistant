#!/bin/bash
set -e

# Source the bash shell profile for the runner user
# This ensures environment variables are properly set
source ~/.bashrc

# Check for required environment variables
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
CONFIG_ARGS+=(--name "$RUNNER_NAME")
CONFIG_ARGS+=(--labels "$LABELS")
CONFIG_ARGS+=(--unattended) # Skips confirmation prompts
CONFIG_ARGS+=(--replace)    # Replaces any existing runner with the same name

echo "--- Configuring Runner ---"
# EXECUTION MUST USE THE ABSOLUTE PATH TO THE RUNNER FILES
/home/runner/actions-runner/config.sh "${CONFIG_ARGS[@]}"

echo "--- Starting Runner ---"
# EXECUTION MUST USE THE ABSOLUTE PATH TO THE RUNNER FILES
exec /home/runner/actions-runner/run.sh
