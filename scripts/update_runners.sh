#!/bin/bash
# Script to deploy and update Meraki self-hosted runners
#
# Usage:
#   ./scripts/update_runners.sh [--publish]
#
# Flags:
#   --publish: Builds the image locally and pushes it to Docker Hub before deployment.

set -e

IMAGE_NAME="80m1/meraki-runner"
RUNNER_REPO="brewmarsh/meraki-homeassistant"

# Action 1: Optional Build and Publish Loop
if [[ "$1" == "--publish" ]]; then
    echo "--- Building and Pushing new image: $IMAGE_NAME ---"
    # Ensure we are in the correct directory context for the build
    # Assuming script is run from project root
    docker build -t "$IMAGE_NAME" ./docker-runner
    docker push "$IMAGE_NAME"
    echo "--- Publish Complete ---"
fi

# Pull the latest image (or verify the local build)
echo "--- Pulling latest runner image: $IMAGE_NAME ---"
docker pull "$IMAGE_NAME"

# Action 3: Print image digest for traceability
DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' "$IMAGE_NAME" 2>/dev/null || echo "Local build")
echo "Current Image Digest: $DIGEST"

# Action 2: Pre-Flight Health Check
# Verify the Docker CLI is functional within the image before deploying runners
echo "--- Pre-Flight Health Check ---"
if ! docker run --rm "$IMAGE_NAME" docker --version; then
    echo "FATAL: Docker CLI is missing or broken in image $IMAGE_NAME."
    echo "Check the Dockerfile and ensure docker-ce-cli is correctly installed."
    exit 1
fi
echo "Pre-flight check passed: Docker CLI is functional."

function deploy_runner() {
    local name=$1
    local token=$2
    local labels=$3

    echo "Deploying runner: $name"

    # Action 3 (Refined): Dynamic GID Mapping and Staging Environment Setup
    # - --group-add maps the host socket GID dynamically.
    # - Ensure image has latest CLI fixes for tools like agent-score (diff --base).

    # Remove existing container if it exists
    docker rm -f "$name" 2>/dev/null || true

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

    # Final "Doctor" check on the new container
    echo "Verifying Docker CLI in $name..."
    docker exec "$name" docker --version

    # Visual confirmation of Agent Scorecard compatibility (diagnostic)
    echo "Verifying Agent Scorecard compatibility..."
    docker exec "$name" bash -c "if command -v agent-score >/dev/null; then agent-score --version; else echo 'agent-score not pre-installed (installed at runtime)'; fi"
}

# Example usage (uncomment and replace YOUR_TOKEN to run manually):
# deploy_runner "meraki-smoketest" "YOUR_TOKEN" "self-hosted,meraki-smoketest"
