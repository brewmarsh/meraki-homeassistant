#!/bin/bash
set -e

# --- Meraki Runner Entrypoint ---

# Action: Sync internal docker group GID with the host socket GID
# This ensures the 'runner' user has permission to use the mounted docker socket.
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

# Diagnostic: Verify Docker CLI availability
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

# ACTION: Cleanup any existing runner configuration to ensure ephemeral behavior.
# If /home/runner/actions-runner is mounted to a persistent volume,
# we must clear the old state before config.sh can run successfully.
echo "--- Cleaning up stale runner state ---"
sudo -u runner rm -f /home/runner/actions-runner/.runner /home/runner/actions-runner/.credentials /home/runner/actions-runner/.credentials_rsaparams

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

# Action 3: Append the --replace flag to forcefully overwrite existing registrations.
CONFIG_ARGS+=(--replace)

echo "--- Configuring Runner ---"
# Execute config.sh using sudo to switch to the non-root 'runner' user
sudo -u runner /home/runner/actions-runner/config.sh "${CONFIG_ARGS[@]}"

echo "--- Starting Runner ---"
# Startup diagnostic
which docker
docker --version

# Action: Use exec to launch the runner process as PID 1
# This ensures correct signal handling and allows 'docker exec' to work reliably.
cd /home/runner/actions-runner
exec sudo -E -u runner ./run.sh
