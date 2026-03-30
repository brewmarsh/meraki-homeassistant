#!/bin/bash
set -e

# --- Configuration ---
DOCKER_IMAGE="meraki-ha-runner:latest"

# Action 4: Unified COMMON_MOUNTS ensuring preserved socket access
# Mount the docker socket for DinD and the HA config directory
COMMON_MOUNTS="-v /var/run/docker.sock:/var/run/docker.sock -v /home/runner/ha_config:/ha_config"

deploy_runner() {
    local name=$1
    local token=$2
    local repo=$3

    echo "--- Deploying Runner: $name ---"

    # Ensure any existing container with the same name is removed
    docker rm -f "$name" 2>/dev/null || true

    # Action 1: Launch container with --group-add and common mounts
    docker run -d \
        --name "$name" \
        --restart always \
        --group-add $(stat -c '%g' /var/run/docker.sock) \
        $COMMON_MOUNTS \
        -e RUNNER_TOKEN="$token" \
        -e RUNNER_REPO="$repo" \
        -e RUNNER_NAME="$name" \
        "$DOCKER_IMAGE"

    # Action 2: Pre-launch Validation
    echo "--- Performing Pre-launch Validation for $name ---"
    # Give the container a moment to initialize the socket connection
    sleep 2

    if docker exec "$name" docker version > /dev/null 2>&1; then
        echo "SUCCESS: Docker socket connectivity verified in $name"
    else
        echo "FATAL: Docker socket connectivity FAILED in $name"
        echo "Diagnostic: Checking socket permissions inside container..."
        docker exec "$name" ls -l /var/run/docker.sock || true
        docker stop "$name"
        return 1
    fi

    echo "--- Runner $name deployed and validated successfully ---"
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [ "$#" -lt 3 ]; then
        echo "Usage: $0 <runner_name> <github_token> <repo_path>"
        exit 1
    fi
    deploy_runner "$1" "$2" "$3"
fi
