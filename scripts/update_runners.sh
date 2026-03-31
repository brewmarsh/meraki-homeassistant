#!/bin/bash
# Script to deploy and update Meraki self-hosted runners

set -e

IMAGE_NAME="80m1/meraki-runner"
RUNNER_REPO="brewmarsh/meraki-homeassistant"

function deploy_runner() {
    local name=$1
    local token=$2
    local labels=$3

    echo "Deploying runner: $name"

    # Action 2: Add --group-add $(stat -c '%g' /var/run/docker.sock) to docker run
    # This allows the container's 'runner' user to access the host's docker socket
    # regardless of the GID mismatch between host and container.
    docker run -d \
        --name "$name" \
        --restart always \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /ha_config:/ha_config \
        -e RUNNER_NAME="$name" \
        -e RUNNER_REPO="$RUNNER_REPO" \
        -e RUNNER_TOKEN="$token" \
        -e LABELS="$labels" \
        --group-add $(stat -c '%g' /var/run/docker.sock) \
        "$IMAGE_NAME"

    # Action 4: Verify the fix with a "Doctor" check
    echo "Verifying Docker CLI in $name..."
    docker exec "$name" docker --version
}

# Example usage (commented out):
# deploy_runner "meraki-smoketest" "YOUR_TOKEN" "self-hosted,meraki-smoketest"
