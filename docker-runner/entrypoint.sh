#!/bin/bash
set -e

# --- Cleaned-Up entrypoint.sh ---

# Sync internal docker group GID with the host socket GID
DOCKER_SOCKET_GID=$(stat -c '%g' /var/run/docker.sock 2>/dev/null)
if [ -n "$DOCKER_SOCKET_GID" ]; then
    echo "--- Syncing internal docker group GID to $DOCKER_SOCKET_GID ---"
    if getent group docker >/dev/null; then
        groupmod -g "$DOCKER_SOCKET_GID" docker || true
    else
        groupadd -g "$DOCKER_SOCKET_GID" docker
        usermod -aG docker runner
    fi
fi

# Action 4: Proactively apply a "Doctor" check to verify Docker CLI
echo "--- Doctor Check ---"
if command -v docker >/dev/null 2>&1; then
    docker --version
else
    echo "WARNING: Docker CLI not found in PATH"
fi

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
